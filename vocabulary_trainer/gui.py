import sys

from PyQt6.QtWidgets import QWidget, QApplication, QLineEdit, QHBoxLayout, QPushButton, QLabel, QVBoxLayout


class VocabularyAskingWidget(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.


        self.input_widget = QLineEdit(self, returnPressed=self.ok_clicked)
        self.ok_button = QPushButton("Ok", self, clicked=self.ok_clicked)
        self.skip_button = QPushButton("Skip", self, clicked=self.skip_clicked)
        self.global_stats = QLabel("<stats>", self)
        self.vocabulary_stats = QLabel("<vocabulary_stats>", self)




        layout = QHBoxLayout()

        layout.addWidget(self.input_widget)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.skip_button)


        main_layout = QVBoxLayout()
        main_layout.addWidget(self.global_stats)
        main_layout.addLayout(layout)
        main_layout.addWidget(self.vocabulary_stats)

        self.setLayout(main_layout)


    def ok_clicked(self):
        print("Ok")

    def skip_clicked(self):
        print("Skip")


def main():
    app = QApplication([])

    win = VocabularyAskingWidget()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
