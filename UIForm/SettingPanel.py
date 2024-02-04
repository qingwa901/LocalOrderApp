# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 22:07:36 2024

@author: qingw
"""

import wx
from Config import Config
from logging import Logger
from DataBase import DataBase


class SettingPanel(wx.Panel):
    """"""

    def __init__(self, parent, size, logger: Logger, DataBase: DataBase):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent, size=size)
        self._logger = logger
        self._database = DataBase
        vSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Printer Setting:")
        hSizer.Add(label)
        vSizer.Add(hSizer)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Cashier Printer:")
        hSizer.Add(label)
        PrinterList = self._database.Printer.PrinterList()
        self.CashPrinter = wx.ComboBox(self, choices=PrinterList)
        self.CashPrinter.Bind(wx.EVT_COMBOBOX, self.CashierSelectorOnChange)
        hSizer.Add(self.CashPrinter)
        TestBut1 = wx.Button(self, label=f"Test Print")
        TestBut1.Bind(wx.EVT_BUTTON, self.TestPrinterCashier)
        hSizer.Add(TestBut1)
        vSizer.Add(hSizer)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Kitchen Printer:")
        hSizer.Add(label)
        PrinterList = self._database.Printer.PrinterList()
        self.KitchenPrinter = wx.ComboBox(self, choices=PrinterList)
        self.KitchenPrinter.Bind(wx.EVT_COMBOBOX, self.KitchenSelectorOnChange)
        hSizer.Add(self.KitchenPrinter)
        TestBut2 = wx.Button(self, label=f"Test Print")
        TestBut2.Bind(wx.EVT_BUTTON, self.TestPrintKitchen)
        hSizer.Add(TestBut2)
        vSizer.Add(hSizer)

        self.SetSizer(vSizer)
        self.Hide()
        self.InitialSelection()

    def InitialSelection(self):
        self.CashPrinter.Clear()
        self.KitchenPrinter.Clear()
        PrinterList = self._database.Printer.PrinterList()
        n = 1
        for Printer in PrinterList:
            self.CashPrinter.Append(Printer, (n, Printer))
            self.KitchenPrinter.Append(Printer, (n, Printer))
            n += 1
        if self._database.Printer.DefaultCashierPrinter in PrinterList:
            self.CashPrinter.SetValue(self._database.Printer.DefaultCashierPrinter)
        else:
            self.CashPrinter.SetValue('')
        if self._database.Printer.DefaultKitchenPrinter in PrinterList:
            self.KitchenPrinter.SetValue(self._database.Printer.DefaultKitchenPrinter)
        else:
            self.KitchenPrinter.SetValue('')

    def TestPrintKitchen(self, e):
        self._database.Printer.SendTestOrder(self.KitchenPrinter.GetValue())

    def TestPrinterCashier(self, e):
        self._database.Printer.SendTestOrder(self.CashPrinter.GetValue())

    def KitchenSelectorOnChange(self, e):
        self._database.Printer.DefaultKitchenPrinter = self.KitchenPrinter.GetValue()

    def CashierSelectorOnChange(self, e):
        self._database.Printer.DefaultCashierPrinter = self.CashPrinter.GetValue()
