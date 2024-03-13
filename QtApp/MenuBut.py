from PySide6 import QtCore, QtGui, QtWidgets
from functools import partial
from Config import Config
from QtApp.Base import CPushButton


class OrderType:
    Valid = 0
    RunOut = 1


class MenuBut(CPushButton):
    def __init__(self, parent):
        CPushButton.__init__(self, parent)

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
        if OrderType == 0:
            self.SetBackgoundColor('white')
        elif OrderType == 1:
            self.SetBackgoundColor('Gray')

    def BindEvent(self, Event):
        self.pressed.connect(partial(Event, self.FoodID))

    def Clear(self):
        self.setObjectName('None')
        _translate = QtCore.QCoreApplication.translate
        self.setText(_translate("Form", ''))
        self.setEnabled(False)
        self.setVisible(False)
