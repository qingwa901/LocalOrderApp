from PySide6 import QtCore, QtGui, QtWidgets
from QtApp.Base import CLineEdit
from .KeyboardActive import popup_keyboard

BlockPanel = None
NumberKeyBoard = None


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
        if self.ValueType == eValueType.String:
            self.ShowWordKeyBoard(aEvent)
        else:
            self.ShowNumberKeyBoard()

    def ShowNumberKeyBoard(self):
        try:
            width = 300
            height = 300
            if NumberKeyBoard is not None and BlockPanel is not None:
                NumberKeyBoard.OriValue = self.text()
                NumberKeyBoard.setTarget(self)
                NumberKeyBoard.setVisible(True)
                NumberKeyBoard.resize(width, height)
                NumberKeyBoard.raise_()
                NumberKeyBoard.focusWidget()

                BlockPanel.setVisible(True)
                BlockPanel.Resize()
                BlockPanel.lower()
                BlockPanel.stackUnder(NumberKeyBoard)
                BlockPanel.mousePressEvent = lambda x: self.CloseNumberKeyBoard()
        except Exception as e:
            self.Logger.error(f'Error during open number keyboard window', exc_info=e)

    def CloseNumberKeyBoard(self):
        try:
            if NumberKeyBoard.target is not None:
                NumberKeyBoard.target.clean(NumberKeyBoard.OriValue)
                NumberKeyBoard.target.clearFocus()
                NumberKeyBoard.OriValue = None
            NumberKeyBoard.removeTarget()
            NumberKeyBoard.setVisible(False)
            BlockPanel.setVisible(False)

        except Exception as e:
            self.Logger.error(f'Error during close jump window', exc_info=e)

    def ShowWordKeyBoard(self, aEvent):
        try:
            if BlockPanel is not None:
                BlockPanel.setVisible(True)
                BlockPanel.Resize()
                BlockPanel.raise_()
                BlockPanel.mousePressEvent = self.CloseWordKeyBoard
                popup_keyboard(aEvent)
        except Exception as e:
            self.Logger.error(f'Error during open word keyboard window', exc_info=e)

    def CloseWordKeyBoard(self, aEvent):
        try:
            popup_keyboard(aEvent)
            if BlockPanel is not None:
                BlockPanel.setVisible(False)
        except Exception as e:
            self.Logger.error(f'Error during close word keyboard window', exc_info=e)

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
