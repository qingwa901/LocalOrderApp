from QtApp.CEODPanelBase import CEODPanelBase


class CEODPanel(CEODPanelBase):
    def __init__(self, aParent):
        CEODPanelBase.__init__(self, aParent)
        self.data = None
        self.TotalCard = 0
        self.TotalCash = 0
        self.PreviousCashBox = 0
        self.Total = 0

    def Load(self):
        data = self.DataBase.GetHistoryOrders()
        for order in data.ByOrderIDDict.values():
            self.Total += order.GetTotalAmount()
            self.TotalCash += order.Cash
            self.TotalCard += order.Card
        self.LBTotalCash.setText(self.TotalCash)
        self.LBTodayTotalCash.setText(self.TotalCard)
        self.LBTotalIncome.setText(self.Total)
        CashDict = self.DataBase.LoadCashBoxAmount()
        for i in self.Values:
            if i in CashDict:
                self.Values[i].setText(str(int(CashDict[i])))
            else:
                self.Values[i].setText(0)
        self.Summary()

    def Summary(self):
        self.realTotal = 0
        for i in self.Values:
            self.realTotal += i * self.Values[i].value()
        self.LBRealTotalCash.setText(str(round(self.realTotal, 2)))
        self.LBTotalCash.setText(
            str(round(float(self.LBTodayTotalCash.text()) + self.EditMoneyIn.value() - self.EditMoneyOut.value(), 2)))
        self.LBCashMismatch.setText(str(round(float(self.LBTotalCash) - float(self.LBRealTotalCash), 2)))
        self.LBCardMismatch.setText(str(round(float(self.LBTotalCard) - float(self.LBRealTotalCard), 2)))

    def Save(self):
        pass
