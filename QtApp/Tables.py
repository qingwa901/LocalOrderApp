# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui/Tables.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from QtApp.TableBut import TableBut, TableStatus


class TablesPanel(QtWidgets.QFrame):
    def __init__(self, parant):
        QtWidgets.QFrame.__init__(self, parant)

    def setupUi(self, TableOrder):
        self.setObjectName("Tables")
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        RowNum = 0
        ColNum = 0
        self.Tables = {}
        for row in TableOrder:
            for item in row:
                if item is not None:
                    Table = TableBut(self.gridLayoutWidget)
                    Table.setupUi(int(item))
                    self.gridLayout.addWidget(Table, RowNum, ColNum, 1, 1)
                    self.Tables[item] = Table
                ColNum += 1
            ColNum = 0
            RowNum += 1
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))

    def BindEvent(self, Event):
        for i in self.Tables.values():
            i.BindEvent(Event)

    def setupTableColor(self, TablesInfo):
        for TableNumber in self.Tables:
            TableInfo = None
            if TableNumber in TablesInfo:
                TableInfo = TablesInfo[TableNumber]
            if TableInfo is None or TableInfo.StartTime is None:
                # initial table
                self.Tables[TableNumber].setupColor(TableStatus.Empty)

            elif TableInfo.EndTime is None:
                # working table
                self.Tables[TableNumber].setupColor(TableStatus.Started)
            elif not TableInfo.IsFinished:
                # end table
                self.Tables[TableNumber].setupColor(TableStatus.Finishing)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = TablesPanel(None)
    ui.setupUi([[1]])
    Form.show()
    sys.exit(app.exec_())
