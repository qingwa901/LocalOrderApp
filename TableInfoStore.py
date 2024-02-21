import pandas as pd
from Config import Config
from collections import defaultdict
from MenuStore import FullMenuList


class OrderInfo:
    ID = None
    OrderID = None
    FoodID = None
    NameCN = None
    NameEN = None
    Qty = None
    UnitPrice = None
    OriUnitPrice = None
    StaffID = None
    Note = None
    CreateTime = None
    OrderList = Config.DataBase.OrderList

    def SetOrder(self, Order: pd.Series):
        self.ID = Order[self.OrderList.ID]
        self.OrderID = Order[self.OrderList.ID_ORDER]
        self.FoodID = Order[self.OrderList.ID_FOOD]
        self.Qty = Order[self.OrderList.QTY]
        self.UnitPrice = Order[self.OrderList.UNIT_PRICE]
        self.StaffID = Order[self.OrderList.ID_STAFF]
        self.Note = Order[self.OrderList.NOTE]
        self.CreateTime = Order[self.OrderList.CREATE_TIME]

    def getValue(self, Tag):
        conf = Config.DataBase.OrderList
        if Tag == conf.ID_FOOD:
            return self.FoodID
        elif Tag == conf.QTY:
            return self.Qty
        elif Tag == conf.NOTE:
            return self.Note
        elif Tag == conf.UNIT_PRICE:
            return self.UnitPrice

    def LoadMenu(self, menu: FullMenuList):
        m = menu.Foods[self.FoodID]
        self.NameCN = m.NameCN
        self.NameEN = m.NameEN
        self.OriUnitPrice = m.UnitPrice


class TableInfoStore():
    OrderID = None
    TableID = None
    StartTime = None
    EndTime = None
    IsFinished = False
    NumOfPeople = None
    OrderList = Config.DataBase.OrderList
    OrderMetaList = Config.DataBase.OrderMetaData
    Orders = {}

    def Clear(self):
        self.StartTime = None
        self.EndTime = None
        self.OrderID = None
        self.IsFinished = False
        self.NumOfPeople = None
        self.TableID = None
        self.Orders = {}

    def SetMetaInfo(self, Info: pd.Series):
        field = Info[self.OrderMetaList.FIELD]
        value = Info[self.OrderMetaList.VALUE]
        self.OrderID = Info[self.OrderMetaList.ID_ORDER]
        if field == self.OrderMetaList.Fields.IS_FINISHED:
            self.IsFinished = value == 'True'
        elif field == self.OrderMetaList.Fields.START_TIME:
            self.StartTime = value
        elif field == self.OrderMetaList.Fields.END_TIME:
            self.EndTime = value
        elif field == self.OrderMetaList.Fields.NUM_OF_PEOPLE:
            self.NumOfPeople = value
        elif field == self.OrderMetaList.Fields.ID_TABLE:
            self.TableID = value

    def SetOrder(self, Order: pd.Series):
        self.OrderID = Order[self.OrderList.ID_ORDER]
        ID = Order[self.OrderList.ID]
        if pd.isna(ID):
            return
        if ID not in self.Orders:
            self.Orders[ID] = OrderInfo()
        self.Orders[ID].SetOrder(Order)

    def LoadMenu(self, menu:FullMenuList):
        for i in self.Orders.values():
            i.LoadMenu(menu)

class AllTableInfoStore():
    UpdateTime = None
    OrderList = Config.DataBase.OrderList
    OrderMetaList = Config.DataBase.OrderMetaData
    OnlineOrderTableMap = dict()
    OfflineOrderTableMap = dict()
    ByOrderIDDict = defaultdict(TableInfoStore)
    ByTableIDDict = defaultdict(TableInfoStore)

    def _AddOrder(self, order: pd.Series):
        OrderID = order[self.OrderList.ID_ORDER]
        self.ByOrderIDDict[OrderID].SetOrder(order)

    def _AddOrderMeta(self, OrderMeta: pd.Series):
        OrderID = OrderMeta[self.OrderMetaList.ID_ORDER]
        self.ByOrderIDDict[OrderID].SetMetaInfo(OrderMeta)
        if OrderMeta[self.OrderMetaList.FIELD] == self.OrderMetaList.Fields.ID_TABLE:
            self.ByTableIDDict[int(OrderMeta[self.OrderMetaList.VALUE])] = self.ByOrderIDDict[OrderID]

    def Clear(self):
        for table in self.ByTableIDDict.values():
            table.Clear()
        self.ByTableIDDict.clear()
        self.ByOrderIDDict.clear()

    def ConverOrderData(self, Order: pd.DataFrame, OrderMeta: pd.DataFrame):
        self.Clear()
        self.AddOrderMetaInfo(OrderMeta)
        self.AddOrderInfo(Order)

    def AddOrderInfo(self, Order):
        Order.apply(self._AddOrder, axis=1)

    def AddOrderMetaInfo(self, OrderMeta):
        OrderMeta.apply(self._AddOrderMeta, axis=1)

    def LoadMenu(self, menu):
        for i in self.ByOrderIDDict.values():
            i.LoadMenu(menu)