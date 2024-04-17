import importlib.util
import json
from functools import wraps
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout

from tries import Tries


class QuizNotExistsError(BaseException):
    def __str__(self):
        return f"{self.__class__.__name__}: The Quiz {self.args[0]!r} not exists!"


class QuizType:

    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier

    def __call__(self, func_or_class):
        @wraps(func_or_class)
        def helper(*args, **kwargs):
            return func_or_class(*args, **kwargs)

        return helper

    def __str__(self):
        return f"<QuizType {self.identifier!r}>"


def get_quiz_by_id(quizzes, expected_identifier):
    return {quiz.identifier: quiz for quiz in quizzes}[expected_identifier]


class Plugin:
    def __init__(self, path_to_main_folder):
        with open(Path(path_to_main_folder) / "extension.json", encoding="utf-8") as plugin_config_file:
            plugin_config = json.load(plugin_config_file)

            self.name = plugin_config["name"]
            self.plugin_main_file = Path(path_to_main_folder) / plugin_config["file"]

            # Load plugin_main_file as module into extension_modul
            spec = importlib.util.spec_from_file_location(self.plugin_main_file.stem, self.plugin_main_file)
            extension_modul = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(extension_modul)

            self.registered_quiz_types = [
                getattr(extension_modul, type_data["class"])
                for type_data in plugin_config["quiz_types"]  # TODO code again
            ]


class QuizWidget(QMainWindow):
    def __init__(self, quizzes):
        super().__init__()

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(quizzes[0])

    @classmethod
    def from_json(cls, json_data, plugins):
        all_quiz_types = sum([plugin.registered_quiz_types for plugin in plugins], [])



        print(all_quiz_types)
        print(json_data["quizzes"][0]["type"])
        quizzes = [all_quiz_types[quiz_data["type"]]
                   for quiz_data in json_data["quizzes"]]

        return cls(quizzes=quizzes)


def main():
    app = QApplication([])

    with open("quiz.json", encoding="utf-8") as file:
        window = QuizWidget.from_json(json.load(file), [
            Plugin(Path(__file__).parent / "extensions/default_extension")
        ])

    window.show()

    app.exec()


if __name__ == '__main__':
    main()
