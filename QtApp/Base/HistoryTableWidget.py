import sys
from PySide6.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QTableWidget, QHBoxLayout, \
    QTableWidgetItem
from PySide6.QtGui import QColor
from Config import Config
from TableInfoStore import TableInfoStore
from QtApp.Base import CTableWidget, CWidget


class TableWidget(CTableWidget):
    def __init__(self, aParent):
        super().__init__(aParent, 0, len(Config.DisplaySetting.HistoryOrderTable.COL_NAME_CN))
        self.setupUI()

    def test(self):
        for i in range(20):
            self.insertRow(i)
            for j in range(8):
                self.setItem(i, j, QTableWidgetItem(i))

    def setupUI(self):
        self.setHorizontalHeaderLabels(Config.DisplaySetting.HistoryOrderTable.COL_NAME_CN)

    def addRow(self, Order: TableInfoStore):
        self.Logger.info(f"{Order.OrderID}, {Order.TableID}, {Order.GetTotalAmount()}, {Order.EndTime}")
        rowCount = self.rowCount()
        self.insertRow(rowCount)
        if Order.EndTime is not None:
            self.setItem(rowCount, 0, QTableWidgetItem(str(Order.EndTime.split(' ')[1])))
        else:
            self.setItem(rowCount, 0, QTableWidgetItem(''))
        self.setItem(rowCount, 1, QTableWidgetItem(str(Order.OrderID)))
        self.setItem(rowCount, 2, QTableWidgetItem(str(Order.TableID)))
        total = round(Order.GetTotalAmount(), 2)
        self.setItem(rowCount, 3, QTableWidgetItem(str(total)))
        self.setItem(rowCount, 4, QTableWidgetItem(str(round(Order.ServiceCharge * Order.GetTotalAmount() / 100, 2))))
        self.setItem(rowCount, 5, QTableWidgetItem(str(round(Order.GetTotalAmount() * Order.Discount / 100, 2))))
        self.setItem(rowCount, 6, QTableWidgetItem(str(Order.Cash)))
        self.setItem(rowCount, 7, QTableWidgetItem(str(Order.Card)))
        self.setItem(rowCount, 8,
                     QTableWidgetItem(str(round(total * (1 + Order.ServiceCharge / 100) * (
                             1 - Order.Discount / 100) - Order.Cash - Order.Card, 2))))


class AppDemo(CWidget):
    def __init__(self):
        super().__init__(None)
        self.resize(1600, 600)
        mainLayout = QHBoxLayout()
        table = TableWidget(self)
        mainLayout.addWidget(table)
        self.setLayout(mainLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())
