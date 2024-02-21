import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QTableWidget, QHBoxLayout, \
    QTableWidgetItem
from PyQt5.QtGui import QColor
from Config import Config
from TableInfoStore import OrderInfo


class TableWdiget(QTableWidget):
    def __init__(self, parent):
        super().__init__(0, len(Config.DisplaySetting.OrderTable.COL_NAME_CN), parent=parent)
        self.verticalHeader().setDefaultSectionSize(25)
        self.horizontalHeader().setDefaultSectionSize(150)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
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
        self.setHorizontalHeaderLabels(Config.DisplaySetting.OrderTable.COL_NAME_CN)

    def addRow(self, Order: OrderInfo):
        rowCount = self.rowCount()
        self.insertRow(rowCount)
        colCount = self.columnCount()
        displayList = Config.DataBase.MenuList.DISPLAYLIST
        OrderColList = Config.DataBase.OrderList.COLUMNS
        self.setItem(rowCount, 0, QTableWidgetItem(str(Order.NameCN)))
        self.setItem(rowCount, 1, QTableWidgetItem(str(Order.Qty)))
        self.setItem(rowCount, 2, QTableWidgetItem(str(Order.UnitPrice)))
        self.setItem(rowCount, 3, QTableWidgetItem(str(Order.Note)))

    def Clear(self):
        rowCount = self.rowCount()
        for i in range(rowCount - 1, -1, -1):
            self.removeRow(i)

    def CellChanged(self, currentRow, CurrentColumn, previousRow, previousCol):
        self.setRowBackgoundColor(self.selectedRow, QColor(255, 255, 255))
        if self.selectedRow != currentRow:
            self.selectedRow = currentRow
        self.setRowBackgoundColor(self.selectedRow, QColor(207, 254, 255))

    def setRowBackgoundColor(self, row, color):
        if row == None:
            return
        if row >= self.rowCount():
            return
        colCount = self.columnCount()
        for i in range(colCount):
            self.item(row, i).setBackground(color)


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1600, 600)
        mainLayout = QHBoxLayout()
        table = TableWdiget(self)
        mainLayout.addWidget(table)
        self.setLayout(mainLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())
