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
from Logger import CreateLogger
from logging import Logger
from PySide6 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets, QtPrintSupport


class PrinterControl:
    def __init__(self, logger: Logger, Setting: ConfigSetting):
        if logger is None:
            logger = CreateLogger('test')
        self.logger = logger
        self.Setting = Setting
        self.DefaultKitchenPrinters = {}
        self.DefaultCashierPrinter = None
        self.ReadPrinterConfig()

    def SetDefaultKitchenPrinter(self, value: str, MenuID):
        if value in self.PrinterList():
            self.DefaultKitchenPrinters[MenuID] = value
            MenuName = self.Setting.GetValue(Config.ValueSetting.Manu.EN_NAME)
            self.logger.info(f'change Kitchen {MenuName[MenuID]} printer to {value}')
            self.Setting.SetValue(Config.ValueSetting.Printer.STR_KITCHEN_PRINTER + MenuName[MenuID], value)
        else:
            self.DefaultKitchenPrinters[MenuID] = None
            MenuName = self.Setting.GetValue(Config.ValueSetting.Manu.EN_NAME)
            self.logger.info(f'change Kitchen {MenuName[MenuID]} printer to None')
            self.Setting.SetValue(Config.ValueSetting.Printer.STR_KITCHEN_PRINTER + MenuName[MenuID], None)

    def SetDefaultCashierPrinter(self, value: str):
        if value in self.PrinterList():
            self.DefaultCashierPrinter = value
            self.logger.info(f'change Cashier printer to {value}')
            self.Setting.SetValue(Config.ValueSetting.Printer.STR_CASHIER_PRINTER, value)
        else:
            self.DefaultCashierPrinter = None
            self.logger.info(f'change Cashier printer to None')
            self.Setting.SetValue(Config.ValueSetting.Printer.STR_CASHIER_PRINTER, None)

    def ReadPrinterConfig(self):
        Printerlist = self.PrinterList()
        logstr = 'Read Default Printer: '
        self.DefaultCashierPrinter = self.Setting.GetValue(Config.ValueSetting.Printer.STR_CASHIER_PRINTER)
        if self.DefaultCashierPrinter not in Printerlist:
            self.DefaultCashierPrinter = None
        logstr += f'{Config.ValueSetting.Printer.STR_CASHIER_PRINTER}: {self.DefaultCashierPrinter}, '
        self.DefaultKitchenPrinters = {}
        ManeList = self.Setting.GetValue(Config.ValueSetting.Manu.EN_NAME)
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

    # def PrintReceipt(self, TableInfo: TableInfoStore):
    #     receiptform = ('''<html><body><style type="text/css">.receipt_main {display: grid;width = 100%;
    #     grid-template-columns: 1fr 1fr;align-items: center;}.itemname{flex-wrap: wrap;}
    #     .itemprice{margin-right:0;margin-left: auto;}</style>
    #     <div id="receipt">
    #     <div id="receipt_head" style="text-align: center;">
    #     <div id="icon"><img src="file://{Path_To_LOGO}" style="width:50px;height:50px;"></div>
    #     <div id="address">{ADDRESS}</div>
    #     </div><hr>
    #     <div id="receipt_info">VAT No: {VATNO}<br>Date: {TIME}<br> ORDERID: {ORDERID}<br>Table Number: {TABLE_NUMBER}
    #     </div></div><hr>'''.replace('{Path_To_LOGO}', '').replace('{ADDRESS}', '')
    #                    .replace('{VATNO}', '').replace('{TIME}', '').replace('{ORDERID}', '')
    #                    .replace('{TABLE_NUMBER}', ''))
    #     Total = TableInfo.GetTotalAmount()
    #     for OrderID in TableInfo.Orders:
    #         Order = TableInfo.Orders[OrderID]
    #
    #         receiptform += ('''<div id="item" class="receipt_main">
    #         <div class="itemname">{QTY} x {NAME} {NOTE}</div>
    #         <div class="itemprice">£{PRICE}</div>
    #         </div>'''.replace('{QTY}', str(int(Order.Qty))).replace('{NAME}', Order.NameEN)
    #                         .replace('{NOTE}', Order.Note).replace('{PRICE}', str(round(Order.UnitPrice, 2))))
    #     receiptform += '''<hr><div id='Total' class='receipt_main'>
    #         <div class="itemname">SUBTOTAL</div>
    #         <div class="itemprice">£{TOTAL}</div></div>'''.replace('{TOTAL}', str(round(Total, 2)))
    #     if TableInfo.ServiceCharge != 0:
    #         receiptform += ('''<div id="Total" class="receipt_main">
    #         <div class="itemname">{SERVICE_CHARGE_PERCENT}% Service Charge</div>
    #         <div class="itemprice">£{SERVICE_CHARGE_AMOUNT}</div></div>'''
    #                         .replace('SERVICE_CHARGE_PERCENT}', str(round(TableInfo.ServiceCharge, 1)))
    #                         .replace('{SERVICE_CHARGE_AMOUNT}', str(round(Total * TableInfo.ServiceCharge, 2))))
    #         Total = Total * (1 + TableInfo.ServiceCharge)
    #     DiscountPercent = round(TableInfo.Discount)
    #     if DiscountPercent > 0:
    #         receiptform += ('''<div id='discount' class='receipt_main'>
    #         <div class="itemname">{DISCOUNT_PERCENT}%DISCOUNT</div>
    #         <div class="itemprice">£{DISCOUNT_AMOUNT}}</div></div><br>'''
    #                         .replace('DISCOUNT_PERCENT}', str(round(TableInfo.Discount)))
    #                         .replace('{DISCOUNT_AMOUNT}', str(round(Total * TableInfo.Discount, 2))))
    #         Total = Total * (1 - DiscountPercent)
    #
    #     receiptform += '''<hr><div id="Total" class="receipt_main"><div class="itemname">12.5% VAT included</div></div>
    #     <div id="Total" class="receipt_main"><div class="itemname">TOTAL</div>
    #     <div class="itemprice">£{TOTAL}</div></div><hr>
    #     <div id="receipt_foot" style="text-align: center;">
    #     Thanks for visiting!<br>You can find us on instagram<br> @usagi_animemaid_cafe</div></div></body></html>
    #     '''.replace('{TOTAL}', str(round(Total, 2)))
    #     self.convert_html_to_pdf(receiptform, Config.DataBase.TMP_PRINT_PDF_PATH)

    def LoadReceiptHTML(self, TableInfo: TableInfoStore):
        receiptform = ('''<html><body><style type="text/css">.receipt_main {display: grid;width = 100%;
                                 grid-template-columns: 1fr 1fr;align-items: center;}.itemname{flex-wrap: wrap;}
                                 .itemprice{margin-right:0;margin-left: auto;}</style>
                                 <div id="receipt">
                                 <div id="receipt_head" style="text-align: center;">
                                 <div id="icon"><img src="file://{Path_To_LOGO}" width="50" height="50"></div>
                                 <div id="address">{ADDRESS}</div>
                                 </div><hr>
                                 <div id="receipt_info">VAT No: {VATNO}<br>Date: {TIME}<br>#ORDER: {ORDERID}<br>#Table: {TABLE_NUMBER}
                                 </div></div><hr>'''.replace('{Path_To_LOGO}', 'D:/Code/web_python/App/img/Login.png')
                       .replace('{ADDRESS}', 'Address')
                       .replace('{VATNO}', '')
                       .replace('{TIME}', TableInfo.EndTime)
                       .replace('{ORDERID}', str(TableInfo.OrderID))
                       .replace('{TABLE_NUMBER}', str(TableInfo.TableID)))
        Total = TableInfo.GetTotalAmount()
        receiptform += "<table width='100%'>"
        for OrderID in TableInfo.Orders:
            Order = TableInfo.Orders[OrderID]
            if Order.Qty > 0:
                receiptform += ('''<tr><td style="flex-wrap: wrap;">{QTY} x {NAME} {NOTE}</td>
                 <td style="text-align: right;">£{PRICE}</td>'''
                                .replace('{QTY}', str(int(Order.Qty))).replace('{NAME}', Order.NameEN)
                                .replace('{NOTE}', Order.Note).replace('{PRICE}', str(round(Order.UnitPrice, 2))))
        receiptform += "</table><hr><table width='100%'>"
        receiptform += ('''<tr><td style="flex-wrap: wrap;">SUBTOTAL</td>
                             <td style="text-align: right;">£{TOTAL}</td></tr>'''
                        .replace('{TOTAL}', str(round(Total, 2))))
        if TableInfo.ServiceCharge != 0:
            receiptform += ('''<tr><td style="flex-wrap: wrap;">{SERVICE_CHARGE_PERCENT}% Service Charge</td>
                                     <td style="text-align: right;">
                                     £{SERVICE_CHARGE_AMOUNT}</td></tr>'''
                            .replace('{SERVICE_CHARGE_PERCENT}', str(round(TableInfo.ServiceCharge, 1)))
                            .replace('{SERVICE_CHARGE_AMOUNT}', str(round(Total * TableInfo.ServiceCharge / 100, 2))))
            Total = Total * (1 + TableInfo.ServiceCharge/100)
        DiscountPercent = round(TableInfo.Discount)
        if DiscountPercent > 0:
            receiptform += ('''<tr><td style="flex-wrap: wrap;">{DISCOUNT_PERCENT}%DISCOUNT</td>
                                 <td style="text-align: right;">£{DISCOUNT_AMOUNT}}</td></tr>'''
                            .replace('{DISCOUNT_PERCENT}', str(round(TableInfo.Discount)))
                            .replace('{DISCOUNT_AMOUNT}', str(round(Total * TableInfo.Discount / 100, 2))))
            Total = Total * (1 - DiscountPercent/100)

        receiptform += '''</table><hr><table width='100%'>
                                 <tr><td style="flex-wrap: wrap;">12.5% VAT included</td></tr>
                                 <tr><td style="flex-wrap: wrap;">TOTAL</td>
                                 <td style="text-align: right;">£{TOTAL}</td></tr></table><hr>
                                 <div id="receipt_foot" style="text-align: center;">
                                 Thanks for visiting!</div>
                                 </div></body></html>
                                 '''.replace('{TOTAL}', str(round(Total, 2)))
        self.HTML = receiptform
        return receiptform

    def LoadOrderHTML(self, TableInfo: list, OrderID, TableID):
        receiptform = ('''<html><body>
                                 <div id="receipt_info">#ORDER: {ORDERID}<br>#Table: {TABLE_NUMBER}<br>Date: {TIME}
                                 </div></div><hr>'''.replace('{Path_To_LOGO}', 'D:/Code/web_python/App/img/Login.png')
                       .replace('{TIME}', datetime.datetime.now().strftime('%H:%M:%S'))
                       .replace('{ORDERID}', str(OrderID))
                       .replace('{TABLE_NUMBER}', str(TableID)))
        receiptform += "<table width='100%'>"
        for Order in TableInfo:
            receiptform += ('''<tr><td style="flex-wrap: wrap;">{QTY} x {NAME}</td>
             <td style="text-align: right;">{NOTE}</td>'''
                            .replace('{QTY}', str(int(Order.Qty))).replace('{NAME}', Order.NameEN)
                            .replace('{NOTE}', Order.Note))
        receiptform += '''</table></body></html>'''
        return receiptform

    def Print(self, Html, PrinterName):
        if PrinterName is not None:
            printer = QtPrintSupport.QPrinter()
            printer.setPageMargins(QtCore.QMargins(0, 0, 0, 0), QtGui.QPageLayout.Millimeter)
            printer.setFullPage(True)
            printer.setPrinterName(PrinterName)
            printer.setResolution(80)

            # size = QPageSize(QtCore.QSize(70 * 2.83465, 260 *2.83465))
            # printer.setPageSize(size)
            # self.web_view.print_(printer)

            document = QtGui.QTextDocument()
            document.setPageSize(
                QtCore.QSizeF(printer.width(), printer.height()))
            cursor = QtGui.QTextCursor(document)
            blockFormat = QtGui.QTextBlockFormat()
            cursor.insertBlock(blockFormat)
            cursor.insertHtml(Html)
            blockFormat.setPageBreakPolicy(QtGui.QTextFormat.PageBreak_AlwaysBefore)
            document.print_(printer)

    def PrintReceipt(self, TableInfo):
        try:
            self.logger.info("Print Orders.")
            self.Print(self.LoadReceiptHTML(TableInfo), self.DefaultCashierPrinter)
        except Exception as e:
            self.logger.error("Unknown Error in PrintReceipt", exc_info=e)

    def PrintOrder(self, TableInfo):
        try:
            self.logger.info("Print Orders.")
            OrderDict = {}
            for type in self.DefaultKitchenPrinters:
                if self.DefaultKitchenPrinters[type] is not None:
                    OrderList = list(filter(lambda x: x.FoodType == type, TableInfo.Orders))
                    if len(OrderList) > 0:
                        if self.DefaultKitchenPrinters[type] in OrderDict:
                            OrderDict[self.DefaultKitchenPrinters[type]].extend(OrderList)
                        else:
                            OrderDict[self.DefaultKitchenPrinters[type]] = OrderList
            for PrinterName in OrderDict:
                self.Print(self.LoadOrderHTML(OrderDict[PrinterName], TableInfo.OrderID, TableInfo.TableID),
                           PrinterName)
        except Exception as e:
            self.logger.error("Unknown Error in PrintOrder", exc_info=e)


if __name__ == '__main__':
    Logger = CreateLogger('test')
    setting = ConfigSetting(Logger, 'test/')
    printer = PrinterControl(Logger, setting)
