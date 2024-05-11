from PySide6 import QtCore, QtWidgets
from QtApp.Base.TakeAwayTable import TableWidget
from TableInfoStore import OrderInfo, TableInfoStore
from functools import partial
from QtApp.Base import CFrame, CPushButton


class TakeAwayPanel(CFrame):
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
        self.BtnNewAccount.pressed.connect(self.OpenNew)

    def setupUi(self):
        self.setObjectName("orderList")
        self.tableView = TableWidget(self)
        self.tableView.setObjectName("tableView")
        hLayout = QtWidgets.QHBoxLayout()
        mainLayout = QtWidgets.QVBoxLayout()
        hLayout.addLayout(mainLayout)
        mainLayout.addWidget(self.tableView)
        self.BtnNewAccount = CPushButton(self)
        self.BtnNewAccount.setObjectName("BtnNewAccount")
        self.BtnNewAccount.setMaximumWidth(300)
        hLayout2 = QtWidgets.QHBoxLayout()
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

    def OpenNew(self):
        if self.OpenEvent is not None:
            self.OpenEvent(None)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = TakeAwayPanel(None)
    ui.show()
    ui.tableView.test()
    ui.BtnNewAccount.pressed.connect(ui.tableView.RefreshTest)
    sys.exit(app.exec_())
