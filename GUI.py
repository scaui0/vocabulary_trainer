import json
import sys
from os import PathLike

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QApplication

from main import Vocabularies


class VocabularyWidget(QWidget):
    def __init__(self, parent=None, path: PathLike | str = ""):
        super().__init__(parent)

        self.vocabulary = None
        with open(path) as file:
            self.vocabularies = Vocabularies.from_json(json.load(file)["entries"], False)

        self.vocabulary_label = QLabel("Label", self)
        self.vocabulary_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # noinspection PyArgumentList
        self.ok_button = QPushButton("OK", self, clicked=self.check_vocabulary)
        self.vocabulary_entry = QLineEdit(self)
        # noinspection PyUnresolvedReferences
        self.vocabulary_entry.returnPressed.connect(self.check_vocabulary)
        # noinspection PyArgumentList
        self.show_stats_button = QPushButton("Show Stats", self, clicked=self.show_stats)
        # noinspection PyArgumentList
        self.add_vocabulary_button = QPushButton("Add Vocabulary", self, clicked=self.add_vocabulary)

        self.show_result_label = QLabel("", self)
        self.show_result_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.side_layout = QVBoxLayout()
        self.side_layout.addWidget(self.add_vocabulary_button)
        self.side_layout.addWidget(self.show_stats_button)

        self.vocabulary_input_layout = QHBoxLayout()
        self.vocabulary_input_layout.addWidget(self.vocabulary_entry)
        self.vocabulary_input_layout.addWidget(self.ok_button)

        self.vocabulary_layout = QVBoxLayout()
        self.vocabulary_layout.addWidget(self.vocabulary_label)
        self.vocabulary_layout.addLayout(self.vocabulary_input_layout)
        self.vocabulary_layout.addWidget(self.show_result_label)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.side_layout)
        self.main_layout.addLayout(self.vocabulary_layout)

        self.setLayout(self.main_layout)

        self.new_vocabulary()

    def check_vocabulary(self):
        is_right = self.vocabularies.next_try(self.vocabulary_entry.text())
        text = ("Right" if is_right else "False",
                f"{self.vocabulary._tries_right}/{self.vocabulary.tries}",
                f"It would be {self.vocabulary._translations}" if not is_right else ""
                )
        self.show_result_label.setText(" ".join(text))
        self.vocabulary_entry.setText("")
        self.new_vocabulary()

    def show_stats(self):
        pass  # TODO

    def add_vocabulary(self):
        pass

    def new_vocabulary(self):
        self.vocabulary = self.vocabularies.get_new_vocabulary()
        self.vocabulary_label.setText(self.vocabulary.name)


def main():
    app = QApplication(["Vocabulary Trainer"])
    widget = VocabularyWidget(path="vocabularies_new.json")
    widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
