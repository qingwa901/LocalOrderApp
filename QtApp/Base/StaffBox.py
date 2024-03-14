from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class Staffbox(QtWidgets.QComboBox):
    def __init__(self, aParent, *args, **kwargs):
        QtWidgets.QComboBox.__init__(self, aParent, *args, **kwargs)
        if aParent is not None:
            self.Logger = aParent.Logger
            self.DataBase = aParent.DataBase
        else:
            self.Logger = None
            self.DataBase = None
        self.addItems(self.DataBase.StaffList.keys())
        self.getStaffID(1)
        self.currentIndexChanged.connect(self.getStaffID)

    def getStaffID(self, index):
        self.DataBase.StaffName = self.currentText()
