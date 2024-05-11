from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QHeaderView, QAbstractItemView
import functools


class CTableWidget(QtWidgets.QTableWidget):
    def __init__(self, aParent, *args, **kwargs):
        QtWidgets.QTableWidget.__init__(self, parent=aParent, *args, **kwargs)
        if aParent is not None:
            self.Logger = aParent.Logger
            self.DataBase = aParent.DataBase
        else:
            self.Logger = None
            self.DataBase = None
        self.verticalHeader().setDefaultSectionSize(25)
        self.horizontalHeader().setDefaultSectionSize(150)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.setAutoScroll(True)
        self.selectedRow = None
        self.currentCellChanged.connect(self.CellChanged)

    def AbsX(self):
        return self.x() + self.parent().AbsX()

    def AbsY(self):
        return self.y() + self.parent().AbsY()

    def SetBackgoundColor(self, aColor):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'background-color: {aColor};')

    def Clear(self):
        self.selectedRow = None
        rowCount = self.rowCount()
        for i in range(rowCount - 1, -1, -1):
            self.removeRow(i)

    def CellChanged(self, currentRow, CurrentColumn, previousRow, previousCol):
        if previousRow is not None and previousRow > -1:
            self.setRowBackgroundColor(previousRow, QColor(255, 255, 255))
        if self.selectedRow != currentRow:
            self.selectedRow = currentRow
        if self.selectedRow is not None and self.selectedRow > -1:
            self.setRowBackgroundColor(self.selectedRow, QColor(207, 254, 255))

    def setRowBackgroundColor(self, row, color):
        if row is None:
            return
        if row >= self.rowCount():
            return
        colCount = self.columnCount()
        for i in range(colCount):
            cell = self.item(row, i)
            if cell is not None:
                cell.setBackground(color)


def RefreshDecoration(function):
    @functools.wraps(function)
    def wrap(self, *args, **kwargs):
        self.currentCellChanged.disconnect(self.CellChanged)
        scrollBar = self.verticalScrollBar()
        scrollValue = scrollBar.value()
        selectedRow = self.selectedRow
        rowID = function(self, *args, **kwargs)
        if rowID is not None:
            selectedRow = rowID
        scrollBar.setValue(scrollValue)
        if selectedRow is not None and selectedRow > -1:
            # self.setCurrentCell(selectedRow, 0)
            self.selectedRow = selectedRow
            self.setRowBackgroundColor(selectedRow, QColor(207, 254, 255))
        self.currentCellChanged.connect(self.CellChanged)

    return wrap
