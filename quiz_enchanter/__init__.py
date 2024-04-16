from functools import wraps

from PyQt6.QtWidgets import QWidget, QApplication

from tries import Tries


class QuizType:
    registered_types = {}

    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier

    def __call__(self, func_or_class):
        def helper(*args, **kwargs):
            return func_or_class(*args, **kwargs)
        wraps(helper, func_or_class)

        QuizType.registered_types[self.identifier] = func_or_class
        return helper


class Plugin:
    def __init__(self, name, quiz_types):
        self.name = name
        self.quiz_types = quiz_types


def main():
    app = QApplication([])

    window = QWidget()
    window.show()

    app.exec()

if __name__ == '__main__':
    main()
