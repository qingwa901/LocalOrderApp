# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui/MenuPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets
import pandas as pd
from functools import partial
from QtApp.MenuBut import MenuBut


class MenuPage(QtWidgets.QFrame):
    def __init__(self, parent, Name='MenuPage'):
        QtWidgets.QFrame.__init__(self, parent)
        self.Name = Name
        self.ButList = []
        self.Count = 0
        self.gridSize = 5
        self.setupUi()

    def setupUi(self):
        self.setObjectName(self.Name)
        self.resize(400, 300)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 10, 391, 281))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def AddMenu(self, data):
        if self.Count >= len(self.ButList):
            But = MenuBut(self.gridLayoutWidget)
            self.ButList.append(But)
            self.gridLayout.addWidget(But, self.Count // self.gridSize, self.Count % self.gridSize, 1, 1)
        else:
            But = self.ButList[self.Count]
        self.Count += 1
        But.setupUi(data)

    def AddItem(self, data: pd.Series):
        But = QtWidgets.QPushButton(self.gridLayoutWidget)
        But.setObjectName(data['FoodENName'])
        self.ButList.append(But)
        self.gridLayout.addWidget(But, self.Count // self.gridSize, self.Count % self.gridSize, 1, 1)
        self.Count += 1
        But.setText(self._translate("Form", data['FoodCNName']))

    def retranslateUi(self):
        self._translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(self._translate("Form", "MenuPage"))

    def Connect(self, Event):
        for btn in self.ButList:
            btn.BindEvent(Event)

    def Clear(self):
        for btn in self.ButList:
            btn.Clear()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MenuPage(None)
    ui.setupUi()
    ui.show()
    sys.exit(app.exec_())
