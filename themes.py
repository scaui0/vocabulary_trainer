import sys
from dataclasses import dataclass
from functools import partial

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainterPath, QPainter, QColor, QPen
from PyQt6.QtWidgets import QApplication, QPushButton, QStyle, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout


def get_style_property(style: QStyle, name, default=None):
    value = style.property(name)
    return value if value is not None else default


@dataclass
class SimpleColor:
    normal: QColor
    disabled: QColor
    focus: QColor

    def __init__(self, normal, disabled, focus):
        self.normal = QColor(normal)
        self.disabled = QColor(disabled)
        self.focus = QColor(focus)


class ButtonColors:
    """

    button_color.background
    """

    def __init__(self, style: QStyle, background: SimpleColor, foreground: SimpleColor, ring: SimpleColor):
        self.background = None
        self.default_background = background
        self.default_foreground = foreground
        self.default_ring = ring


class PushButtonBase(QPushButton):
    ROUND = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_colors()

    def setStyleSheet(self, style_sheet):
        super().setStyleSheet(style_sheet)

        self.load_colors()

    def load_colors(self):
        blue = "#3574F0"
        white = "#fff"

        style = self.style()

        self.background = SimpleColor(
            get_style_property(style, "background-color", blue),
            get_style_property(style, "disabled-background-color", "#6C7AA5"),
            get_style_property(style, "selected-background-color", blue)
        )

        self.foreground = SimpleColor(
            get_style_property(style, "foreground-color", white),
            get_style_property(style, "disabled-foreground-color", white),
            get_style_property(style, "selected-foreground-color", white)
        )

        self.ring = SimpleColor(
            get_style_property(style, "ring-color", blue),
            get_style_property(style, "disabled-ring-color", blue),
            get_style_property(style, "selected-ring-color", blue)
        )

    def current_color_of(self, color):
        if self.hasFocus():
            return color.focus
        elif self.isEnabled():
            return color.normal
        else:
            return color.disabled

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        background = self.current_color_of(self.background)
        foreground = self.current_color_of(self.foreground)
        ring = self.current_color_of(self.ring)

        if self.hasFocus() or self.isDown():
            margin = 2
            rect = self.rect().adjusted(margin, margin, -margin, -margin)
        else:
            rect = self.rect()

        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), self.ROUND, self.ROUND)

        painter.fillPath(path, background)

        painter.setPen(foreground)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())

        self.paint_ring(painter, ring, 2)

    def paint_ring(self, painter, color, width):
        pen = QPen(color)
        pen.setWidth(width)
        painter.setPen(pen)
        painter.drawRoundedRect(QRectF(self.rect()), self.ROUND, self.ROUND)


class PrimaryPushButton(PushButtonBase):
    pass


class PushButton(PushButtonBase):
    def load_colors(self):
        blue = "#3574F0"
        white = "#fff"
        black = "#000"
        grey = "#b5b5b5"

        style = self.style()

        self.background = SimpleColor(
            get_style_property(style, "background-color", white),
            get_style_property(style, "disabled-background-color", "#333"),
            get_style_property(style, "selected-background-color", white)
        )

        self.foreground = SimpleColor(
            get_style_property(style, "foreground-color", black),
            get_style_property(style, "disabled-foreground-color", black),
            get_style_property(style, "selected-foreground-color", black)
        )

        self.ring = SimpleColor(
            get_style_property(style, "ring-color", grey),
            get_style_property(style, "disabled-ring-color", grey),
            get_style_property(style, "selected-ring-color", blue)
        )


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        BUTTONS = (
            (PushButton("Cancel"), PrimaryPushButton("Ok")),
            (PushButton("Cancel"), PushButton("Discard"), PrimaryPushButton("Save")),
            (PushButton("Continue"), PushButton("Discard"), PushButton("Save in Cloud"),
             PrimaryPushButton("Select in other place"))
        )

        main_layout = QVBoxLayout()

        for buttons in BUTTONS:
            layout = QHBoxLayout(self)
            for button in buttons:
                layout.addWidget(button)
                button.clicked.connect(partial(self.print, button.text()))
            main_layout.addLayout(layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def print(self, *args):
        print(*args[:-1])


def main():
    app = QApplication([])
    widget = Window()

    widget.show()
    sys.exit(app.exec())




if __name__ == '__main__':
    main()
