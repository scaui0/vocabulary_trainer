from importlib.util import spec_from_file_location, module_from_spec
import json
from pathlib import Path

from .tries import Tries

CURRENT_PATH = Path(__file__).parent


class PluginNotRegisteredError(Exception):
    pass


class QuizType:
    def __init__(self, name, identifier, gui=None, cli=None, gui_builder=None):
        self.name = name
        self.identifier = identifier

        self._gui = gui
        self._cli = cli
        self._gui_builder = gui_builder

    def gui(self, func):
        self._gui = func
        return func

    def cli(self, func):
        self._cli = func
        return func

    def gui_builder(self, func):
        self._gui_builder = func
        return func



class Plugin:
    def __init__(self, identifier):
        self.identifier = identifier
        self.quiz_types = {}

        PluginManager.PLUGINS[identifier] = self

    def quiz_type(self, name, identifier):
        quiz_type = QuizType(name, identifier)

        self.quiz_types[identifier] = quiz_type
        return quiz_type



class PluginManager:
    PLUGINS = {}
    ACTIVE_PLUGINS = {}
    DEACTIVATED_PLUGINS = {}

    @classmethod
    def plugin_from_main_folder(cls, path_to_main_folder):
        with open(Path(path_to_main_folder) / "extension.json", encoding="utf-8") as plugin_config_file:
            plugin_config = json.load(plugin_config_file)

            plugin_id = plugin_config["id"]

            plugin_main_file = Path(path_to_main_folder) / plugin_config["file"]

            # Load plugin_main_file as module into extension_modul
            spec = spec_from_file_location(plugin_main_file.stem, plugin_main_file)
            extension_modul = module_from_spec(spec)
            # Execute modul
            spec.loader.exec_module(extension_modul)

        return cls.PLUGINS[plugin_id]  # The Plugin is already registered.

    @classmethod
    @property
    def all_quiz_types(cls):
        return {
            identifier: quiz_type
            for plugin in cls.PLUGINS.values()
            for identifier, quiz_type in plugin.quiz_types.items()
        }




def main():
    manager = PluginManager.plugin_from_main_folder(
        CURRENT_PATH / "extensions/default_extension"
    )

    print(PluginManager.all_quiz_types)


if __name__ == '__main__':
    main()
