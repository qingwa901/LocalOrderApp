# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui/SettingPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PrinterControl import PrinterControl
from QtApp.SettingPanelBase import SettingPanelBase
from functools import partial
from Config import Config


class SettingPanel(SettingPanelBase):
    def __init__(self, parant):
        SettingPanelBase.__init__(self, parant)
        self.EventChangeDefaultServiceChargePercent = None
        self.EventChangeDefaultDiscountPercentA = None
        self.EventChangeDefaultDiscountPercentB = None

    def SetupPrinters(self, Printer: PrinterControl):
        self.Printer = Printer
        self.PrintList = Printer.PrinterList()
        for PrinterName in self.PrintList:
            self.CBCashierPrinter.addItem(PrinterName)
        if self.Printer.DefaultCashierPrinter is not None:
            self.CBCashierPrinter.setCurrentText(self.Printer.DefaultCashierPrinter)
        else:
            self.CBCashierPrinter.setCurrentIndex(-1)
        self.CBCashierPrinter.currentIndexChanged.connect(self.CashierPrinterChange)
        self.BtnCashierTestPrint.pressed.connect(self.SendCashierTestOrder)
        for CBPrinterID in self.CBsPrinter:
            for PrinterName in self.PrintList:
                self.CBsPrinter[CBPrinterID].addItem(PrinterName)

            if self.Printer.DefaultKitchenPrinters[CBPrinterID] is not None:
                self.CBsPrinter[CBPrinterID].setCurrentText(self.Printer.DefaultKitchenPrinters[CBPrinterID])
            else:
                self.CBsPrinter[CBPrinterID].setCurrentIndex(-1)
            self.CBsPrinter[CBPrinterID].currentIndexChanged.connect(partial(self.KitchenPrinterChange, CBPrinterID))
            self.BtnsPrinterTest[CBPrinterID].pressed.connect(partial(self.SendKitchenTestOrder, CBPrinterID))

    def SendKitchenTestOrder(self, MenuID):
        self.Printer.SendTestOrder(self.Printer.DefaultKitchenPrinters[MenuID],
                                   Config.DisplaySetting.MenuPage.MENU_EN_NAME[MenuID])

    def SendCashierTestOrder(self):
        self.Printer.SendTestOrder(self.Printer.DefaultCashierPrinter, 'Cashier')

    def SetupServiceChargePercentList(self, PercentList, CurrentPercent):
        self.ServiceChargePercentList = PercentList
        for Percent in PercentList:
            self.CBServiceChargePercent.addItem(f"{Percent}%")
        self.CBServiceChargePercent.setCurrentText(f"{CurrentPercent}%")
        self.CBServiceChargePercent.currentIndexChanged.connect(self.CBServiceChargePercentChangeEvent)

    def SetupDiscountPercentAList(self, PercentList, CurrentPercent):
        self.DiscountPercentAList = PercentList
        for Percent in PercentList:
            self.CBDiscountPercentA.addItem(f"{Percent}%")
        self.CBDiscountPercentA.setCurrentText(f"{CurrentPercent}%")
        self.CBDiscountPercentA.currentIndexChanged.connect(self.CBDiscountPercentAChangeEvent)

    def SetupDiscountPercentBList(self, PercentList, CurrentPercent):
        self.DiscountPercentBList = PercentList
        for Percent in PercentList:
            self.CBDiscountPercentB.addItem(f"{Percent}%")
        self.CBDiscountPercentB.setCurrentText(f"{CurrentPercent}%")
        self.CBDiscountPercentB.currentIndexChanged.connect(self.CBDiscountPercentBChangeEvent)

    def KitchenPrinterChange(self, MenuId, index):
        self.Printer.SetDefaultKitchenPrinter(self.PrintList[index], MenuId)

    def CashierPrinterChange(self, index):
        self.Printer.SetDefaultCashierPrinter(self.PrintList[index])

    def CBServiceChargePercentChangeEvent(self, index):
        self.EventChangeDefaultServiceChargePercent(self.ServiceChargePercentList[index])

    def CBDiscountPercentAChangeEvent(self, index):
        self.EventChangeDefaultDiscountPercentA(self.DiscountPercentAList[index])

    def CBDiscountPercentBChangeEvent(self, index):
        self.EventChangeDefaultDiscountPercentB(self.DiscountPercentBList[index])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = SettingPanel(None)
    ui.show()
    sys.exit(app.exec_())
