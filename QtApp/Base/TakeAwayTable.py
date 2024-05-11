import sys
from PySide6.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QTableWidget, QHBoxLayout, \
    QTableWidgetItem
from PySide6.QtGui import QColor
from Config import Config
from TableInfoStore import OrderInfo
from QtApp.Base import CTableWidget, RefreshDecoration


class TableWidget(CTableWidget):
    def __init__(self, aParent):
        super().__init__(aParent, 0, len(Config.DisplaySetting.TakeAwayTable.COL_NAME_CN))
        self.setupUI()

    def test(self):
        for i in range(20):
            self.insertRow(i)
            for j in range(len(Config.DisplaySetting.TakeAwayTable.COL_NAME_CN)):
                self.setItem(i, j, QTableWidgetItem(i))

    def setupUI(self):
        self.setHorizontalHeaderLabels(Config.DisplaySetting.TakeAwayTable.COL_NAME_CN)

    @RefreshDecoration
    def Refresh(self):
        SelectedOrderID = self.CurrentOrderID()
        self.Clear()
        selectedRow = None
        AccountTable = Config.DataBase.OrderAccountList
        OrderData = self.DataBase.GetTakeAwayOrders()
        AccountData = self.DataBase.GetAccountList()
        for order in OrderData.ByOrderIDDict.values:
            rowCount = self.rowCount()
            self.insertRow(rowCount)
            self.setItem(rowCount, 0, QTableWidgetItem(str(order.OrderID)))
            self.setItem(rowCount, 1, QTableWidgetItem(str(order.OrderName)))
            self.setItem(rowCount, 2, QTableWidgetItem(str(order.OrderName)))
            for i in range(len(AccountData)):
                Account = AccountData.iloc[i]
                if Account[AccountTable.ID] == order.AccountID:
                    self.setItem(rowCount, 3, QTableWidgetItem(str(Account[AccountTable.ACCOUNT_NAME])))
            self.setItem(rowCount, 4, QTableWidgetItem('已收' if order.IsFinished else '未收'))
            if order.OrderID == SelectedOrderID:
                selectedRow = rowCount
        return selectedRow

    @RefreshDecoration
    def RefreshTest(self):
        self.Clear()
        self.test()

    def CurrentOrderID(self) -> int:
        row = self.currentRow()
        return int(self.item(row, 0).text())


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1600, 600)
        mainLayout = QHBoxLayout()
        self.DataBase = None
        self.Logger = None
        table = TableWidget(self)
        mainLayout.addWidget(table)
        self.setLayout(mainLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())
