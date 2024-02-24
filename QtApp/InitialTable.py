# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui/InitialTable.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class InitialTable(QtWidgets.QFrame):
    def __init__(self, parant):
        QtWidgets.QFrame.__init__(self, parant)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("InitialTable")
        self.resize(469, 361)
        self.formLayoutWidget = QtWidgets.QWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 281, 133))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.LBTableNumber = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBTableNumber.setObjectName("LBTableNumber")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.LBTableNumber)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.EditBoxNumOfPeople = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.EditBoxNumOfPeople.setMinimum(1)
        self.EditBoxNumOfPeople.setMaximum(30)
        self.EditBoxNumOfPeople.setObjectName("EditBoxNumOfPeople")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.EditBoxNumOfPeople)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 220, 121, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.OpenTable = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.OpenTable.setObjectName("OpenTable")
        self.gridLayout.addWidget(self.OpenTable, 0, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "桌号"))
        self.LBTableNumber.setText(_translate("Form", "None"))
        self.label_2.setText(_translate("Form", "人数"))
        self.OpenTable.setText(_translate("Form", "开台"))

    def DisplayTable(self, TableNumber):
        self.TableNumber = TableNumber
        self.LBTableNumber.setText(str(TableNumber))

    def AddConnect(self, Event):
        self.OpenTable.pressed.connect(Event)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = InitialTable(None)
    ui.setupUi()
    ui.show()
    sys.exit(app.exec_())
