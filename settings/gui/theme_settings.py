from typing import Any

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import Theme, setTheme, setThemeColor

from settings.gui import GUIBooleanSetting, ColorSetting


class ThemeSetting(GUIBooleanSetting):
    def __init__(self, parent: QWidget | None, value: bool | Theme):
        if isinstance(value, Theme):
            value = value == Theme.DARK
        super().__init__(parent, value, "Theme", "theme", "The theme of the application", "Dark", "Light")

        self.value_changed()

    def value_changed(self):
        setTheme(Theme.DARK if self.value else Theme.LIGHT)


class ThemeColorSetting(ColorSetting):
    def __init__(self, parent: QWidget | None, value: QColor):
        super().__init__(parent, value, "Theme color", "theme_color", "The theme color of the application")

    def value_changed(self):
        setThemeColor(self.value)
