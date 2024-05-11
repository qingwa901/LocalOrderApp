import sys
from PySide6.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QTableWidget, QHBoxLayout, \
    QTableWidgetItem
from Config import Config
from TableInfoStore import OrderInfo
from QtApp.Base import CTableWidget


class TableWidget(CTableWidget):
    def __init__(self, aParent):
        super().__init__(aParent, 0, len(Config.DisplaySetting.OrderTable.COL_NAME_CN))
        self.setupUI()

    def test(self):
        for i in range(20):
            self.insertRow(i)
            for j in range(len(Config.DisplaySetting.OrderTable.COL_NAME_CN)):
                self.setItem(i, j, QTableWidgetItem(i))

    def setupUI(self):
        self.setHorizontalHeaderLabels(Config.DisplaySetting.OrderTable.COL_NAME_CN)

    def addRow(self, Order: OrderInfo):
        self.Logger.info(f"Add Order Row: {Order.ID}, {Order.NameCN}, {Order.Qty}, {Order.UnitPrice}, {Order.Note}")
        rowCount = self.rowCount()
        self.insertRow(rowCount)
        self.setItem(rowCount, 0, QTableWidgetItem(str(Order.NameCN)))
        self.setItem(rowCount, 1, QTableWidgetItem(str(Order.Qty)))
        self.setItem(rowCount, 2, QTableWidgetItem(str(Order.UnitPrice)))
        self.setItem(rowCount, 3, QTableWidgetItem(str(Order.Note)))


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
