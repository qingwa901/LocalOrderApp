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
from TableInfoStore import TableInfoStore
import pdfkit


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

    def convert_html_to_pdf(self, html_content, pdf_path):
        try:
            pdfkit.from_string(html_content, pdf_path)
            self.logger.info(f"PDF generated and saved at {pdf_path}")
        except Exception as e:
            self.logger.error(f"PDF generation failed at {pdf_path}", exc_info=e)

    def PrintReceipt(self, TableInfo: TableInfoStore):
        receiptform = ('''<html><body><style type="text/css">.receipt_main {display: grid;width = 100%;
        grid-template-columns: 1fr 1fr;align-items: center;}.itemname{flex-wrap: wrap;}
        .itemprice{margin-right:0;margin-left: auto;}</style>
        <div id="receipt">
        <div id="receipt_head" style="text-align: center;">
        <div id="icon"><img src="file://{Path_To_LOGO}" style="width:50px;height:50px;"></div>
        <div id="address">{ADDRESS}</div>
        </div><hr>
        <div id="receipt_info">VAT No: {VATNO}<br>Date: {TIME}<br> ORDERID: {ORDERID}<br>Table Number: {TABLE_NUMBER}
        </div></div><hr>'''.replace('{Path_To_LOGO}', '').replace('{ADDRESS}', '')
                       .replace('{VATNO}', '').replace('{TIME}', '').replace('{ORDERID}', '')
                       .replace('{TABLE_NUMBER}', ''))
        Total = TableInfo.GetTotalAmount()
        for OrderID in TableInfo.Orders:
            Order = TableInfo.Orders[OrderID]

            receiptform += ('''<div id="item" class="receipt_main">
            <div class="itemname">{QTY} x {NAME} {NOTE}</div>
            <div class="itemprice">£{PRICE}</div>
            </div>'''.replace('{QTY}', str(int(Order.Qty))).replace('{NAME}', Order.NameEN)
                            .replace('{NOTE}', Order.Note).replace('{PRICE}', str(round(Order.UnitPrice, 2))))
        receiptform += '''<hr><div id='Total' class='receipt_main'>
            <div class="itemname">SUBTOTAL</div>
            <div class="itemprice">£{TOTAL}</div></div>'''.replace('{TOTAL}', str(round(Total, 2)))
        if TableInfo.ServiceCharge != 0:
            receiptform += ('''<div id="Total" class="receipt_main">
            <div class="itemname">{SERVICE_CHARGE_PERCENT}% Service Charge</div>
            <div class="itemprice">£{SERVICE_CHARGE_AMOUNT}</div></div>'''
                            .replace('SERVICE_CHARGE_PERCENT}', str(round(TableInfo.ServiceCharge, 1)))
                            .replace('{SERVICE_CHARGE_AMOUNT}', str(round(Total * TableInfo.ServiceCharge, 2))))
            Total = Total * (1 + TableInfo.ServiceCharge)
        DiscountPercent = round(TableInfo.Discount)
        if DiscountPercent > 0:
            receiptform += ('''<div id='discount' class='receipt_main'>
            <div class="itemname">{DISCOUNT_PERCENT}%DISCOUNT</div>
            <div class="itemprice">£{DISCOUNT_AMOUNT}}</div></div><br>'''
                            .replace('DISCOUNT_PERCENT}', str(round(TableInfo.Discount)))
                            .replace('{DISCOUNT_AMOUNT}', str(round(Total * TableInfo.Discount, 2))))
            Total = Total * (1 - DiscountPercent)

        receiptform += '''<hr><div id="Total" class="receipt_main"><div class="itemname">12.5% VAT included</div></div>
        <div id="Total" class="receipt_main"><div class="itemname">TOTAL</div>
        <div class="itemprice">£{TOTAL}</div></div><hr>
        <div id="receipt_foot" style="text-align: center;">
        Thanks for visiting!<br>You can find us on instagram<br> @usagi_animemaid_cafe</div></div></body></html>
        '''.replace('{TOTAL}', str(round(Total, 2)))
        self.convert_html_to_pdf(receiptform, Config.DataBase.TMP_PRINT_PDF_PATH)

