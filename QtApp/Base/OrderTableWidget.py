import sys
from PySide6.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QTableWidget, QHBoxLayout, \
    QTableWidgetItem
from PySide6.QtGui import QColor
from Config import Config
from TableInfoStore import OrderInfo
from QtApp.Base import CTableWidget


class TableWidget(CTableWidget):
    def __init__(self, aParent):
        super().__init__(aParent, 0, len(Config.DisplaySetting.OrderTable.COL_NAME_CN))
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
        self.setHorizontalHeaderLabels(Config.DisplaySetting.OrderTable.COL_NAME_CN)

    def addRow(self, Order: OrderInfo):
        self.Logger.info(f"Add Order Row: {Order.ID}, {Order.NameCN}, {Order.Qty}, {Order.UnitPrice}, {Order.Note}")
        rowCount = self.rowCount()
        self.insertRow(rowCount)
        self.setItem(rowCount, 0, QTableWidgetItem(str(Order.NameCN)))
        self.setItem(rowCount, 1, QTableWidgetItem(str(Order.Qty)))
        self.setItem(rowCount, 2, QTableWidgetItem(str(Order.UnitPrice)))
        self.setItem(rowCount, 3, QTableWidgetItem(str(Order.Note)))

    def Clear(self):
        self.selectedRow = None
        rowCount = self.rowCount()
        for i in range(rowCount - 1, -1, -1):
            self.removeRow(i)

    def CellChanged(self, currentRow, CurrentColumn, previousRow, previousCol):
        if self.selectedRow is not None and self.selectedRow > -1:
            self.setRowBackgroundColor(self.selectedRow, QColor(255, 255, 255))
        if self.selectedRow != currentRow:
            self.selectedRow = currentRow
        if self.selectedRow is not None and self.selectedRow > -1:
            self.setRowBackgroundColor(self.selectedRow, QColor(207, 254, 255))

    def setRowBackgroundColor(self, row, color):
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
        table = TableWidget(self)
        mainLayout.addWidget(table)
        self.setLayout(mainLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())
