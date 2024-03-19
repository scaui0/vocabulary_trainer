import sys

from PyQt6.QtWidgets import QMainWindow, QGroupBox, QPushButton, QToolButton, QHBoxLayout, QApplication, QComboBox, \
    QVBoxLayout, QWidget
from themes import PrimaryPushButton, PushButton


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_group = QGroupBox("Buttons", self)
        self.buttons = [QPushButton, QToolButton, PushButton, PrimaryPushButton]

        layout = QHBoxLayout()
        for button_cls in self.buttons:
            button = button_cls(self)
            button.setText("Hallo")
            layout.addWidget(button)

        self.button_group.setLayout(layout)

        self.widget_state = QComboBox(self)
        self.widget_state.addItems(("Normal", "Disabled"))
        self.widget_state.currentIndexChanged.connect(self.set_state)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.button_group)
        main_layout.addWidget(self.widget_state)

        widget = QWidget(self)
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

    def set_state(self, index):
        self.button_group.setDisabled(index)


def main():
    app = QApplication([])
    window = Window()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
