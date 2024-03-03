import pandas as pd
from Config import Config
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


class TableInfoStore:
    OrderList = Config.DataBase.OrderList
    OrderMetaList = Config.DataBase.OrderMetaData

    def __init__(self):
        self.Clear()

    def Clear(self):
        self.Orders = {}
        self.OrderID = None
        self.TableID = None
        self.StartTime = None
        self.EndTime = None
        self.IsFinished = False
        self.NumOfPeople = None
        self.Cash = 0
        self.Card = 0
        self.ServiceCharge = 0
        self.Discount = 0

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
        elif field == self.OrderMetaList.Fields.CARD:
            self.Card = round(float(value), 2)
        elif field == self.OrderMetaList.Fields.CASH:
            self.Cash = round(float(value), 2)
        elif field == self.OrderMetaList.Fields.DISCOUNT_PERCENT:
            self.Discount = int(value)
        elif field == self.OrderMetaList.Fields.SERVICE_CHARGE_PERCENT:
            self.ServiceCharge = int(value)

    def SetOrder(self, Order: pd.Series):
        self.OrderID = Order[self.OrderList.ID_ORDER]
        ID = Order[self.OrderList.ID]
        if pd.isna(ID):
            return
        if ID not in self.Orders:
            self.Orders[ID] = OrderInfo()
        self.Orders[ID].SetOrder(Order)

    def LoadMenu(self, menu: FullMenuList):
        for i in self.Orders.values():
            i.LoadMenu(menu)

    def GetTotalAmount(self):
        total = 0
        for order in self.Orders.values():
            total += order.UnitPrice * order.Qty
        return total


class AllTableInfoStore:
    UpdateTime = None
    OrderList = Config.DataBase.OrderList
    OrderMetaList = Config.DataBase.OrderMetaData
    OnlineOrderTableMap = dict()
    OfflineOrderTableMap = dict()
    ByOrderIDDict = {}
    ByTableIDDict = {}

    def __init__(self, logger):
        self.logger = logger

    def _AddOrder(self, order: pd.Series):
        self.logger.debug(f"Order added. ID: {order[self.OrderList.ID]}, OrderID: {order[self.OrderList.ID_ORDER]}")
        OrderID = order[self.OrderList.ID_ORDER]
        if OrderID not in self.ByOrderIDDict:
            self.ByOrderIDDict[OrderID] = TableInfoStore()
        self.ByOrderIDDict[OrderID].SetOrder(order)

    def _AddOrderMeta(self, OrderMeta: pd.Series):
        self.logger.debug(f"Order Meta added: ID: {OrderMeta[self.OrderMetaList.ID]}, "
                          f"OrderID: {OrderMeta[self.OrderMetaList.ID_ORDER]}, "
                          f"Field: {OrderMeta[self.OrderMetaList.FIELD]}, "
                          f"Value: {OrderMeta[self.OrderMetaList.VALUE]}")
        OrderID = OrderMeta[self.OrderMetaList.ID_ORDER]
        if OrderID not in self.ByOrderIDDict:
            self.ByOrderIDDict[OrderID] = TableInfoStore()
        self.ByOrderIDDict[OrderID].SetMetaInfo(OrderMeta)
        if OrderMeta[self.OrderMetaList.FIELD] == self.OrderMetaList.Fields.ID_TABLE:
            self.ByTableIDDict[int(OrderMeta[self.OrderMetaList.VALUE])] = self.ByOrderIDDict[OrderID]

    def Clear(self):
        self.logger.debug('Clear Tableinfo')
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
