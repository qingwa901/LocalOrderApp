# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui/OrderList.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtWidgets
from QtApp.Base.OrderTableWidget import TableWidget
from collections import defaultdict
from TableInfoStore import OrderInfo, TableInfoStore
from functools import partial
from Logger import CreateLogger
from QtApp.Base import CFrame, CPushButton


class OrderListPanel(CFrame):
    def __init__(self, aParent):
        CFrame.__init__(self, aParent)
        self.setupUi()
        self.OrderEditEvent = None
        self.IsEditable = True
        self.Orders = TableInfoStore()
        self.TableInfo = None
        self.tableView.cellClicked.connect(self.OpenOrderEditor)
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
        self.BtnPlaceOrder = CPushButton(self)
        self.BtnPlaceOrder.setObjectName("BtnPlacecOrder")
        self.BtnPlaceOrder.setMaximumWidth(300)
        mainLayout.addWidget(self.BtnPlaceOrder)
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
        self.setWindowTitle(_translate("Form", "OrderList"))
        self.BtnPlaceOrder.setText(_translate("Form", "下单"))
        self.Btnup.setText(_translate("Form", "^"))
        self.Btndown.setText(_translate("Form", "v"))

    def selectedRow(self):
        return self.tableView.selectedRow

    def DisplayTable(self, TableInfo):
        self.Logger.debug(f'Display Order:ID {TableInfo.OrderID}, table: {TableInfo.TableID}')
        self.tableView.Clear()
        self.BtnPlaceOrder.setVisible(False)
        self.Orders.Clear()
        self.Orders.OrderID = TableInfo.OrderID
        self.Orders.TableID = TableInfo.TableID
        self.Orders.Orders = []
        for order in TableInfo.Orders.values():
            self.Orders.Orders.append(order)
            self.tableView.addRow(order)

    def Reload(self):
        self.tableView.Clear()
        for order in self.Orders.Orders:
            self.tableView.addRow(order)

    def Clear(self):
        self.Logger.info('clear OrderList panel')
        self.tableView.Clear()
        self.BtnPlaceOrder.setVisible(True)
        self.Orders.Orders = []

    def AddOrder(self, Order):
        self.Orders.Orders.append(Order)
        self.tableView.addRow(Order)

    def Connect(self, Event):
        self.BtnPlaceOrder.pressed.connect(partial(Event, self.Orders))

    def OpenOrderEditor(self, row, column):
        if self.IsEditable:
            Order = self.Orders.Orders[row]
            self.OrderEditEvent(Order)

    def btn_page_up(self):
        scrollBar = self.tableView.verticalScrollBar()
        scrollBar.setValue(scrollBar.value() - scrollBar.pageStep())

    def btn_page_down(self):
        scrollBar = self.tableView.verticalScrollBar()
        scrollBar.setValue(scrollBar.value() + scrollBar.pageStep())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = OrderListPanel(None)
    ui.show()
    ui.tableView.test()
    sys.exit(app.exec_())
