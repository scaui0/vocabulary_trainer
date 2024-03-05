from abc import abstractmethod, ABCMeta
from typing import Any

from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import LineEdit, SpinBox, SwitchButton, FluentIcon, \
    SettingCard, ExpandGroupSettingCard, ColorPickerButton

from settings import Setting, CorrectionError
from settings.validators import StringValidator, IntegerValidator, BooleanValidator
from tools import LabeledWidget


class GUISettingMeta(ABCMeta, type(QWidget)):
    pass


class GUISetting(Setting, SettingCard, metaclass=GUISettingMeta):
    def __init__(self, parent: QWidget | None,
                 value: Any,
                 display_name: str,
                 name: str | None = None,
                 description: str = ""):

        QWidget.__init__(self, parent)
        super().__init__(value, display_name, name, description)

        self.value_changed()

        self.setObjectName(self.name)

        self.widget = None
        self.init_widget()

    def _set_value(self, value=None):
        """Please use 'value = None'

        Sets the value attribut of self to value if available, else to self.current_value, which can be overridden"""
        if value is None:
            self.value = self.current_value
        else:
            self.value = value
        print(f"Current value: {self.value}")

    @abstractmethod
    def init_widget(self):
        """Sets the widget content on self"""
        pass

    @property
    def current_value(self):
        return self.value


class GUIStringSetting(GUISetting, StringValidator):
    def init_widget(self):
        layout = QVBoxLayout()
        self.widget = LineEdit(self)
        self.widget.returnPressed.connect(self._set_value)
        layout.addWidget(
            LabeledWidget(self.display_name, self.widget, parent=self)
        )
        self.setLayout(layout)

    @property
    def current_value(self):
        return self.widget.text()


class GUIIntegerSetting(GUISetting, IntegerValidator):
    def init_widget(self):
        layout = QVBoxLayout()
        self.widget = SpinBox(self)
        self.widget.valueChanged.connect(self._set_value)
        layout.addWidget(
            LabeledWidget(self.display_name, self.widget, parent=self)
        )
        self.setLayout(layout)

    @property
    def current_value(self):
        return self.widget.text()


class GUIBooleanSetting(GUISetting, BooleanValidator):
    def __init__(self, parent: QWidget | None,
                 value: Any,
                 display_name: str,
                 name: str | None = None,
                 description: str = "",
                 on_text: str = "On",
                 off_text: str = "Off"):
        self.on_text = on_text
        self.off_text = off_text
        super().__init__(parent, value, display_name, name, description)

    def init_widget(self):
        layout = QVBoxLayout()
        self.widget = SwitchButton(self)
        self.widget.setOnText(self.on_text)
        self.widget.setOffText(self.off_text)

        self.widget.checkedChanged.connect(self._set_value)
        layout.addWidget(
            LabeledWidget(self.display_name, self.widget, parent=self)
        )
        self.setLayout(layout)

    @property
    def current_value(self):
        return self.widget.isChecked()


class ColorSetting(GUISetting):
    def __init__(self, parent: QWidget | None,
                 value: Any,
                 display_name: str,
                 name: str | None = None,
                 description: str = ""):
        super().__init__(parent, value, display_name, name, description)

    def init_widget(self):
        self.widget = ColorPickerButton(self.value, self.display_name, self)
        self.widget.colorChanged.connect(self._set_value)

        layout = QVBoxLayout()
        layout.addWidget(
            LabeledWidget(self.display_name, self.widget, parent=self)
        )
        self.setLayout(layout)

    def validate(self, value) -> bool:
        return isinstance(value, QColor)

    def correct(self, value) -> Any:
        try:
            return QColor(value)
        except (TypeError, OverflowError):
            raise CorrectionError


class Settings(ExpandGroupSettingCard):
    def __init__(self, icon: str | QIcon | FluentIcon, title: str, *settings: GUISetting):
        super().__init__(icon, title)

        [self.addGroupWidget(setting) for setting in settings]
        self.setObjectName(str(hash(settings)))
