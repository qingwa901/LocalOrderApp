import sys
from PySide6.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QTableWidget, QHBoxLayout, \
    QTableWidgetItem
from PySide6.QtGui import QColor
from Config import Config
from TableInfoStore import OrderInfo
from QtApp.Base import CTableWidget, RefreshDecoration
from typing import Union


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
        if len(OrderData.ByOrderIDDict) > 0:
            AccountData = self.DataBase.GetAccountList()
            for order in OrderData.ByOrderIDDict.values():
                rowCount = self.rowCount()
                self.insertRow(rowCount)
                self.setItem(rowCount, 0, QTableWidgetItem(str(order.OrderID)))
                self.setItem(rowCount, 1, QTableWidgetItem(str(order.OrderName)))
                AccountName = AccountData[AccountData['ID'] == order.AccountID]['AccountName']
                if len(AccountName) > 0:
                    self.setItem(rowCount, 2, QTableWidgetItem(AccountName.iloc[0]))
                else:
                    self.setItem(rowCount, 2, QTableWidgetItem(''))

                self.setItem(rowCount, 3, QTableWidgetItem(str(round(order.GetTotalAmount(), 2))))

                self.setItem(rowCount, 4, QTableWidgetItem('已收' if order.IsFinished else '未收'))
                if order.OrderID == SelectedOrderID:
                    selectedRow = rowCount
        return selectedRow

    @RefreshDecoration
    def RefreshTest(self):
        self.Clear()
        self.test()

    def CurrentOrderID(self) -> Union[int, None]:
        row = self.currentRow()
        if row >= 0:
            try:
                return int(self.item(row, 0).text())
            except ValueError:
                self.Logger.error(f"Order ID {self.item(row, 0).text()} is not int")
                return None
        else:
            return None


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
