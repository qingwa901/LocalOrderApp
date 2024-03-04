# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 20:21:57 2024

@author: qingw
"""

import win32ui
import win32print
import datetime
from ConfigSetting import ConfigSetting
from Config import Config


class PrinterControl:
    def __init__(self, logger, Setting: ConfigSetting):
        self.logger = logger
        self.Setting = Setting
        self.DefaultKitchenPrinters = {}
        self.DefaultCashierPrinter = None
        self.ReadPrinterConfig()

    def SetDefaultKitchenPrinter(self, value: str, MenuID):
        if value in self.PrinterList():
            self.DefaultKitchenPrinters[MenuID] = value
            MenuName = Config.DisplaySetting.MenuPage.MENU_EN_NAME[MenuID]
            self.logger.info(f'change Kitchen {MenuName} printer to {value}')
            self.Setting.SetValue(Config.ValueSetting.Printer.STR_KITCHEN_PRINTER + MenuName, value)

    def SetDefaultCashierPrinter(self, value: str):
        if value in self.PrinterList():
            self.DefaultCashierPrinter = value
            self.logger.info(f'change Cashier printer to {value}')
            self.Setting.SetValue(Config.ValueSetting.Printer.STR_CASHIER_PRINTER, value)

    def ReadPrinterConfig(self):
        Printerlist = self.PrinterList()
        logstr = 'Read Default Printer: '
        self.DefaultCashierPrinter = self.Setting.GetValue(Config.ValueSetting.Printer.STR_CASHIER_PRINTER)
        if self.DefaultCashierPrinter not in Printerlist:
            self.DefaultCashierPrinter = None
        logstr += f'{Config.ValueSetting.Printer.STR_CASHIER_PRINTER}: {self.DefaultCashierPrinter}, '
        self.DefaultKitchenPrinters = {}
        ManeList = Config.DisplaySetting.MenuPage.MENU_EN_NAME
        for i in ManeList:
            self.DefaultKitchenPrinters[i] = self.Setting.GetValue(
                Config.ValueSetting.Printer.STR_KITCHEN_PRINTER + ManeList[i])
            if self.DefaultKitchenPrinters[i] is not None and self.DefaultKitchenPrinters[i] not in Printerlist:
                self.DefaultKitchenPrinters[i] = None
            logstr += \
                f'{Config.ValueSetting.Printer.STR_KITCHEN_PRINTER + ManeList[i]}: {self.DefaultKitchenPrinters[i]}, '
        self.logger.info(logstr)

    def PrinterList(self) -> list:
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None,
                                           1)
        return [x[2] for x in printers if 'ONENOTE' not in x[2].upper() and
                'PDF' not in x[2].upper()]

    def SendOrder(self, text, printer):
        if printer is not None:
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
                    w += 18
            hDC.EndPage()
            hDC.EndDoc()

    def SendTestOrder(self, printer: str, info: str):
        self.logger.info(f'Send {info} Test order to {printer}.')
        self.SendOrder(f"Printer: {printer}\nTime:"
                       f"{datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')}"
                       f"\nThis is a {info} test print.", printer)
