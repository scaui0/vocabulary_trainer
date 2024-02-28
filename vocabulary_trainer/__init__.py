import json
from abc import abstractmethod
from pathlib import Path

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import PushButton, LineEdit

from vocabulary_trainer.vocabularies import VocabularyList


def not_implement():
    print("Not yet implement. Coming soon")


def input_(prompt) -> str:
    answer = input(prompt)
    if answer == "e":
        raise KeyboardInterrupt("Thanks for using")
    return answer


class AskerBase:
    def __init__(self, path, *args, **kwargs):
        with open(path, encoding="utf-8") as file:
            self.vocabularies = VocabularyList.from_json(json.load(file))

        self.current_vocabulary_name = self.get_new_vocabulary()

    def get_new_vocabulary(self):
        return self.vocabularies.get_new_vocabulary()

    def skip(self):
        pass

    def ok(self):
        name = self.get_vocabulary_name()
        self.show_result(self.vocabularies.next_try(name))

        self.current_vocabulary_name = self.get_new_vocabulary()
        self.show_new_vocabulary(self.current_vocabulary_name)

    @abstractmethod
    def show_help(self):
        """Shows some help

        Must be overridden by the inherited.
        """

    @abstractmethod
    def show_new_vocabulary(self, vocabulary):
        """Shows the vocabulary

        Must be overridden by the inherited.
        """

    @abstractmethod
    def run(self):
        """Runs the mainloop

        Must be overridden by the inherited.
        The method shouldn't be leaved to main prozess
        """

    @abstractmethod
    def get_vocabulary_name(self):
        """Shout return the name of a vocabulary, which the user gave in

        Must be overridden by the inherited.
        """

    @abstractmethod
    def show_result(self, result):
        """Shows the result of the input

        Must be overridden by the inherited.
        """


class CommandLineAsker(AskerBase):
    def __init__(self, path):
        super().__init__(path)

    def show_help(self):
        pass

    def show_new_vocabulary(self, vocabulary):
        pass

    def get_vocabulary_name(self):
        return input_(f"Translated name of {self.current_vocabulary_name!r}: ")

    def show_result(self, result):
        print("Right" if result[0] else "False",
              f"\nIt would be {result[1]}" if not result[0] else "")

    def run(self):
        while True:
            self.ok()


class GUIAsker(AskerBase, QWidget):
    def __init__(self, path, parent=None):
        super().__init__(path=path, parent=parent)

        self.ok_button = PushButton("Ok", self)
        self.ok_button.clicked.connect(self.ok)
        self.vocabulary_input = LineEdit(self)

        layout = QHBoxLayout(self)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.vocabulary_input)

        self.setLayout(layout)

    def show_help(self):
        pass
        # messagebox.help()

    def show_new_vocabulary(self, vocabulary):
        pass
        # self.vocabulary_name.setText(vocabulary)

    def get_vocabulary_name(self):
        pass
        # return self.line.text()

    def show_result(self, result):
        pass
        # self.result_label.setText(result)

    def run(self):
        pass
        # self.ok_button.clicked.connect(self.ok)
        # exec()


def main():
    asker = CommandLineAsker(Path(__file__).parent.parent / Path("testvokabeln.json"))
    asker.run()


if __name__ == '__main__':
    main()
