from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class ConnectionLabel(QtWidgets.QLabel):
    def __init__(self, aParent, *args, **kwargs):
        QtWidgets.QLabel.__init__(self, aParent, *args, **kwargs)
        if aParent is not None:
            self.Logger = aParent.Logger
            self.DataBase = aParent.DataBase
        else:
            self.Logger = None
            self.DataBase = None
        self.DataBase.StatusLabel = self
        self.Connection(self.DataBase.Connected)

    def Connection(self, IsConnected):
        if IsConnected:
            self.setText("Connect")
            self.setStyleSheet("color : green;")
        else:
            self.setText("Disconnect")
            self.setStyleSheet("color : red;")
