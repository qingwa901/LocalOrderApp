from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class CTableWidget(QtWidgets.QTableWidget):
    def __init__(self, aParent,  *args, **kwargs):
        QtWidgets.QTableWidget.__init__(self, parent=aParent, *args, **kwargs)
        if aParent is not None:
            self.Logger = aParent.Logger
            self.DataBase = aParent.DataBase

    def AbsX(self):
        return self.x() + self.parent().AbsX()

    def AbsY(self):
        return self.y() + self.parent().AbsY()

    def SetBackgoundColor(self, aColor):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'background-color: {aColor};')
