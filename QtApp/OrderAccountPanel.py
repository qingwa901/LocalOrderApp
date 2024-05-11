from PySide6 import QtCore, QtWidgets
from QtApp.Base.OrderAccountTable import TableWidget
from TableInfoStore import OrderInfo, TableInfoStore
from functools import partial
from QtApp.Base import CFrame, CPushButton


class OrderAccountPanel(CFrame):
    def __init__(self, aParent):
        CFrame.__init__(self, aParent)
        self.setupUi()
        self.OrderEditEvent = None
        self.IsEditable = True
        self.TableInfo = None
        # self.tableView.cellClicked.connect(self.OpenOrderEditor)
        self.Btnup.pressed.connect(self.btn_page_up)
        self.Btndown.pressed.connect(self.btn_page_down)
        self.OpenEvent = None
        self.BtnEditAccount.pressed.connect(self.OpenEdit)
        self.BtnNewAccount.pressed.connect(self.OpenNew)

    def setupUi(self):
        self.setObjectName("orderList")
        self.tableView = TableWidget(self)
        self.tableView.setObjectName("tableView")
        hLayout = QtWidgets.QHBoxLayout()
        mainLayout = QtWidgets.QVBoxLayout()
        hLayout.addLayout(mainLayout)
        mainLayout.addWidget(self.tableView)
        self.BtnEditAccount = CPushButton(self)
        self.BtnEditAccount.setObjectName("BtnEditAccount")
        self.BtnEditAccount.setMaximumWidth(300)
        self.BtnNewAccount = CPushButton(self)
        self.BtnNewAccount.setObjectName("BtnNewAccount")
        self.BtnNewAccount.setMaximumWidth(300)
        hLayout2 = QtWidgets.QHBoxLayout()
        hLayout2.addWidget(self.BtnEditAccount)
        hLayout2.addWidget(self.BtnNewAccount)
        mainLayout.addLayout(hLayout2)
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
        self.BtnEditAccount.setText(_translate("Form", "编辑"))
        self.BtnNewAccount.setText(_translate("Form", "新建"))
        self.Btnup.setText(_translate("Form", "^"))
        self.Btndown.setText(_translate("Form", "v"))

    def btn_page_up(self):
        scrollBar = self.tableView.verticalScrollBar()
        scrollBar.setValue(scrollBar.value() - scrollBar.pageStep())

    def btn_page_down(self):
        scrollBar = self.tableView.verticalScrollBar()
        scrollBar.setValue(scrollBar.value() + scrollBar.pageStep())

    def Refresh(self):
        self.tableView.Refresh()

    def OpenEdit(self):
        if self.OpenEvent is not None:
            self.OpenEvent(self.tableView.CurrentAccount())

    def OpenNew(self):
        if self.OpenEvent is not None:
            self.OpenEvent(None)
