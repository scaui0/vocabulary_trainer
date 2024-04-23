from datetime import datetime, time, date

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QComboBox, QLineEdit, QTimeEdit, QDateTimeEdit, QDateEdit

from quiz_enchanter import Plugin


plugin = Plugin("default")


@plugin.quiz_type("Select", "select")
class Select(QWidget):
    NAME = "Select"
    ID = "select"

    def __init__(self, question, options, right, parent=None):
        super().__init__(parent=parent)
        self.question = question
        self.options = options
        self.right = right

        self.combobox = QComboBox(self)
        self.combobox.addItems(options)

        self.question_label = QLabel(self.question, self)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.question_label)
        main_layout.addWidget(self.combobox)

        self.setLayout(main_layout)

    @classmethod
    def from_json(cls, json_data, parent=None):
        return cls(
            json_data["question"],
            json_data["options"],
            json_data["right"],
            parent
        )

    @property
    def is_right(self):
        return self.options[self.combobox.currentIndex()] == self.right


@plugin.quiz_type("Match", "match")
class Match(QLineEdit):
    NAME = "Match"
    ID = "match"

    def __init__(self, right, parent=None):
        super().__init__(parent=parent)
        self.right = right

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data["right"]
        )

    @property
    def is_right(self):
        return self.text() == self.right


@plugin.quiz_type("Time", "time")
class Time(QTimeEdit):
    NAME = "Time"
    ID = "time"

    def __init__(self, required_time, parent=None):
        super().__init__(parent=parent)

        self.required_time = required_time

    @classmethod
    def from_json(cls, json_data):
        return cls(
            time.fromisoformat(json_data["time"])
        )

    @property
    def is_right(self):
        return self.time() == self.required_time


@plugin.quiz_type("DateTime", "datetime")
class DateTime(QDateTimeEdit):
    NAME = "DateTime"
    Id = "datetime"

    def __init__(self, required_datetime, parent=None):
        super().__init__(parent=parent)

        self.required_datetime = required_datetime

    @classmethod
    def from_json(cls, json_data):
        return cls(
            datetime.fromisoformat(json_data["datetime"])
        )

    @property
    def is_right(self):
        return self.dateTime() == self.required_datetime


@plugin.quiz_type("Date", "date")
class Date(QDateEdit):
    NAME = "Date"
    Id = "date"

    def __init__(self, required_date, parent=None):
        super().__init__(parent=parent)

        self.required_date = required_date

    @classmethod
    def from_json(cls, json_data):
        return cls(
            date.fromisoformat(json_data["date"])
        )

    @property
    def is_right(self):
        return self.date() == self.required_date
