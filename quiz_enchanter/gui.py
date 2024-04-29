import json
import sys
from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QStackedWidget, QPushButton, QWidget

from quiz_enchanter import quiz_type_by_id, PluginManager

CURRENT_PATH = Path(__file__).parent


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        manager = PluginManager.plugin_from_main_folder(
            CURRENT_PATH / "extensions/default_extension"
        )

        self.quiz_widget = QStackedWidget(self)

        self.current_quiz_index = 0
        with open(CURRENT_PATH / "quiz.json", encoding="utf-8") as file:
            for json_data in json.load(file)["quizzes"]:
                quiz = quiz_type_by_id(json_data["type"]).from_json(json_data)
                self.quiz_widget.addWidget(quiz)


        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.quiz_widget)
        self.main_layout.addWidget(QPushButton("Next", self,
                                               clicked=lambda: self.quiz_widget.setCurrentIndex(self.quiz_widget.currentIndex()+1)
                                               )
                                   )

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)



def main():
    app = QApplication([])

    window = Window()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
