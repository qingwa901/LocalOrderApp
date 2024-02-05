import pandas as pd
from Config import Config
from collections import defaultdict


class OrderInfo:
    FoodID = None
    Qty = None
    UnitPrice = None
    StaffID = None
    Note = None
    CreatTime = None
    OrderList = Config.DataBase.OrderList

    def SetOrder(self, Order: pd.Series):
        self.FoodID = Order[self.OrderList.ID_FOOD]
        self.Qty = Order[self.OrderList.QTY]
        self.UnitPrice = Order[self.OrderList.UNIT_PRICE]
        self.StaffID = Order[self.OrderList.ID_STAFF]
        self.Note = Order[self.OrderList.NOTE]
        self.CreatTime = Order[self.OrderList.CREATE_TIME]


class TableInfoStore:
    OrderID = None
    StartTime = None
    EndTime = None
    IsFinished = None
    NumOfPeople = None
    OrderInfo = defaultdict(OrderInfo)
    OrderList = Config.DataBase.OrderList
    OrderMetaList = Config.DataBase.OrderMetaData

    def Clear(self):
        self.StartTime = None
        self.EndTime = None
        self.IsFinished = None
        self.NumOfPeople = None
        self.OrderInfo = defaultdict(OrderInfo)

    def SetMetaInfo(self, Info: pd.Series):
        field = Info[self.OrderMetaList.FIELD]
        value = Info[self.OrderMetaList.VALUE]
        if field == self.OrderMetaList.Fields.IS_FINISHED:
            self.IsFinished = value == 'True'
        elif field == self.OrderMetaList.Fields.START_TIME:
            self.StartTime = value
        elif field == self.OrderMetaList.Fields.END_TIME:
            self.EndTime = value
        elif field == self.OrderMetaList.Fields.NUM_OF_PEOPLE:
            self.NumOfPeople = value

    def SetOrder(self, Order: pd.Series):
        self.OrderID = Order[self.OrderList.ID_ORDER]
        self.OrderInfo[self.OrderID].SetOrder(Order)


class AllTableInfoStore:
    UpdateTime = None
    TableInfo = defaultdict(TableInfoStore)
    OrderList = Config.DataBase.OrderList
    OrderMetaList = Config.DataBase.OrderMetaData
    OrderTableMap = dict()

    def __item__(self, tableID):
        return self.TableInfo[tableID]

    def _AddOrder(self, order: pd.Series):
        TableID = order[self.OrderList.ID_TABLE]
        OrderID = order[self.OrderList.ID_ORDER]
        self.OrderTableMap[OrderID] = TableID
        self.TableInfo[TableID].SetOrder(order)

    def _AddOrderMeta(self, OrderMeta: pd.Series):
        OrderID = OrderMeta[self.OrderMetaList.ID_ORDER]
        if OrderID in self.OrderTableMap:
            self.TableInfo[self.OrderTableMap[OrderID]].SetMetaInfo(OrderMeta)

    def Clear(self):
        for table in self.TableInfo.values():
            table.Clear()
        self.OrderTableMap = dict()

    def ConverOrderData(self, Order: pd.DataFrame, OrderMeta: pd.DataFrame):
        self.Clear()
        Order.apply(self._AddOrder, axis=1)
        OrderMeta.apply(self._AddOrderMeta, axis=1)
