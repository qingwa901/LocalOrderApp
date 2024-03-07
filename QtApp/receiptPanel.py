# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui/Status.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets, QtPrintSupport
from TableInfoStore import TableInfoStore
from functools import partial


class Receipt(QtWidgets.QFrame):
    def __init__(self, parant):
        QtWidgets.QFrame.__init__(self, parant)
        self.TableNumber = None
        self.setupUi()
        self.HTML = ''

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(468, 1000)
        self.setObjectName("Form")
        self.web_view = QtWebEngineWidgets.QWebEngineView(self)
        # set the widget as the main window's central widget
        vview = QtWidgets.QVBoxLayout(self)
        vview.addWidget(self.web_view)
        self.setLayout(vview)

        QtCore.QMetaObject.connectSlotsByName(self)

    def LoadHtml2(self, TableInfo: TableInfoStore):
        receiptform = ('''<html><body><style type="text/css">.receipt_main {display: grid;width = 100%;
                                grid-template-columns: 1fr 1fr;align-items: center;}.itemname{flex-wrap: wrap;}
                                .itemprice{margin-right:0;margin-left: auto;}</style>
                                <div id="receipt">
                                <div id="receipt_head" style="text-align: center;">
                                <div id="icon"><img src="file://{Path_To_LOGO}" style="width:50px;height:50px;"></div>
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
            Total = Total * (1 + TableInfo.ServiceCharge)
        DiscountPercent = round(TableInfo.Discount)
        if DiscountPercent > 0:
            receiptform += ('''<tr><td style="flex-wrap: wrap;">{DISCOUNT_PERCENT}%DISCOUNT</td>
                                <td style="text-align: right;">£{DISCOUNT_AMOUNT}}</td></tr>'''
                            .replace('{DISCOUNT_PERCENT}', str(round(TableInfo.Discount)))
                            .replace('{DISCOUNT_AMOUNT}', str(round(Total * TableInfo.Discount / 100, 2))))
            Total = Total * (1 - DiscountPercent)

        receiptform += '''</table><hr><table width='100%'>
                                <tr><td style="flex-wrap: wrap;">12.5% VAT included</td></tr>
                                <tr><td style="flex-wrap: wrap;">TOTAL</td>
                                <td style="text-align: right;">£{TOTAL}</td></tr></table><hr>
                                <div id="receipt_foot" style="text-align: center;">
                                Thanks for visiting!<br>You can find us on instagram<br> @usagi_animemaid_cafe</div>
                                </div></body></html>
                                '''.replace('{TOTAL}', str(round(Total, 2)))
        self.HTML = receiptform
        return receiptform

    def LoadHtml(self, TableInfo: TableInfoStore):
        receiptform = ('''<html><body><style type="text/css">.receipt_main {display: grid;width = 100%;
                                grid-template-columns: 1fr 1fr;align-items: center;}.itemname{flex-wrap: wrap;}
                                .itemprice{margin-right:0;margin-left: auto;}</style>
                                <div id="receipt">
                                <div id="receipt_head" style="text-align: center;">
                                <div id="icon"><img src="file://{Path_To_LOGO}" style="width:50px;height:50px;"></div>
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
        for OrderID in TableInfo.Orders:
            Order = TableInfo.Orders[OrderID]

            receiptform += ('''<div id="item" class="receipt_main" style="flex: 1;width = 100%;align-items: center;">
                                    <div class="itemname" style="flex-wrap: wrap;">{QTY} x {NAME} {NOTE}</div>
                                    <div class="itemprice" style="margin-right:0;margin-left: auto;">£{PRICE}</div>
                                    </div>'''.replace('{QTY}', str(int(Order.Qty))).replace('{NAME}', Order.NameEN)
                            .replace('{NOTE}', Order.Note).replace('{PRICE}', str(round(Order.UnitPrice, 2))))
        receiptform += ('''<hr><div id='Total' class='receipt_main' style="display: grid;width = 100%;
                                grid-template-columns: 1fr 1fr;align-items: center;">
                                    <div class="itemname" style="flex-wrap: wrap;">SUBTOTAL</div>
                                    <div class="itemprice" style="margin-right:0;margin-left: auto;">£{TOTAL}</div></div>'''
                        .replace('{TOTAL}', str(round(Total, 2))))
        if TableInfo.ServiceCharge != 0:
            receiptform += ('''<div id="Total" class="receipt_main" style="display: grid;width = 100%;
                                grid-template-columns: 1fr 1fr;align-items: center;">
                                    <div class="itemname" style="flex-wrap: wrap;">{SERVICE_CHARGE_PERCENT}% Service Charge</div>
                                    <div class="itemprice" style="margin-right:0;margin-left: auto;">
                                    £{SERVICE_CHARGE_AMOUNT}</div></div>'''
                            .replace('{SERVICE_CHARGE_PERCENT}', str(round(TableInfo.ServiceCharge, 1)))
                            .replace('{SERVICE_CHARGE_AMOUNT}', str(round(Total * TableInfo.ServiceCharge, 2))))
            Total = Total * (1 + TableInfo.ServiceCharge)
        DiscountPercent = round(TableInfo.Discount)
        if DiscountPercent > 0:
            receiptform += ('''<div id='discount' class='receipt_main' style="display: grid;width = 100%;
                                grid-template-columns: 1fr 1fr;align-items: center;">
                                    <div class="itemname" style="flex-wrap: wrap;">{DISCOUNT_PERCENT}%DISCOUNT</div>
                                    <div class="itemprice" style="margin-right:0;margin-left: auto;">
                                    £{DISCOUNT_AMOUNT}}</div></div><br>'''
                            .replace('{DISCOUNT_PERCENT}', str(round(TableInfo.Discount)))
                            .replace('{DISCOUNT_AMOUNT}', str(round(Total * TableInfo.Discount, 2))))
            Total = Total * (1 - DiscountPercent)

        receiptform += '''<hr><div id="Total" class="receipt_main" style="display: grid;width = 100%;
                                grid-template-columns: 1fr 1fr;align-items: center;">
                                <div class="itemname" style="flex-wrap: wrap;">12.5% VAT included</div></div>
                                <div id="Total" class="receipt_main" style="display: grid;width = 100%;
                                grid-template-columns: 1fr 1fr;align-items: center;">
                                <div class="itemname" style="flex-wrap: wrap;">TOTAL</div>
                                <div class="itemprice" style="margin-right:0;margin-left: auto;">
                                £{TOTAL}</div></div><hr>
                                <div id="receipt_foot" style="text-align: center;">
                                Thanks for visiting!<br>You can find us on instagram<br> @usagi_animemaid_cafe</div>
                                </div></body></html>
                                '''.replace('{TOTAL}', str(round(Total, 2)))
        self.HTML = receiptform
        return receiptform

    def LoadTable(self, TableInfo: TableInfoStore):
        receiptform = self.LoadHtml2(TableInfo)
        self.web_view.setHtml(receiptform)

    def print_me2(self):
        printer = QtPrintSupport.QPrinter()
        printer.setOutputFormat(QtPrintSupport.QPrinter.NativeFormat)
        printer.setPrinterName('ET-2850 Series(Network)')
        painter = QtGui.QPainter(printer)
        # scale = printer.pageRect(QtPrintSupport.QPrinter.Unit.DevicePixel).width() / (self.width()+50)
        # painter.translate(printer.paperRect(QtPrintSupport.QPrinter.Unit.DevicePixel).center())
        # painter.scale(scale, scale)
        # painter.translate((self.width() / 2) * -1, (self.height() / 2) * -1)
        # self.web_view.page().printRequested()
        self.web_view.render(painter, QtCore.QPoint())
        painter.end()

    def print_me3(self):
        printer = QtPrintSupport.QPrinter()
        printer.setOutputFormat(QtPrintSupport.QPrinter.NativeFormat)
        printer.setPrinterName('ET-2850 Series(Network)')
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        blockFormat = QtGui.QTextBlockFormat()
        cursor.insertBlock(blockFormat)
        cursor.insertHtml(self.HTML)
        blockFormat.setPageBreakPolicy(QtGui.QTextFormat.PageBreak_AlwaysBefore)
        document.print_(printer)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Receipt(None)
    ui.show()
    sys.exit(app.exec_())
