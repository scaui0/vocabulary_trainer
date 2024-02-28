import sys
from typing import Any

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QApplication, QMainWindow
from qfluentwidgets import SwitchButton, SubtitleLabel

from settings import Setting, BooleanSetting, IntegerSetting, StringSetting, FloatSetting


class LabeledWidget(QFrame):
    def __init__(self, text, widget: QWidget, parent=None):
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.label = SubtitleLabel(text, self)
        self.content = widget

        self.main_layout.addWidget(self.label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.content)
        self.setLayout(self.main_layout)


class GUISetting(Setting, QWidget):
    def __init__(self, parent, value: Any, display_name: str, name: str | None = None, description: str = ""):
        super().__init__(parent=parent, value=value, display_name=display_name, name=name, description=description)

    def set_value(self, value):
        self.value = value

    def init_widget(self):
        """Sets the widget content on self"""
        pass


class GUIBooleanSetting(BooleanSetting, GUISetting):
    def init_widget(self):
        widget = SwitchButton(self)
        widget.checkedChanged.connect(lambda x: self.set_value(x))

        layout = QHBoxLayout(self)
        layout.addWidget(LabeledWidget(self.display_name, widget, self))

        # self.setLayout(layout)


class GUIntegerSetting(IntegerSetting, GUISetting):
    pass


class GUIStringSetting(StringSetting, GUISetting):
    pass


class GUIFloatSetting(FloatSetting, GUISetting):
    pass


def main():
    app = QApplication([])
    window = QMainWindow()
    window.setCentralWidget(GUIntegerSetting(None, True, "Theme"))
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
