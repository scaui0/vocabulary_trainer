import sys
from importlib.util import spec_from_file_location, module_from_spec
import json
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from .tries import Tries

CURRENT_PATH = Path(__file__).parent


class PluginNotRegisteredError(BaseException):
    pass


PLUGINS = {}


class Plugin:
    def __init__(self, identifier):
        self.identifier = identifier
        self.quiz_types = {}

        PLUGINS[identifier] = self

    def quiz_type(self, name, identifier):
        def helper(func):
            self.quiz_types[identifier] = func
            return func

        return helper


class PluginManager:
    def __init__(self, plugins):
        self.activated_plugins = plugins
        self.deactivated_plugins = []

    @property
    def quiz_types(self):
        return sum([p.quiz_types for p in self.activated_plugins], [])

    @staticmethod
    def plugin_from_main_folder(path_to_main_folder):
        with open(Path(path_to_main_folder) / "extension.json", encoding="utf-8") as plugin_config_file:
            plugin_config = json.load(plugin_config_file)

            plugin_id = plugin_config["id"]

            plugin_main_file = Path(path_to_main_folder) / plugin_config["file"]

            # Load plugin_main_file as module into extension_modul
            spec = spec_from_file_location(plugin_main_file.stem, plugin_main_file)
            extension_modul = module_from_spec(spec)
            # Execute modul
            spec.loader.exec_module(extension_modul)

        return PLUGINS[plugin_id]



def quiz_type_by_id(expected_identifier):
    return {
        identifier: quiz_type
        for plugin in PLUGINS.values()
        for identifier, quiz_type in plugin.quiz_types.items()
    }[expected_identifier]


def main():
    manager = PluginManager.plugin_from_main_folder(
        CURRENT_PATH / "extensions/default_extension"
    )

    app = QApplication([])
    widget = quiz_type_by_id("select")("1+1=", "1 2 3 4".split(" "), "2")
    widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
