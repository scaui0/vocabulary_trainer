import sys

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, FluentIcon, Theme, NavigationItemPosition

from settings.gui import Settings, ColorSetting
from settings.gui.theme_settings import ThemeSetting, ThemeColorSetting

app = QApplication([])

window = FluentWindow()
window.setWindowTitle("Settings Test")
widget = Settings(FluentIcon.PALETTE, "Theme",
                  ThemeSetting(None, Theme.LIGHT),
                  ThemeColorSetting(window, QColor(0, 0, 0)))

window.addSubInterface(widget, FluentIcon.SETTING, "Settings", NavigationItemPosition.BOTTOM)
window.show()

sys.exit(app.exec())
