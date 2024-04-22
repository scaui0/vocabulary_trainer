from datetime import datetime, time, date

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QComboBox, QLineEdit, QTimeEdit, QDateTimeEdit, QDateEdit

from quiz_enchanter import QuizType


@QuizType("Select", "select")
class Select(QWidget):
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


@QuizType("Match", "match")
class Match(QLineEdit):
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


@QuizType("Time", "time")
class Time(QTimeEdit):
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


@QuizType("Datetime", "datetime")
class DateTime(QDateTimeEdit):
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


@QuizType("Date", "date")
class Date(QDateEdit):
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

print(Plugin.plugins)
