from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QHBoxLayout, QFrame, QWidget
from qfluentwidgets import BodyLabel


class LabeledWidget(QFrame):
    def __init__(self, text, widget: QWidget | None, parent=None):
        super().__init__(parent)
        self.content = widget
        self.main_layout = QHBoxLayout(self)
        self.label = BodyLabel(text, self)

        self.label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed,
                                                       QtWidgets.QSizePolicy.Policy.Minimum))

        self.main_layout.addWidget(self.label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.content)
        self.setLayout(self.main_layout)
