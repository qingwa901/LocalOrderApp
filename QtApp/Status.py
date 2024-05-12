# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui/Status.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets
from QtApp.Base import CFrame, CPushButton, CWidget


class StatusPanel(CFrame):
    def __init__(self, aParent):
        CFrame.__init__(self, aParent)
        self.setupUi()
        self.TableNumber = None
        self.OrderID = None

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(468, 232)
        self.formLayoutWidget = CWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 281, 131))
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
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.LBNumOfPeople = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBNumOfPeople.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LBNumOfPeople.setObjectName("LBNumOfPeople")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.LBNumOfPeople)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.LBStartTime = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBStartTime.setObjectName("LBStartTime")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.LBStartTime)

        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.LBName = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBName.setObjectName("LBName")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.LBName)

        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.LBNumber = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBNumber.setObjectName("LBName")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.LBNumber)

        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.LBNote = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBNote.setObjectName("LBNote")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.LBNote)

        self.gridLayoutWidget = CWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 150, 295, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.BtnCleanTable = CPushButton(self.gridLayoutWidget)
        self.BtnCleanTable.setObjectName("BtnCleanTable")
        self.gridLayout.addWidget(self.BtnCleanTable, 0, 1, 1, 1)
        self.BtnNewOrder = CPushButton(self.gridLayoutWidget)
        self.BtnNewOrder.setObjectName("BtnNewOrder")
        self.gridLayout.addWidget(self.BtnNewOrder, 0, 0, 1, 1)
        self.BtnCheckOut = CPushButton(self.gridLayoutWidget)
        self.BtnCheckOut.setObjectName("BtnCheckOut")
        self.gridLayout.addWidget(self.BtnCheckOut, 0, 2, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Status"))
        self.label.setText(_translate("Form", "桌号"))
        self.LBTableNumber.setText(_translate("Form", "None"))
        self.label_2.setText(_translate("Form", "人数"))
        self.LBNumOfPeople.setText(_translate("Form", "None"))
        self.label_3.setText(_translate("Form", "开始时间"))
        self.LBStartTime.setText(_translate("Form", "None"))

        self.label_4.setText(_translate("Form", "订单名"))
        self.LBName.setText(_translate("Form", "None"))
        self.label_5.setText(_translate("Form", "电话号码"))
        self.LBNumber.setText(_translate("Form", "None"))
        self.label_6.setText(_translate("Form", "备注"))
        self.LBNote.setText(_translate("Form", "None"))

        self.BtnCleanTable.setText(_translate("Form", "关台"))
        self.BtnNewOrder.setText(_translate("Form", "下单"))
        self.BtnCheckOut.setText(_translate("Form", "结账"))

    def DisplayTable(self, TableInfo):
        self.Clear()
        self.OrderID = TableInfo.OrderID
        self.BtnCleanTable.setVisible(len(TableInfo.Orders) == 0)
        self.BtnCheckOut.setVisible(len(TableInfo.Orders) != 0)
        if int(TableInfo.TableID) > 0:
            self.TableNumber = TableInfo.TableID
            self.LBTableNumber.setText(TableInfo.TableID)
            self.LBStartTime.setText(TableInfo.StartTime)
            self.LBNumOfPeople.setText(str(TableInfo.NumOfPeople))
            self.SwitchTakeAway(False)
        else:
            self.TableNumber = 0
            self.LBTableNumber.setText("外卖")
            self.LBStartTime.setText(TableInfo.StartTime)
            self.LBName.setText(TableInfo.OrderName)
            self.LBNumber.setText(TableInfo.OrderNumber)
            self.LBNote.setText(TableInfo.OrderNote)
            self.SwitchTakeAway(True)

    def Clear(self):
        self.TableNumber = None
        self.OrderID = None
        self.LBTableNumber.setText('')
        self.LBStartTime.setText('')
        self.LBName.setText('')
        self.LBNumber.setText('')
        self.LBNote.setText('')

    def SwitchTakeAway(self, IsTakeAway):
        self.LBNumOfPeople.setVisible(not IsTakeAway)
        self.label_2.setVisible(not IsTakeAway)
        self.label_4.setVisible(IsTakeAway)
        self.label_5.setVisible(IsTakeAway)
        self.label_6.setVisible(IsTakeAway)
        self.LBName.setVisible(IsTakeAway)
        self.LBNumber.setVisible(IsTakeAway)
        self.LBNote.setVisible(IsTakeAway)

    def CloseTableConnect(self, Event):
        self.BtnCleanTable.pressed.connect(Event)

    def NewOrderConnect(self, Event):
        self.BtnNewOrder.pressed.connect(Event)

    def CheckOutConnect(self, Event):
        self.BtnCheckOut.pressed.connect(Event)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = StatusPanel(None)
    # ui.SwitchTakeAway(True)
    ui.show()
    sys.exit(app.exec_())
