from PySide6 import QtCore, QtWidgets
from QtApp.Base.HistoryTableWidget import TableWidget

from collections import defaultdict
from TableInfoStore import AllTableInfoStore
from functools import partial
from Logger import CreateLogger
from QtApp.Base import CFrame, CPushButton


class HistoryOrders(CFrame):
    def __init__(self, aParent):
        CFrame.__init__(self, aParent)
        self.setupUi()
        self.OpenHistoryOrderEvent = None
        self.IsEditable = True
        self.OrderList = None
        self.tableView.cellClicked.connect(self.OpenHistoryOrderEvent)
        self.Btnup.pressed.connect(self.btn_page_up)
        self.Btndown.pressed.connect(self.btn_page_down)

    def setupUi(self):
        self.setObjectName("orderList")
        self.tableView = TableWidget(self)
        self.tableView.setObjectName("tableView")
        hLayout = QtWidgets.QHBoxLayout()
        mainLayout = QtWidgets.QVBoxLayout()
        hLayout.addLayout(mainLayout)
        mainLayout.addWidget(self.tableView)
        # self.BtnPlaceOrder = CPushButton(self)
        # self.BtnPlaceOrder.setObjectName("BtnPlacecOrder")
        # self.BtnPlaceOrder.setMaximumWidth(300)
        # mainLayout.addWidget(self.BtnPlaceOrder)
        vLayout = QtWidgets.QVBoxLayout()
        hLayout.addLayout(vLayout)
        self.Btnup = CPushButton(self)
        vLayout.addWidget(self.Btnup)
        self.Btndown = CPushButton(self)
        vLayout.addWidget(self.Btndown)
        self.setLayout(hLayout)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "HistoryOrderList"))
        # self.BtnPlaceOrder.setText(_translate("Form", "下单"))
        self.Btnup.setText(_translate("Form", "^"))
        self.Btndown.setText(_translate("Form", "v"))

    def btn_page_up(self):
        scrollBar = self.tableView.verticalScrollBar()
        scrollBar.setValue(scrollBar.value() - scrollBar.pageStep())

    def btn_page_down(self):
        scrollBar = self.tableView.verticalScrollBar()
        scrollBar.setValue(scrollBar.value() + scrollBar.pageStep())

    def OpenHistoryOrder(self, row, column):
        if self.OpenHistoryOrderEvent is not None:
            Order = self.OrderList[row]
            self.OpenHistoryOrderEvent(Order)

    def DisplayAllOrders(self,):
        self.Logger.debug(f'Display History Orders List:')
        Orders = self.DataBase.GetHistoryOrders()
        self.tableView.Clear()
        self.OrderList = Orders.ByOrderIDDict.values()
        for order in self.OrderList:
            self.tableView.addRow(order)


