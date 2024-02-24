from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from Config import Config


class OrderType:
    Valid = 0
    RunOut = 1


class MenuBut(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)

    def setupUi(self, Menu):
        table = Config.DataBase.MenuList
        self.FoodID = Menu.ID
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setObjectName(Menu.NameEN)
        _translate = QtCore.QCoreApplication.translate
        self.setText(_translate("Form", Menu.NameCN))
        self.setVisible(True)
        self.setEnabled(True)

    def setupColor(self, OrderType):
        self.setAttribute(self.Qt.WA_StyledBackground, True)
        if OrderType == 0:
            self.setStyleSheet('background-color: white;')
        elif OrderType == 1:
            self.setStyleSheet('background-color: Gray;')

    def BindEvent(self, Event):
        self.pressed.connect(partial(Event, self.FoodID))

    def Clear(self):
        self.setObjectName('None')
        _translate = QtCore.QCoreApplication.translate
        self.setText(_translate("Form", ''))
        self.setEnabled(False)
        self.setVisible(False)
