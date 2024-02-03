# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 20:21:57 2024

@author: qingw
"""


import win32ui
import win32print
import datetime


class PrinterControl:
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config['printer']

    def ReadConfig(self):
        self.DefaultCashierPrinter = self.config['DefaultCashierPrinter']
        self.DefaultKitchenPrinter = self.config['DefaultKitchenPrinter']

    def PrinterList(self):
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None,
                                           1)
        return [x[2] for x in printers if not 'ONENOTE' not in x.upper() and
                'PDF' not in x.upper()]

    def SendOrder(self, text, printer):
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
                hDC.TextOut(X, Y, line[w: w+18])
                Y += 100
        hDC.EndPage()
        hDC.EndDoc()

    def SendTestOrder(self, printer):
        self.SendOrder(f"Printer: {printer}\nTime:"
                       f"{datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')}"
                       f"\nThis is a test print.")
