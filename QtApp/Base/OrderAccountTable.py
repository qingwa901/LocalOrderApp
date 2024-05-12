import sys
from PySide6.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QTableWidget, QHBoxLayout, \
    QTableWidgetItem
from PySide6.QtGui import QColor
from Config import Config
from TableInfoStore import OrderInfo
from QtApp.Base import CTableWidget


class TableWidget(CTableWidget):
    def __init__(self, aParent):
        super().__init__(aParent, 0, len(Config.DisplaySetting.OrderAccountTable.COL_NAME_CN))
        self.verticalHeader().setDefaultSectionSize(25)
        self.horizontalHeader().setDefaultSectionSize(150)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setupUI()
        self.selectedRow = None
        self.currentCellChanged.connect(self.CellChanged)

    def test(self):
        for i in range(20):
            self.insertRow(i)
            for j in range(4):
                self.setItem(i, j, QTableWidgetItem(i))

    def setupUI(self):
        self.setHorizontalHeaderLabels(Config.DisplaySetting.OrderAccountTable.COL_NAME_CN)

    def Refresh(self):
        self.Clear()
        AccountTable = Config.DataBase.OrderAccountList
        OrderData = self.DataBase.GetHistoryOrders()
        AccountData = self.DataBase.GetAccountList()
        for i in range(len(AccountData)):
            Account = AccountData.iloc[i]
            ID = Account[AccountTable.ID]
            Name = Account[AccountTable.ACCOUNT_NAME]
            IsAutoDelete = Account[AccountTable.AUTO_DELETE]
            History_Amount = Account[AccountTable.TOTAL_AMOUNT]
            Today_Amount = 0
            if History_Amount is None:
                History_Amount = 0
            for order in OrderData.ByOrderIDDict.values():
                if order.AccountID == ID:
                    Today_Amount += order.GetTotalAmount()
            rowCount = self.rowCount()
            self.insertRow(rowCount)
            self.setItem(rowCount, 0, QTableWidgetItem(str(ID)))
            self.setItem(rowCount, 1, QTableWidgetItem(str(Name)))
            if IsAutoDelete == 1:
                self.setItem(rowCount, 2, QTableWidgetItem('删除'))
            else:
                self.setItem(rowCount, 2, QTableWidgetItem('保留'))
            self.setItem(rowCount, 3, QTableWidgetItem(str(History_Amount)))
            self.setItem(rowCount, 4, QTableWidgetItem(str(round(Today_Amount, 2))))

    def CurrentAccount(self):
        AccountTable = Config.DataBase.OrderAccountList
        Res = dict()
        row = self.currentRow()
        if row >= 0:
            Res[AccountTable.ID] = int(self.item(row, 0).text())
            Res[AccountTable.ACCOUNT_NAME] = self.item(row, 1).text()
            Res[AccountTable.AUTO_DELETE] = self.item(row, 2).text() == '删除'
            Res[AccountTable.TOTAL_AMOUNT] = round(float(self.item(row, 3).text()), 2)
        return Res


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
