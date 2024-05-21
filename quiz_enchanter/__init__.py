import json
import logging
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

CURRENT_PATH = Path(__file__).parent

logger = logging.getLogger(__name__)


class AlreadyRegisteredError(BaseException):
    """AlreadyRegisteredError"""

    def __init__(self, thing, type_=None):
        self.type_ = thing.__class__.__name__ if type is None else type_
        self.thing = thing

    def __str__(self):
        return f"{self.type_} {self.thing!r} is already registered!"


class NotRegisteredError(BaseException):
    """NotRegisteredError"""

    def __init__(self, thing, type_=None):
        self.type_ = thing.__class__.__name__ if type is None else type_
        self.thing = thing

    def __str__(self):
        return f"{self.type_} {self.thing!r} is not registered!"


class BaseModel:  # It's redundant, maybe remove it in later versions?
    @property
    def is_right(self):
        return True


def base_cli():
    return True


class DictModel(dict, BaseModel):
    pass


class QuizType:
    def __init__(self, name, identifier, model=DictModel, cli=base_cli):
        self.name = name
        self.identifier = identifier

        self.model_class = model
        self.cli_func = cli

    def cli(self, func):
        self.cli_func = func
        return func

    def model(self, func):
        self.model_class = func
        return func


class Plugin:
    GLOBAL_PLUGINS = {}

    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name
        self.quiz_types = {}

        if identifier in Plugin.GLOBAL_PLUGINS:
            raise AlreadyRegisteredError(identifier)

        Plugin.GLOBAL_PLUGINS[identifier] = self

    @classmethod
    def get_plugin(cls, identifier):
        if identifier not in Plugin.GLOBAL_PLUGINS:
            raise NotRegisteredError(identifier, "plugin")
        else:
            return Plugin.GLOBAL_PLUGINS[identifier]

    def register_quiz_type(self, identifier, name, model=None, cli=None):
        if identifier in self.quiz_types:
            raise AlreadyRegisteredError(identifier)
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

    def __init__(self, activated_plugins=None, deactivated_plugins=None):
        if deactivated_plugins is None:
            deactivated_plugins = {}
        self.deactivated_plugins = deactivated_plugins

        if activated_plugins is None:
            activated_plugins = {}
        self.activated_plugins = activated_plugins

    def activate_plugin(self, plugin_id):
        """Activate the plugin whose identifier is equals to plugin_id."""
        if plugin_id in self.deactivated_plugins:
            self.activated_plugins[plugin_id] = self.deactivated_plugins.pop(plugin_id)
            # Move from activated to deactivated plugins

        elif plugin_id in Plugin.GLOBAL_PLUGINS:
            self.activated_plugins[plugin_id] = Plugin.GLOBAL_PLUGINS[plugin_id]

    def deactivate_plugin(self, plugin_id):
        """Deactivate the plugin whose identifier is equals to plugin_id."""
        if plugin_id in self.activated_plugins:
            self.deactivated_plugins[plugin_id] = self.activated_plugins.pop(plugin_id)
            # Move from deactivated to activated plugins

        elif plugin_id in Plugin.GLOBAL_PLUGINS:
            self.deactivated_plugins[plugin_id] = Plugin.GLOBAL_PLUGINS[plugin_id]

    def remove_plugin(self, plugin_id):
        """Remove the plugin, whose plugin_id is equals to plugin_id."""
        if plugin_id in self.activated_plugins:
            del self.activated_plugins[plugin_id]

        elif plugin_id in self.deactivated_plugins:
            del self.deactivated_plugins[plugin_id]

    def add_plugin(self, plugin, activate=False):
        """Add a Plugin. If the activate flag is set, the plugin will be activated."""
        if activate:
            self.activated_plugins[plugin.identifier] = plugin
        else:
            self.deactivated_plugins[plugin.identifier] = plugin

    @property
    def all_plugins(self):
        return self.activated_plugins | self.deactivated_plugins

    @property
    def all_activated_quiz_types(self):
        """All quiz types of all activated plugins"""
        return {
            identifier: quiz_type
            for plugin in self.activated_plugins.values()
            for identifier, quiz_type in plugin.quiz_types.items()
        }

    @classmethod
    def plugin_from_main_folder(cls, path_to_main_folder):
        """Load a plugin from the main folder. This requires that there is a file, called 'extension.json'."""
        with open(Path(path_to_main_folder) / "extension.json", encoding="utf-8") as plugin_config_file:
            plugin_config = json.load(plugin_config_file)

            plugin_id = plugin_config["id"]

            plugin_python_files = (Path(path_to_main_folder) / file_name for file_name in plugin_config["files"])

            for plugin_python_file in plugin_python_files:
                # Load plugin_python_file as module into extension_modul
                spec = spec_from_file_location(plugin_python_file.stem, plugin_python_file)
                extension_modul = module_from_spec(spec)
                # Execute modul
                spec.loader.exec_module(extension_modul)

        if plugin_id not in Plugin.GLOBAL_PLUGINS:
            raise NotRegisteredError(plugin_id, "Plugin")
        return Plugin.GLOBAL_PLUGINS[plugin_id]  # The Plugin is already registered. It registers itself on creation


def execute_quiz_as_cli_from_quiz_file(quiz_file_path, plugin_manager):
    quiz_file_path = Path(quiz_file_path)
    if not quiz_file_path.exists():
        raise FileNotFoundError(f"File {quiz_file_path} doesn't exists!")

    with quiz_file_path.open("r", encoding="utf-8") as quiz_file:
        quiz_config = json.load(quiz_file)

    quiz_name = quiz_config["name"]

    quiz_clis_and_models = []
    for quiz_data in quiz_config["quizzes"]:
        if "type" not in quiz_data:
            raise KeyError("Quiz data has no key 'type' field!")

        quiz_type_as_string = quiz_data["type"]
        if quiz_type_as_string not in plugin_manager.all_activated_quiz_types:
            raise NotRegisteredError(quiz_type_as_string, "Quiz type")

        quiz_type = plugin_manager.all_activated_quiz_types[quiz_type_as_string]

        model = quiz_type.model_class(quiz_data)
        cli = quiz_type.cli_func
        quiz_clis_and_models.append((model, cli))

        logger.debug(f"Loaded model and cli for quiz type {quiz_type_as_string}.")

    right_tries = 0
    print(f"Welcome to {quiz_name!r}!\nPlease answer the following questions!\n")
    for model, cli in quiz_clis_and_models:
        is_right = cli(model)
        right_tries += is_right

        print("That's right!" if is_right else "That's wrong! :(")
        print()

    print(f"Total: {int(right_tries / len(quiz_clis_and_models) * 100)}% {right_tries}/{len(quiz_clis_and_models)}")


def execute_quiz_as_cli(path):
    file = Path(path)
    plugin_folders = [CURRENT_PATH / "extensions/default_extension"]

    if file.is_dir():
        quiz_path = file / "quiz.json"

        plugin_main_path = file / "plugins"
        if plugin_main_path.exists():
            plugin_folders += plugin_main_path.iterdir()
    else:
        quiz_path = file

    plugin_manager = PluginManager()
    for plugin_path in plugin_folders:
        plugin_manager.add_plugin(
            PluginManager.plugin_from_main_folder(plugin_path),
            activate=True
        )

    if quiz_path.exists():
        execute_quiz_as_cli_from_quiz_file(quiz_path, plugin_manager)
    else:
        print(f"No quiz found at {quiz_path}!")
