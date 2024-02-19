# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 20:21:57 2024

@author: qingw
"""

import win32ui
import win32print
import datetime
from ConfigSetting import ConfigSetting


class PrinterControl:
    def __init__(self, logger, Setting: ConfigSetting):
        self.logger = logger
        self.Setting = Setting
        self._DefaultKitchenPrinter = None
        self._DefaultCashierPrinter = None
        self.ReadConfig()

    def GetDefaultKitchenPrinter(self):
        return self._DefaultKitchenPrinter

    def SetDefaultKitchenPrinter(self, value: str):
        if value in self.PrinterList():
            self._DefaultKitchenPrinter = value
            self.logger.info(f'change Kitchen printer to {value}')
            self.Setting.SetValue('Printer.DefaultKitchenPrinter', value)

    DefaultKitchenPrinter = property(GetDefaultKitchenPrinter, SetDefaultKitchenPrinter)

    def GetDefaultCashierPrinter(self):
        return self._DefaultCashierPrinter

    def SetDefaultCashierPrinter(self, value: str):
        if value in self.PrinterList():
            self._DefaultCashierPrinter = value
            self.logger.info(f'change Cashier printer to {value}')
            self.Setting.SetValue('Printer.DefaultCashierPrinter', value)

    DefaultCashierPrinter = property(GetDefaultCashierPrinter, SetDefaultCashierPrinter)

    def ReadConfig(self):
        list = self.PrinterList()
        if self.Setting.GetValue('Printer.DefaultCashierPrinter') in list:
            self._DefaultCashierPrinter = self.Setting.GetValue('Printer.DefaultCashierPrinter')
        if self.Setting.GetValue('Printer.DefaultKitchenPrinter') in list:
            self._DefaultKitchenPrinter = self.Setting.GetValue('Printer.DefaultKitchenPrinter')

    def PrinterList(self) -> list:
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None,
                                           1)
        return [x[2] for x in printers if 'ONENOTE' not in x[2].upper() and
                'PDF' not in x[2].upper()]

    def SendOrder(self, text, printer):
        self.logger.debug(f'Send text: {text} to {printer}.')
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer)
        font = win32ui.CreateFont({'name': 'Arial', 'height': 60})
        hDC.SelectObject(font)
        hDC.StartDoc("Test doc")
        hDC.StartPage()
        X = 50
        Y = 20
        lines = text.split('\n')
        for line in lines:
            w = 0
            while w < len(line):
                hDC.TextOut(X, Y, line[w: w + 18])
                Y += 100
        hDC.EndPage()
        hDC.EndDoc()

    def SendTestOrder(self, printer: str):
        self.logger.info(f'Send Test order to {printer}.')
        self.SendOrder(f"Printer: {printer}\nTime:"
                       f"{datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')}"
                       f"\nThis is a test print.", printer)
