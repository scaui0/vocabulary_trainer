import sys
from functools import partial
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QApplication, QLineEdit, QHBoxLayout, QPushButton, QLabel, QVBoxLayout, QMessageBox

sys.path.append(r"C:\Users\Scaui\PycharmProjects\vokabel_trainer")

from translator import Translator
from vocabulary_trainer import Vocabularies


def sequence_repr(sequence):
    if len(sequence) == 0:
        return repr(None)
    elif len(sequence) == 1:
        return repr(sequence[0])
    else:
        return repr(sequence)


class VocabularyAskingWidget(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        current_path = Path(__file__).parent

        self.translator = Translator(current_path / Path("translations"))

        self.vocabularies = Vocabularies.from_file(current_path / Path("testvokabeln.json"))
        self.current_source = None

        self.input_widget = QLineEdit(self, returnPressed=self.ok_clicked)
        self.ok_button = QPushButton("Ok", self, clicked=self.ok_clicked)
        self.skip_button = QPushButton("Skip", self, clicked=self.skip_clicked)
        self.global_stats = QLabel("<stats>", self)
        self.vocabulary_stats = QLabel("<vocabulary_stats>", self)

        self.source_label = QLabel("", self)

        self.vocabulary_fade_out_timer = QTimer(self)
        self.vocabulary_fade_out_timer.timeout.connect(partial(self.vocabulary_stats.setText, ""))

        layout = QHBoxLayout()

        layout.addWidget(self.input_widget)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.skip_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.global_stats)
        main_layout.addWidget(self.source_label)
        main_layout.addLayout(layout)
        main_layout.addWidget(self.vocabulary_stats)

        self.setLayout(main_layout)

        self.show_new_vocabulary()

    def tr(self, key: str) -> str:
        return self.translator.translate(key)

    def ok_clicked(self):
        self.next_vocabulary()

    def skip_clicked(self):
        self.next_vocabulary(is_skip=True)

    def next_vocabulary(self, is_skip=False):
        if not is_skip:
            name = self.input_widget.text()
            is_right, it_would = self.vocabularies.next_try(name)
            if is_right:
                text = self.tr("trainer.ask.response.right")
                self.vocabulary_stats.setText(text)
                self.vocabulary_fade_out_timer.start(1500)
                self.input_widget.setText("")

            else:
                QMessageBox.information(self,
                                        self.tr("trainer.ask.wrong"),
                                        self.tr("trainer.ask.response.wrong").format(sequence_repr(it_would))
                                        )
        else:  # Skip
            translation = self.vocabularies.skip()
            QMessageBox.information(
                self,
                self.tr("trainer.ask.skip"),
                self.tr("trainer.ask.response.skip").format(repr(self.current_source), sequence_repr(translation))
            )

        self.show_new_vocabulary()

    def show_new_vocabulary(self):
        self.current_source = self.vocabularies.get_new_vocabulary()
        self.source_label.setText(self.current_source)


def main():
    app = QApplication([])

    win = VocabularyAskingWidget()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
