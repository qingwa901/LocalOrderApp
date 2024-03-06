# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui/Main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets
from QtApp.Tables import TablesPanel
from QtApp.SettingPanel import SettingPanel
from QtApp.InitialTable import InitialTable
from QtApp.Menu import Menu
from QtApp.Status import StatusPanel
from QtApp.OrderList import OrderListPanel
from QtApp.JumpWindow import JumpWindow
from QtApp.FinalStatus import FinalStatusPanel
from QtApp.receiptPanel import Receipt
from DataBase import DataBase
from Logger import CreateLogger
from Config import Config
from datetime import datetime
from TableInfoStore import OrderInfo


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.Logger = CreateLogger('Zhangji', 'TmpLog')
        self.DataBase = DataBase(self.Logger, 'DataBase')
        self.TableOrder = self.DataBase.Setting.GetValue(Config.DataBase.StoreList.TABLE_ORDER)
        self.TableNumber = None
        try:
            self.setupUi()
        except Exception as e:
            self.DataBase.open = False
            self.DataBase.Setting.open = False
            raise e
        self.StaffID = 1

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1121, 679)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setStyleSheet("border: 3px solid blue;")
        self.centralwidget.setObjectName("centralwidget")
        self.SettingPanel = SettingPanel(self.centralwidget)
        self.SettingPanel.setVisible(False)

        self.JumpWindow = JumpWindow(self.centralwidget)
        self.JumpWindow.setVisible(False)

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.TablePanel = TablesPanel(self.splitter)
        self.TablePanel.setupUi(self.TableOrder)
        self.TablePanel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TablePanel.setFrameShadow(QtWidgets.QFrame.Raised)

        self.frame_2 = QtWidgets.QFrame(self.splitter)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.splitter_2 = QtWidgets.QSplitter(self.frame_2)
        self.splitter_2.setGeometry(QtCore.QRect(0, 10, 451, 621))
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")

        self.RightTopFrame = QtWidgets.QFrame(self.splitter_2)
        self.RightTopFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.RightTopFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.RightTopFrame.setObjectName("RightTopFrame")

        self.InitialPanel = InitialTable(self.RightTopFrame)
        self.InitialPanel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.InitialPanel.setFrameShadow(QtWidgets.QFrame.Raised)

        self.StatusPanel = StatusPanel(self.RightTopFrame)
        self.StatusPanel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.StatusPanel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.StatusPanel.setVisible(False)

        self.MenuPanel = Menu(self.RightTopFrame)
        self.MenuPanel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MenuPanel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MenuPanel.setVisible(False)

        self.RightBottomFrame = QtWidgets.QFrame(self.splitter_2)
        self.RightBottomFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.RightBottomFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.RightBottomFrame.setObjectName("RightBottomFrame")

        self.OrderPanel = OrderListPanel(self.RightBottomFrame, self.Logger)
        self.OrderPanel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.OrderPanel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.OrderPanel.setObjectName("OrderPanel")
        self.OrderPanel.setVisible(False)

        self.FinalStatusPanel = FinalStatusPanel(self.RightTopFrame)
        self.FinalStatusPanel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.FinalStatusPanel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.FinalStatusPanel.setVisible(False)

        self.Receipt = Receipt(self.RightTopFrame)
        # self.Receipt.setVisible(False)

        self.setCentralWidget(self.centralwidget)
        self.toolbar = self.addToolBar("Panels")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ToolBar/Setting.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SettingAction = QtGui.QAction(icon, "SettingPage", self)
        self.toolbar.addAction(self.SettingAction)
        self.SettingAction.triggered.connect(self.menuSetting_onClick)

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ToolBar/Table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TableAction = QtGui.QAction(icon1, "MenuPage", self)
        self.toolbar.addAction(self.TableAction)
        self.TableAction.triggered.connect(self.menuTable_onClick)

        self.TestAction = QtGui.QAction("Test", self)
        self.toolbar.addAction(self.TestAction)
        self.TestAction.triggered.connect(self.ShowJumpWindow)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.TablePanel.BindEvent(self.TableButClick)
        self.closeEvent = self.Close
        self.LayoutSetting()

        self.SettingPanel.SetupPrinters(self.DataBase.Printer)

        CurrentServiceChargePercent = (
            self.DataBase.Setting.GetValue(Config.ValueSetting.TableOrder.STR_DEFAULT_SERVICE_CHARGE_PERCENT))
        if CurrentServiceChargePercent is None:
            CurrentServiceChargePercent = 10
        CurrentDiscountPercentA = (
            self.DataBase.Setting.GetValue(Config.ValueSetting.TableOrder.STR_DEFAULT_DISCOUNT_PERCENT_A))
        if CurrentDiscountPercentA is None:
            CurrentDiscountPercentA = 5
        CurrentDiscountPercentB = (
            self.DataBase.Setting.GetValue(Config.ValueSetting.TableOrder.STR_DEFAULT_DISCOUNT_PERCENT_B))
        if CurrentDiscountPercentB is None:
            CurrentDiscountPercentB = 10

        self.SettingPanel.EventChangeDefaultServiceChargePercent = self.ChangeDefaultServiceChargePercent
        self.SettingPanel.SetupServiceChargePercentList(Config.ValueSetting.TableOrder.SERVICE_CHARGE_PERCENT_LIST,
                                                        CurrentServiceChargePercent)
        self.SettingPanel.EventChangeDefaultDiscountPercentA = self.ChangeDefaultSDiscountPercentA
        self.SettingPanel.SetupDiscountPercentAList(Config.ValueSetting.TableOrder.DISCOUNT_PERCENT_LIST,
                                                    CurrentDiscountPercentA)
        self.SettingPanel.EventChangeDefaultDiscountPercentB = self.ChangeDefaultSDiscountPercentB
        self.SettingPanel.SetupDiscountPercentBList(Config.ValueSetting.TableOrder.DISCOUNT_PERCENT_LIST,
                                                    CurrentDiscountPercentB)

        self.InitialPanel.AddConnect(self.OpenTable)

        self.JumpWindow.InitialCloseEvent(self.CloseJumpWindow)

        self.StatusPanel.CloseTableConnect(self.CloseTableEvent)
        self.StatusPanel.NewOrderConnect(self.StartOrder)
        self.StatusPanel.CheckOutConnect(self.CheckOut)

        self.DataBase.MenuLoad.join()
        self.MenuPanel.AddMenu(self.DataBase.menu)
        self.MenuPanel.Connect(self.OrderFood)

        self.OrderPanel.Connect(self.PlaceOrder)

        self.FinalStatusPanel.ReopenConnect(self.ReopenTable)
        self.FinalStatusPanel.AddCardConnect(self.AddCard)
        self.FinalStatusPanel.AddCashConnect(self.AddCash)
        self.FinalStatusPanel.AddDiscountConnect(self.AddDiscountPercent)
        self.FinalStatusPanel.AddServiceChargeConnect(self.AddServiceChargePercent)
        self.FinalStatusPanel.DefaultServiceChargePercent = CurrentServiceChargePercent
        self.FinalStatusPanel.DefaultDiscountPercentA = CurrentDiscountPercentA
        self.FinalStatusPanel.DefaultDiscountPercentB = CurrentDiscountPercentB
        self.FinalStatusPanel.PrintReceiptConnect(self.Receipt.print_me3)

    def LayoutSetting(self):
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.splitter)
        hbox.addWidget(self.SettingPanel)
        hbox.addWidget(self.JumpWindow)
        self.centralwidget.setLayout(hbox)

        hbox = QtWidgets.QHBoxLayout(self.frame_2)
        hbox.addWidget(self.splitter_2)
        self.frame_2.setLayout(hbox)

        hbox = QtWidgets.QHBoxLayout(self.RightTopFrame)
        hbox.addWidget(self.InitialPanel)
        hbox.addWidget(self.MenuPanel)
        hbox.addWidget(self.StatusPanel)
        hbox.addWidget(self.FinalStatusPanel)
        hbox.addWidget(self.Receipt)
        self.RightTopFrame.setLayout(hbox)

        hbox = QtWidgets.QHBoxLayout(self.RightBottomFrame)
        hbox.addWidget(self.OrderPanel)
        self.RightBottomFrame.setLayout(hbox)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def menuSetting_onClick(self, e):
        try:
            self.SettingPanel.setVisible(True)
            self.splitter.setVisible(False)
        except Exception as e:
            self.Logger.error(f'Error during show Setting panel', exc_info=e)

    def menuTable_onClick(self, e):
        try:
            self.SettingPanel.setVisible(False)
            self.splitter.setVisible(True)
        except Exception as e:
            self.Logger.error(f'Error during show menu panel', exc_info=e)

    def setupTableColor(self):
        self.DataBase.GetOpenTableInfo()
        self.TablePanel.setupTableColor(self.DataBase.TableInfo)

    def TableButClick(self, TableNumber):
        try:
            self.Logger.info(f'start to load Table {TableNumber}')
            self.TableNumber = TableNumber
            self.MenuPanel.setVisible(False)
            self.DataBase.GetOpenTableInfo()
            TableInfo = None
            if TableNumber in self.DataBase.TableInfo.ByTableIDDict:
                TableInfo = self.DataBase.TableInfo.ByTableIDDict[TableNumber]
                self.OrderID = TableInfo.OrderID
            if TableInfo is None or TableInfo.StartTime is None:
                # initial table
                self.InitialPanel.setVisible(True)
                self.InitialPanel.DisplayTable(TableNumber)
                self.OrderPanel.setVisible(False)
                self.StatusPanel.setVisible(False)
                self.FinalStatusPanel.setVisible(False)
            elif TableInfo.EndTime is None:
                # working table
                self.InitialPanel.setVisible(False)
                self.StatusPanel.setVisible(True)
                self.StatusPanel.DisplayTable(TableInfo)
                self.OrderPanel.setVisible(True)
                self.OrderPanel.DisplayTable(TableInfo)
                self.FinalStatusPanel.setVisible(False)
            elif not TableInfo.IsFinished:
                # finishing table
                self.InitialPanel.setVisible(False)
                self.StatusPanel.setVisible(False)
                self.OrderPanel.setVisible(True)
                self.OrderPanel.DisplayTable(TableInfo)
                self.FinalStatusPanel.setVisible(True)
                self.FinalStatusPanel.DisplayTable(TableInfo)
                self.Receipt.LoadTable(TableInfo)
        except Exception as e:
            self.Logger.error(f'Error during show Table {TableNumber} info.', exc_info=e)

    def OpenTable(self):
        try:
            TableNumber = self.TableNumber
            self.Logger.info(f'Table {TableNumber} open')
            if TableNumber is not None:
                self.InitialPanel.setVisible(False)
                self.StatusPanel.setVisible(True)
                self.OrderID = self.DataBase.InitialOrder(TableNumber, self.InitialPanel.EditBoxNumOfPeople.value())
                self.TableButClick(self.TableNumber)
        except Exception as e:
            self.Logger.error(f'Error during Table {self.TableNumber} open', exc_info=e)

    def CloseTableEvent(self):
        try:
            # Need a jump out window
            self.Logger.info(f'Table {self.TableNumber} close check')
            self.JumpWindow.SetQuestion('确定要清台吗？')
            self.JumpWindow.connect(self.CloseTable)
            self.ShowJumpWindow()
        except Exception as e:
            self.Logger.error(f'Error during show Close check', exc_info=e)

    def CloseTable(self):
        try:
            self.Logger.info(f'Close Table {self.TableNumber}')
            self.CloseJumpWindow()
            self.DataBase.CloseTable(self.DataBase.TableInfo.ByTableIDDict[self.TableNumber].OrderID)
            self.TableButClick(self.TableNumber)
        except Exception as e:
            self.Logger.error(f'Error during close Table {self.TableNumber}', exc_info=e)

    def ShowJumpWindow(self):
        try:
            self.JumpWindow.setVisible(True)
            self.SettingPanel.setVisible(False)
            self.splitter.setVisible(False)
        except Exception as e:
            self.Logger.error(f'Error during show jump window', exc_info=e)

    def CloseJumpWindow(self):
        try:
            self.JumpWindow.setVisible(False)
            self.splitter.setVisible(True)
            self.JumpWindow.BtnYes.pressed.disconnect()
        except Exception as e:
            self.Logger.error(f'Error during close jump window', exc_info=e)

    def StartOrder(self):
        try:
            self.StatusPanel.setVisible(False)
            self.MenuPanel.setVisible(True)
            self.OrderPanel.setVisible(True)
            self.OrderPanel.Clear()
        except Exception as e:
            self.Logger.error(f'Error during show menu page, start order', exc_info=e)

    def Close(self, e):
        self.Logger.info(f'close connection')
        self.DataBase.open = False
        self.DataBase.Setting.open = False

    def OrderFood(self, FoodID):
        try:
            self.Logger.info(f'menu order food, food id:{FoodID}')
            Order = OrderInfo()
            Order.FoodID = FoodID
            Order.Qty = 1
            Order.Note = ''
            Order.LoadMenu(self.DataBase.menu)
            Order.UnitPrice = Order.OriUnitPrice
            self.OrderPanel.AddOrder(Order)
        except Exception as e:
            self.Logger.error(f'Error during order food into orderlist', exc_info=e)

    def PlaceOrder(self, Orders):
        try:
            self.Logger.info(f'Place order')
            for order in Orders:
                order.OrderID = self.OrderID
                order.StaffID = self.StaffID
            self.DataBase.PlaceOrder(Orders)
            self.TableButClick(self.TableNumber)
        except Exception as e:
            self.Logger.error(f'Error during placing order', exc_info=e)

    def CheckOut(self):
        TableNumber = int(self.StatusPanel.TableNumber)
        try:
            self.Logger.info(f'Table {TableNumber} checkout')
            self.DataBase.CheckOutTable(TableNumber)
            self.TableButClick(TableNumber)
        except Exception as e:
            self.Logger.error(f'Error during check out table {TableNumber}', exc_info=e)

    def ReopenTable(self):
        self.DataBase.ReopenTable(self.TableNumber)
        self.TableButClick(self.TableNumber)

    def AddCash(self, TotalCash):
        self.DataBase.AddCash(Cash=TotalCash, TableNumber=self.TableNumber)

    def AddCard(self, TotalCard):
        self.DataBase.AddCard(Card=TotalCard, TableNumber=self.TableNumber)

    def AddServiceChargePercent(self, ServiceChargePercent):
        self.DataBase.AddServicePercent(ServicePercent=ServiceChargePercent, TableNumber=self.TableNumber)

    def AddDiscountPercent(self, DiscountPercent):
        self.DataBase.AddDiscountPercent(DiscountPercent=DiscountPercent, TableNumber=self.TableNumber)

    def ChangeDefaultServiceChargePercent(self, Value):
        self.DataBase.Setting.SetValue(Config.ValueSetting.TableOrder.STR_DEFAULT_SERVICE_CHARGE_PERCENT, Value)
        self.FinalStatusPanel.DefaultServiceChargePercent = Value

    def ChangeDefaultSDiscountPercentA(self, Value):
        self.DataBase.Setting.SetValue(Config.ValueSetting.TableOrder.STR_DEFAULT_DISCOUNT_PERCENT_A, Value)
        self.FinalStatusPanel.DefaultDiscountPercentA = Value

    def ChangeDefaultSDiscountPercentB(self, Value):
        self.DataBase.Setting.SetValue(Config.ValueSetting.TableOrder.STR_DEFAULT_DISCOUNT_PERCENT_B, Value)
        self.FinalStatusPanel.DefaultDiscountPercentB = Value


import QtApp.resource_rc

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
