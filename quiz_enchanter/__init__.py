from importlib.util import spec_from_file_location, module_from_spec
import json
from pathlib import Path

from tries import Tries

CURRENT_PATH = Path(__file__).parent


class Plugin:
    def __init__(self, quiz_types):
        self.registered_quiz_types = quiz_types

    @classmethod
    def from_main_folder(cls, path_to_main_folder):
        with open(Path(path_to_main_folder) / "extension.json", encoding="utf-8") as plugin_config_file:
            plugin_config = json.load(plugin_config_file)

            plugin_id = plugin_config["plugin_id"]

            plugin_main_file = Path(path_to_main_folder) / plugin_config["file"]

            # Load plugin_main_file as module into extension_modul
            spec = spec_from_file_location(plugin_main_file.stem, plugin_main_file)
            extension_modul = module_from_spec(spec)
            spec.loader.exec_module(extension_modul)

        return cls([])  # How to find QuizTypes in extension_modul?


class QuizType:
    def __init__(self, name, identifier=None):
        self.name = name
        self.identifier = identifier if identifier else name.lower()

    def __call__(self, cls):
        cls.name = self.name
        cls.identifier = self.identifier

        return cls


def main():
    print(
        Plugin.from_main_folder(
            CURRENT_PATH / "extensions/default_extension"
        )
    )


if __name__ == '__main__':
    main()
