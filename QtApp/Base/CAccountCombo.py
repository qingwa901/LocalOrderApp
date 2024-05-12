from .CComboBox import CComboBox
from Config import Config
from TableInfoStore import TableInfoStore
from typing import Union


class AccountCombo(CComboBox):
    def __init__(self, aParent, *args, **kwargs):
        CComboBox.__init__(self, aParent, *args, **kwargs)
        if aParent is not None:
            self.Logger = aParent.Logger
            self.DataBase = aParent.DataBase
        else:
            self.Logger = None
            self.DataBase = None
        self.AccountID = None
        self.setMinimumWidth(150)
        self.OrderID = None
        self.currentIndexChanged.connect(self.ChangeAccount)
        self.AccountDict = dict()

    def Clear(self):
        self.OrderID = None
        self.AccountID = None
        self.clear()

    def SetUp(self, Table: TableInfoStore):
        self.OrderID = Table.OrderID
        self.AccountID = Table.AccountID
        self.DisplayAccount()

    def DisplayAccount(self):
        OrderAccountList = Config.DataBase.OrderAccountList
        Account = self.DataBase.GetAccountList()
        self.AccountDict = Account.set_index(OrderAccountList.ID)[OrderAccountList.ACCOUNT_NAME].to_dict()
        self.addItem('')
        self.setCurrentText('')
        for i in range(len(Account)):
            data = Account.iloc[i]
            self.addItem(data[OrderAccountList.ACCOUNT_NAME])
            if data[OrderAccountList.ID] == self.AccountID:
                self.setCurrentText(data[OrderAccountList.ACCOUNT_NAME])

    def CurrentAccountID(self) -> Union[int, None]:
        if self.AccountDict is not None:
            for i in self.AccountDict.keys():
                if self.AccountDict[i] == self.currentText():
                    return i
        return None

    def ChangeAccount(self):
        if self.OrderID is not None:
            Account = self.currentText()
            self.DataBase.ChangeAccount(Account, self.OrderID)
