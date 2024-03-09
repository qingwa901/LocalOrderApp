from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QPixmap
from functools import partial


class eValueType:
    Float = 1
    Int = 2
    String = 3


class EditBox(QtWidgets.QLineEdit):
    def __init__(self, parent, ValueType, logger):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.logger = logger
        self.ValueType = ValueType
        self.OpenKeyboardEvent = None
        self.Max = None
        self.Min = None

    def focusInEvent(self, e: QtGui.QFocusEvent):
        if e.gotFocus() and e.reason().value != 3:
            if self.OpenKeyboardEvent is None:
                return
            else:
                self.OpenKeyboardEvent(self)

    def setMinimum(self, value):
        self.Min = value

    def setMaximum(self, value):
        self.Max = value

    def clean(self, value='0'):
        if value is None:
            value = '0'
        try:
            if self.ValueType == eValueType.Int:
                value = int(float(self.text()))
                if self.Max is not None:
                    value = min(self.Max, value)
                if self.Min is not None:
                    value = max(self.Min, value)
                self.setText(str(int(value)))
            elif self.ValueType == eValueType.Float:
                value = float(self.text())
                if self.Max is not None:
                    value = min(self.Max, value)
                if self.Min is not None:
                    value = max(self.Min, value)
                self.setText(str(round(value, 2)))
            elif self.ValueType == eValueType.String:
                return
        except Exception as e:
            self.setText(value)
            self.logger.error(f'Error during clean {self.objectName()} value {self.text()}', exc_info=e)
