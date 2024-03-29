# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui/FinalStatus.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets
from TableInfoStore import TableInfoStore
from QtApp.FinalStatusBase import FinalStatusBase
from functools import partial


class FinalStatusPanel(FinalStatusBase):

    def __init__(self, aParent):
        FinalStatusBase.__init__(self, aParent)
        self.total = 0
        self.cash = 0
        self.card = 0
        self.ServiceChargePercent = 10
        self.DiscountPercent = 0
        self.AddCashEvent = None
        self.AddCardEvent = None
        self.AddDiscountEvent = None
        self.AddServiceChargeEvent = None
        self.BtnCashRemove.pressed.connect(self.RemoveCash)
        self.BtnCardRemove.pressed.connect(self.RemoveCard)
        self.BtnPay5Cash.pressed.connect(partial(self.AddCash, 5))
        self.BtnPay10Cash.pressed.connect(partial(self.AddCash, 10))
        self.BtnPay20Cash.pressed.connect(partial(self.AddCash, 20))
        self.BtnPayByCard.pressed.connect(self.AddRestCard)
        self.BtnPayByCash.pressed.connect(self.AddRestCash)
        self._DefaultServiceChargePercent = 10
        self._DefaultDisCountPercentA = 5
        self._DefaultDisCountPercentB = 10
        _translate = QtCore.QCoreApplication.translate
        self.ButDiscountA.setText(_translate("Form", "5%"))
        self.ButDiscountB.setText(_translate("Form", "10%"))
        self.BtnRemoveDiscount.pressed.connect(self.RemoveDiscount)
        self.ButDiscountA.pressed.connect(self.AddDiscountA)
        self.ButDiscountB.pressed.connect(self.AddDiscountB)
        self.BtnAddRemoveServiceCharge.pressed.connect(self.ChangeServiceChargePercent)

    def AddEvent(self):
        self.BtnPrintReceipt.pressed.connect(self.PrintReceipt)

    def setUpOpenKeyboardEvent(self, event):
        self.EditBoxToPayAmount.OpenKeyboardEvent = event

    def SetDefaultDiscountPercentA(self, Value):
        self._DefaultDisCountPercentA = Value
        _translate = QtCore.QCoreApplication.translate
        self.ButDiscountA.setText(_translate("Form", f"{Value}%"))

    def GetDefaultDiscountPercentA(self):
        return self._DefaultDisCountPercentA

    DefaultDiscountPercentA = property(GetDefaultDiscountPercentA, SetDefaultDiscountPercentA)

    def SetDefaultDiscountPercentB(self, Value):
        self._DefaultDisCountPercentB = Value
        _translate = QtCore.QCoreApplication.translate
        self.ButDiscountB.setText(_translate("Form", f"{Value}%"))

    def GetDefaultDiscountPercentB(self):
        return self._DefaultDisCountPercentB

    DefaultDiscountPercentB = property(GetDefaultDiscountPercentB, SetDefaultDiscountPercentB)

    def SetDefaultServiceChargePercent(self, Value: float):
        self._DefaultServiceChargePercent = Value

    def GetDefaultServiceChargePercent(self):
        return self._DefaultServiceChargePercent

    DefaultServiceChargePercent = property(GetDefaultServiceChargePercent, SetDefaultServiceChargePercent)

    def DisplayTable(self, TableInfo: TableInfoStore):
        self.Clear()
        self.TableInfo = TableInfo
        self.LBTableNumber.setText(TableInfo.TableID)
        self.LBStartTime.setText(TableInfo.StartTime)
        self.LBEndTime.setText(TableInfo.EndTime)
        self.LBNumOfPeople.setText(TableInfo.NumOfPeople)
        self.total = round(TableInfo.GetTotalAmount(), 2)
        self.DiscountPercent = TableInfo.Discount
        self.ServiceChargePercent = TableInfo.ServiceCharge
        if TableInfo.Cash is None:
            self.cash = 0
        else:
            self.cash = float(TableInfo.Cash)
        if TableInfo.Card is None:
            self.card = 0
        else:
            self.card = float(TableInfo.Card)
        self.DisplayAllInfo()

    def Clear(self):
        self.card = 0
        self.cash = 0
        self.total = 0
        self.ServiceChargePercent = self.DefaultServiceChargePercent
        self.DiscountPercent = 0
        self.TableInfo = None

    def DisplayAllInfo(self):
        self.LBPaiedCash_2.setText(str(round(self.cash, 2)))
        self.LBPaidCard.setText(str(round(self.card, 2)))
        ServiceCharge = round(self.total * self.ServiceChargePercent / 100, 2)
        self.LBServiceCharge.setText(str(ServiceCharge) + f" ({self.ServiceChargePercent}%)")
        DiscountAmount = round(self.total * self.DiscountPercent / 100, 2)
        self.LBDiscountAmount.setText(str(DiscountAmount) + f" ({self.DiscountPercent}%)")
        self.LBTotalAmount.setText(str(round(self.total + ServiceCharge - DiscountAmount, 2)) +
                                   f" ({round(self.total, 2)})")
        LeftToPay = round(self.total + ServiceCharge - DiscountAmount - self.card - self.cash, 2)
        if LeftToPay > 0:
            self.EditBoxToPayAmount.setText(str(LeftToPay))
            self.LBLablePayment.setText('未付')
            self.BtnCleanTable.setEnabled(False)
        else:
            self.EditBoxToPayAmount.setText(str(-LeftToPay))
            self.LBLablePayment.setText('找零')
            self.BtnCleanTable.setEnabled(True)

    def ReopenConnect(self, Event):
        self.BtnReOpen.pressed.connect(Event)

    def CleanTableConnect(self, Event):
        self.BtnCleanTable.pressed.connect(Event)

    def PrintReceipt(self):
        self.DataBase.Printer.PrintReceipt(self.TableInfo)

    def RemoveCash(self):
        self.cash = 0
        self.AddCashEvent(0)
        self.DisplayAllInfo()

    def RemoveCard(self):
        self.card = 0
        self.AddCardEvent(0)
        self.DisplayAllInfo()

    def AddCash(self, Amount):
        self.cash += Amount
        self.AddCashEvent(self.cash)
        self.DisplayAllInfo()

    def AddCard(self, Amount):
        self.card += Amount
        self.AddCardEvent(self.cash)
        self.DisplayAllInfo()

    def AddRestCash(self):
        self.cash += float(self.EditBoxToPayAmount.text())
        self.AddCashEvent(self.cash)
        self.DisplayAllInfo()

    def AddRestCard(self):
        self.card += float(self.EditBoxToPayAmount.text())
        self.AddCardEvent(self.card)
        self.DisplayAllInfo()

    def ChangeServiceChargePercent(self):
        if self.ServiceChargePercent > 0:
            self.ServiceChargePercent = 0
        else:
            self.ServiceChargePercent = self.DefaultServiceChargePercent
        self.AddServiceChargeEvent(self.ServiceChargePercent)
        self.DisplayAllInfo()

    def RemoveDiscount(self):
        self.DiscountPercent = 0
        self.AddDiscountEvent(0)
        self.DisplayAllInfo()

    def AddDiscountA(self):
        self.DiscountPercent = self.DefaultDiscountPercentA
        self.AddDiscountEvent(self.DefaultDiscountPercentA)
        self.DisplayAllInfo()

    def AddDiscountB(self):
        self.DiscountPercent = self.DefaultDiscountPercentB
        self.AddDiscountEvent(self.DefaultDiscountPercentB)
        self.DisplayAllInfo()

    def AddCashConnect(self, Event):
        self.AddCashEvent = Event

    def AddCardConnect(self, Event):
        self.AddCardEvent = Event

    def AddDiscountConnect(self, Event):
        self.AddDiscountEvent = Event

    def AddServiceChargeConnect(self, Event):
        self.AddServiceChargeEvent = Event

    def HistoryOrderSetting(self, Display):
        self.BtnCleanTable.setVisible(Display)
        self.ButDiscountB.setVisible(Display)
        self.ButDiscountA.setVisible(Display)
        self.BtnReOpen.setVisible(Display)
        self.BtnAddRemoveServiceCharge.setVisible(Display)
        self.BtnRemoveDiscount.setVisible(Display)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = FinalStatusPanel(None)
    ui.show()
    ui.HistoryOrderSetting()
    sys.exit(app.exec_())
