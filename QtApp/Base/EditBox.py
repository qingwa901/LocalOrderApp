from PySide6 import QtCore, QtGui, QtWidgets
from QtApp.Base import CLineEdit


class eValueType:
    Float = 1
    Int = 2
    String = 3


class EditBox(CLineEdit):
    def __init__(self, aParent, aValueType):
        CLineEdit.__init__(self, aParent)
        self.ValueType = aValueType
        self.OpenKeyboardEvent = None
        self.Max = None
        self.Min = None

    def mousePressEvent(self, aEvent: QtGui.QMouseEvent):
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
            self.Logger.error(f'Error during clean {self.objectName()} value {self.text()}', exc_info=e)

    def value(self):
        if self.ValueType == eValueType.Int:
            try:
                return int(self.text())
            except Exception as e:
                self.Logger.error(f'can not convert ({self.text()}) to int', exc_info=e)
                return 0
        elif self.ValueType == eValueType.Float:
            try:
                return float(self.text())
            except Exception as e:
                self.Logger.error(f'can not convert ({self.text()}) to float', exc_info=e)
                return 0
        elif self.ValueType == eValueType.String:
            return self.text()
