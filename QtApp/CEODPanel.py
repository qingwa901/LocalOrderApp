import pandas as pd
from Config import Config

from QtApp.CEODPanelBase import CEODPanelBase


class CEODPanel(CEODPanelBase):
    def __init__(self, aParent):
        CEODPanelBase.__init__(self, aParent)
        self.data = None
        self.TotalCard = 0
        self.TotalCash = 0
        self.PreviousCashBox = 0
        self.Total = 0
        self.ConnectSummary()
        self.BtnReset.pressed.connect(self.reset)
        self.BtnConfirm.pressed.connect(self.Save)

    def reset(self):
        self.EditMoneyIn.setText("0")
        self.EditMoneyOut.setText("0")
        self.EditRealTotalCard.setText("0")
        self.Load()

    def Load(self):
        self.Total = 0
        self.TotalCard = 0
        self.TotalCash = 0
        self.PreviousCashBox = 0
        data = self.DataBase.GetHistoryOrders()
        for order in data.ByOrderIDDict.values():
            if order.IsFinished:
                self.Total += round(order.GetTotalAmount() * (1 - order.Discount / 100) * (1 + order.ServiceCharge / 100),2)
                self.TotalCash += order.Cash
                self.TotalCard += order.Card
        self.LBTotalCard.setText(str(round(self.TotalCard, 2)))
        self.LBTodayTotalCash.setText(str(round(self.TotalCash, 2)))
        self.LBTotalIncome.setText(str(round(self.Total, 2)))
        CashDict = self.DataBase.LoadCashBoxAmount()
        for i in self.Values:
            if str(float(i)) in CashDict:
                self.Values[i].setText(str(int(CashDict[str(float(i))])))
                self.PreviousCashBox += int(CashDict[str(float(i))]) * i
            elif i in CashDict:
                self.Values[i].setText(str(int(CashDict[i])))
                self.PreviousCashBox += int(CashDict[i]) * i
            else:
                self.Values[i].setText('0')
        self.Summary()

    def ConnectSummary(self):
        for i in self.Values.values():
            i.textChanged[str].connect(self.Summary)
        self.EditMoneyOut.textChanged[str].connect(self.Summary)
        self.EditMoneyIn.textChanged[str].connect(self.Summary)
        self.EditRealTotalCard.textChanged[str].connect(self.Summary)

    def SetUpOpenKeyboardEvent(self, Event):
        for i in self.Values.values():
            i.OpenKeyboardEvent = Event
        self.EditMoneyOut.OpenKeyboardEvent = Event
        self.EditMoneyIn.OpenKeyboardEvent = Event
        self.EditRealTotalCard.OpenKeyboardEvent = Event

    def Summary(self, e=None):
        self.realTotal = 0
        for i in self.Values:
            self.realTotal += i * self.Values[i].value()
        self.LBRealTotalCash.setText(str(round(self.realTotal, 2)))
        self.LBTotalCash.setText(
            str(round(float(
                self.LBTodayTotalCash.text()) + self.EditMoneyIn.value() - self.EditMoneyOut.value() + self.PreviousCashBox,
                      2)))
        RealTotalIncome = self.EditRealTotalCard.value() + float(
            self.LBRealTotalCash.text()) - self.EditMoneyIn.value() + self.EditMoneyOut.value() - self.PreviousCashBox
        self.LBRealTotalIncome.setText(str(round(RealTotalIncome, 2)))
        self.LBCashMismatch.setText(
            str(round(round(float(self.LBRealTotalCash.text()), 2) - float(self.LBTotalCash.text()), 2)))
        self.LBCardMismatch.setText(
            str(round(round(self.EditRealTotalCard.value(), 2) - float(self.LBTotalCard.text()), 2)))
        self.LBIncomeMismatch.setText(
            str(round(round(float(self.LBRealTotalIncome.text()), 2) - float(self.LBTotalIncome.text()), 2)))

    def GetCoinData(self):
        Res = {}
        for i in self.Values:
            Res[i] = float(self.Values[i].text())
        return Res

    def GetSummaryData(self):
        table = Config.DataBase.EODSummary
        Res = {}
        Res[table.MONEY_IN] = self.EditMoneyIn.value()
        Res[table.MONEY_OUT] = self.EditMoneyOut.value()
        Res[table.REAL_CARD] = self.EditRealTotalCard.value()
        Res[table.REAL_CASH] = float(self.LBRealTotalCash.text())
        Res[table.RECORD_CARD] = float(self.LBTotalCard.text())
        Res[table.RECORD_CASH] = float(self.LBTotalCash.text())
        Res[table.RECORD_INCOME] = float(self.LBTotalIncome.text())
        Res[table.REAL_INCOME] = float(self.LBRealTotalIncome.text())
        return Res

    def Save(self):
        CoinData = self.GetCoinData()
        self.DataBase.SaveCoinInfo(CoinData)
        self.DataBase.SaveEODSummary(self.GetSummaryData())
        self.DataBase.SaveTodayDataToHistoryTable()
        self.reset()
