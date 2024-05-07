import json
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

# TODO: Add better classproperty!
#  If you read this and have an idea how to implement this, please create an issue!


CURRENT_PATH = Path(__file__).parent


class AlreadyRegisteredError(BaseException):
    """AlreadyRegisteredError"""

    def __init__(self, type_, thing):
        self.type_ = type_
        self.thing = thing

    def __str__(self):
        return f"{self.type_} {self.thing!r} is already registered!"


class NotRegisteredError(BaseException):
    """NotRegisteredError"""

    def __init__(self, type_, thing):
        self.type_ = type_
        self.thing = thing

    def __str__(self):
        return f"{self.type_} {self.thing!r} is not registered!"


class PluginLoadError(BaseException):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return f"Can't load plugin: {self.reason}!"


class InvalidJSONDataError(BaseException):
    pass


class EmptyModel:
    def __init__(self, json_data):
        pass

    @property
    def is_right(self):
        return True


def base_cli(model):
    return True


class QuizType:
    def __init__(self, name, identifier, model=None, cli=None):
        self.name = name
        self.identifier = identifier

        self.model_class = model if model is not None else EmptyModel
        self.cli_func = cli if cli is not None else base_cli

    def cli(self, func):
        self.cli_func = func
        return func

    def model(self, func):
        self.model_class = func
        return func


class Plugin:
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name
        self.quiz_types = {}

        if identifier in PluginManager.all_plugins:
            raise AlreadyRegisteredError("Plugin", identifier)

        PluginManager.add_plugin(self)

    @classmethod
    def get_plugin(cls, identifier):
        if identifier not in PluginManager.all_plugins:
            raise NotRegisteredError("Plugin", identifier)
        else:
            return PluginManager.all_plugins[identifier]

    def register_quiz_type(self, identifier, name, model=None, cli=None):
        if identifier in self.quiz_types:
            raise AlreadyRegisteredError("QuizType", identifier)
        else:
            self.quiz_types[identifier] = QuizType(
                name=name,
                identifier=identifier,
                model=model,
                cli=cli,
            )

    def quiz_type(self, identifier, name):
        if identifier in self.quiz_types:
            return self.quiz_types[identifier]
        else:
            quiz_type = QuizType(name, identifier)
            self.quiz_types[identifier] = quiz_type
            return quiz_type


class PluginManager:
    """Manager to manage plugins."""
    activated_plugins = {}
    deactivated_plugins = {}

    @classmethod
    def activate_plugin(cls, plugin_id):  # Maybe add Errorhandling?
        """Activate the plugin whose plugin_id is equals to plugin_id."""
        if plugin_id in cls.deactivated_plugins:
            cls.activated_plugins[plugin_id] = cls.deactivated_plugins.pop(plugin_id)

    @classmethod
    def deactivate_plugin(cls, plugin_id):  # Maybe add Errorhandling too?
        """Deactivate the plugin whose plugin_id is equals to plugin_id."""
        if plugin_id in cls.deactivated_plugins:
            cls.deactivated_plugins[plugin_id] = cls.activated_plugins.pop(plugin_id)

    @classmethod
    def remove_plugin(cls, plugin_id):
        """Remove the plugin, whose plugin_id is equals to plugin_id."""
        if plugin_id in cls.activated_plugins:
            del cls.activated_plugins[plugin_id]

        elif plugin_id in cls.deactivated_plugins:
            del cls.deactivated_plugins[plugin_id]

    @classmethod
    def add_plugin(cls, plugin, activate=False):
        """Register a Plugin. If the activate flag is set, the plugin will be activated."""
        if activate:
            cls.activated_plugins[plugin.identifier] = plugin
        else:
            cls.deactivated_plugins[plugin.identifier] = plugin

    @classmethod
    def plugin_from_main_folder(cls, path_to_main_folder):
        """Load a plugin from the main folder. This requires that there is a file, called 'extension.json'."""
        extension_file = Path(path_to_main_folder) / "extension.json"

        if not extension_file.exists():
            raise PluginLoadError("No 'extension.json'")

        with open(Path(path_to_main_folder) / "extension.json", encoding="utf-8") as plugin_config_file:
            plugin_config = json.load(plugin_config_file)

            try:
                plugin_id = plugin_config["id"]
            except KeyError:
                raise PluginLoadError("No id specified in 'extension.json'")

            plugin_python_files = [Path(path_to_main_folder) / file_name for file_name in plugin_config["files"]]

            if not all((path.exists() for path in plugin_python_files)):
                raise PluginLoadError(f"Invalid file referred in 'extension.json' of plugin {plugin_id!r}")

            for plugin_python_file in plugin_python_files:
                # Load plugin_python_file as module into extension_modul
                spec = spec_from_file_location(plugin_python_file.stem, plugin_python_file)
                extension_modul = module_from_spec(spec)
                # Execute modul
                spec.loader.exec_module(extension_modul)

        cls.activate_plugin(plugin_id)

        return cls.all_plugins[plugin_id]  # The Plugin is already registered. It registers itself on creation

    @classmethod
    @property
    def all_plugins(cls):
        return cls.activated_plugins | cls.deactivated_plugins

    @classmethod
    @property
    def all_quiz_types(cls):
        """All quiz types of all activated plugins"""
        return {
            identifier: quiz_type
            for plugin in cls.activated_plugins.values()
            for identifier, quiz_type in plugin.quiz_types.items()
        }


def execute_quiz_as_cli_from_quiz_file(quiz_file_path):
    with open(quiz_file_path, encoding="utf-8") as quiz_file:
        try:
            quiz_config = json.load(quiz_file)
        except json.decoder.JSONDecodeError:
            print("Invalid JSON file!")
            return

    name = quiz_config.get("name", "No name specified!")

    quiz_clis_and_models = []
    for quiz_data in quiz_config.get("quizzes", []):
        model = PluginManager.all_quiz_types[quiz_data["type"]].model_class(quiz_data)
        cli = PluginManager.all_quiz_types[quiz_data["type"]].cli_func

        quiz_clis_and_models.append((cli, model))

    right_tries = 0
    print(f"Welcome to {name!r}!\nPlease answer the following questions!\n")
    for cli, model in quiz_clis_and_models:
        is_right = cli(model)

        right_tries += is_right
        print("That's right!" if is_right else "That's wrong! :(")
        print()

    total_percent = int(right_tries / len(quiz_clis_and_models) * 100) if right_tries != 0 else 0
    print(f"Total: {total_percent}% {right_tries}/{len(quiz_clis_and_models)}")
