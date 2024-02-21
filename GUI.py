from __future__ import annotations

import sys
from os import PathLike
from pathlib import Path

import platformdirs
import yaml
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QApplication, QVBoxLayout, QWidget
from qfluentwidgets import FluentIcon as Icons
from qfluentwidgets import (NavigationItemPosition, FluentWindow, SubtitleLabel, setFont, SwitchButton, setTheme, Theme,
                            ExpandGroupSettingCard, setThemeColor, CheckBox, PrimaryPushButton,
                            ColorPickerButton, MessageDialog)


class PlaceholderWidget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)

        # unique object name
        self.setObjectName(text.replace(' ', '-'))


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


def get_theme_from_bool(dark_mode):
    return [Theme.LIGHT, Theme.DARK][dark_mode]


def set_theme_from_bool(dark_mode: bool):
    setTheme(get_theme_from_bool(dark_mode))


class SettingBase(dict):
    def __init__(self, settings):
        super().__init__(settings)
        self.has_unsaved_changes = False


class FileBasedSettings(SettingBase):
    def __init__(self, path: PathLike | str):
        with open(path) as file:
            super().__init__(yaml.safe_load(file))
        self.path = path

        self._refactor_settings()

    def save(self):
        with open(self.path, "w") as file:
            yaml.safe_dump(self._to_dict(), file)

    def _refactor_settings(self):
        pass

    def _to_dict(self) -> dict:
        pass


class Settings(FileBasedSettings):
    def _refactor_settings(self):
        self["theme_color"] = QColor(self["theme_color"])
        self["theme"] = Theme(self["theme"])

    def _to_dict(self) -> dict:
        return dict(
            theme=self["theme"].value,
            theme_color=self["theme_color"].rgb()
        )


class VocabularyAskingWidget(QFrame):
    def __init__(self):
        super().__init__()
        uic.loadUi("vocabulary_trainer.ui", self)



class SettingInterface(QFrame):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        self.settings = Settings(platformdirs.user_data_path(
            "Vocabulary Trainer", "_Scaui", ensure_exists=True) / Path("settings.yml"))

        self.auto_theme = CheckBox(self)
        self.auto_theme.clicked.connect(self.auto_theme_switched)

        self.theme_switcher = SwitchButton(self)
        self.theme_switcher.setOnText("Dark Mode")
        self.theme_switcher.setOffText("Light Mode")
        self.theme_switcher.checkedChanged.connect(self.settings_switched)

        self.color_pickler = ColorPickerButton(QColor(255, 0, 0), "Select Theme color")
        self.color_pickler.colorChanged.connect(self.settings_switched)

        self.save_change_button = PrimaryPushButton(self)
        self.save_change_button.setText("Save changes")
        self.save_change_button.clicked.connect(self.save_changes)

        self.color_group = ExpandGroupSettingCard(Icons.PALETTE, "Theme")
        self.color_group.addGroupWidget(LabeledWidget("Auto theme", self.auto_theme, self))
        self.color_group.addGroupWidget(LabeledWidget("Theme", self.theme_switcher, self))
        self.color_group.addGroupWidget(LabeledWidget("Theme color", self.color_pickler, self))

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.color_group)
        self.main_layout.addWidget(self.save_change_button, alignment=Qt.AlignmentFlag.AlignBottom)

        self.setObjectName(text.replace(' ', '-'))

        self.load_and_set_settings()

    def load_and_set_settings(self):
        setTheme(self.settings["theme"])
        if self.settings["theme"] == Theme.AUTO:
            self.auto_theme.setChecked(True)
            self.theme_switcher.setDisabled(True)
        else:
            self.theme_switcher.setChecked(self.settings["theme"] == Theme.DARK)

        self.color_pickler.setColor(self.settings["theme_color"])
        setThemeColor(self.settings["theme_color"])

    def auto_theme_switched(self):
        checked = self.auto_theme.isChecked()
        self.theme_switcher.setDisabled(checked)
        self.save_change_button.setDisabled(False)

        if checked:
            setTheme(Theme.AUTO)
            self.settings["theme"] = Theme.AUTO
        else:
            set_theme_from_bool(self.theme_switcher.isChecked())

    def settings_switched(self, arg):
        if arg is not None:
            if isinstance(arg, QColor):
                setThemeColor(arg)
                self.settings["theme_color"] = arg
            elif isinstance(arg, bool):
                setTheme(get_theme_from_bool(arg))
                self.settings["theme"] = get_theme_from_bool(arg)

        self.save_change_button.setDisabled(False)

    def save_changes(self):
        message_box = MessageDialog("Are you sure?", "Are you sure to save these changes?", self)
        if not message_box.exec():
            return

        self.settings["theme"] = Theme.AUTO if self.auto_theme.isChecked() \
            else get_theme_from_bool(self.theme_switcher.isChecked())
        self.settings["theme_color"] = self.color_pickler.color
        self.settings.save()

        self.save_change_button.setDisabled(True)


class Window(FluentWindow):

    def __init__(self):
        super().__init__()

        self.homeInterface = PlaceholderWidget('Home Interface', self)
        self.musicInterface = PlaceholderWidget('Music Interface', self)
        self.videoInterface = PlaceholderWidget('Video Interface', self)
        self.albumInterface = PlaceholderWidget('Album Interface', self)
        self.albumInterface1 = PlaceholderWidget('Album Interface 1', self)

        self.asking_interface = VocabularyAskingWidget()
        self.settingInterface = SettingInterface("Settings", self)

        self.init_navigation()
        self.init_window()

    def init_navigation(self):
        self.addSubInterface(self.homeInterface, Icons.HOME, 'Home')
        self.addSubInterface(self.asking_interface, Icons.QUESTION, "Ask Vocabularies")
        self.addSubInterface(self.musicInterface, Icons.MUSIC, 'Music library')
        self.addSubInterface(self.videoInterface, Icons.VIDEO, 'Video library')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.albumInterface, Icons.ALBUM, 'Albums', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.albumInterface1, Icons.ALBUM, 'Album 1', parent=self.albumInterface)

        self.addSubInterface(self.settingInterface, Icons.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def init_window(self):
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
