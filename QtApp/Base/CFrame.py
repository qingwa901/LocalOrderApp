from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class CFrame(QtWidgets.QFrame):
    def __init__(self, aParent,  *args, **kwargs):
        QtWidgets.QFrame.__init__(self, aParent,  *args, **kwargs)
        if aParent is not None:
            self.Logger = aParent.Logger
            self.DataBase = aParent.DataBase
        else:
            self.Logger = None
            self.DataBase = None

    def AbsX(self):
        return self.x() + self.parent().AbsX()

    def AbsY(self):
        return self.y() + self.parent().AbsY()

    def SetBackgoundColor(self, aColor):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'background-color: {aColor};')
