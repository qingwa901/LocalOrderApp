# -*- coding: utf-8 -*-
import pandas as pd
from functools import partial
# Form implementation generated from reading ui file 'Ui/Menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets
from QtApp.MenuPage import MenuPage
from DataBase import FullMenuList
from Config import Config
from QtApp.Base import CFrame, CWidget, CPushButton


class Menu(CFrame):
    def __init__(self, aParant):
        CFrame.__init__(self, aParant)
        self.MenuENName = self.DataBase.Setting.GetValue(Config.ValueSetting.Manu.EN_NAME)
        self.MenuCNName = self.DataBase.Setting.GetValue(Config.ValueSetting.Manu.CN_NAME)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Menu")
        self.resize(546, 338)
        self.VLayout = QtWidgets.QVBoxLayout(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.VLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ButList = {}
        for i in self.MenuCNName:
            But = CPushButton(self)
            But.setObjectName("Btn" + self.MenuENName[i])
            self.horizontalLayout.addWidget(But)
            self.ButList[i] = But
            But.pressed.connect(partial(self.ActivePage, i))
        self.MenuPageList = {}
        self.PageLayout = QtWidgets.QVBoxLayout(self)
        self.VLayout.addLayout(self.PageLayout)
        for type in self.MenuENName:
            Page = MenuPage(self, self.MenuENName[type])
            self.MenuPageList[type] = Page
            self.PageLayout.addWidget(Page)
            # Page.setFrameShape(QtWidgets.QFrame.StyledPanel)
            # Page.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setLayout(self.VLayout)
        self.ActivePage(1)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def AddMenu(self, menu: FullMenuList):
        for m in menu.Foods.values():
            if m.Type in self.MenuPageList:
                self.MenuPageList[m.Type].AddMenu(m)

    def AddItems(self, data: pd.DataFrame):
        data.apply(self.AddItem, axis=1)

    def AddItem(self, data: pd.Series):
        self.MenuPageList[data['FoodType']].AddItem(data)

    def ActivePage(self, FoodType):
        for i in self.MenuPageList:
            if i == FoodType:
                self.MenuPageList[i].setVisible(True)
            else:
                self.MenuPageList[i].setVisible(False)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Menu"))
        for i in self.MenuCNName:
            self.ButList[i].setText(_translate("Form", self.MenuCNName[i]))

    def Connect(self, Event):
        for page in self.MenuPageList:
            self.MenuPageList[page].Connect(Event)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Menu(None)
    ui.setupUi()
    MenuItemList = pd.DataFrame([[0, 'Test1', '测试1', 1], [1, 'Test2', '测试2', 2]],
                                columns=['ID', 'FoodENName', 'FoodCNName', 'FoodType'])
    ui.AddItems(MenuItemList)
    ui.show()
    sys.exit(app.exec_())
