# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 21:40:23 2024

@author: qingw
"""
import os
import time
from SQLControl import SQLControl
from Config import Config
from ConfigSetting import ConfigSetting
import pandas as pd
import threading
from datetime import datetime, timezone
from PrinterControl import PrinterControl
import logging
import json
from TableInfoStore import AllTableInfoStore, OrderInfo, TableInfoStore
from MenuStore import FullMenuList
import sqlite3
import copy


class DataBase(SQLControl):
    def __init__(self, logger: logging.Logger, path):
        SQLControl.__init__(self, logger)
        self.logger = logger
        self.config = Config.DataBase
        self.Setting = ConfigSetting(logger)
        self.STORE_ID = self.config.STORE_ID  # Todo save store id to setting file
        self.DataBaseCheck()
        self.MenuPageLoad = threading.Thread(target=self.LoadMenuPage)
        self.MenuPageLoad.start()
        self.StaffLoad = threading.Thread(target=self.LoadStaffInfo)
        self.StaffLoad.start()
        self.TableInfoLock = threading.Lock()
        self.TableInfo = AllTableInfoStore(self.logger)
        self.OpenPanel = []
        self.path = path
        self.StaffName = None
        self.StaffList = {}
        self.menu = FullMenuList()
        LoadStoreInfo = threading.Thread(target=self.LoadStoreInfo)
        LoadStoreInfo.start()
        self.MenuPageLoad.join()
        self.MenuLoad = threading.Thread(target=self.RefreshMenu)
        self.MenuLoad.start()
        self.auto_update = threading.Thread(target=self.AutoUpdate)
        self.auto_update.start()
        self.MaxOrderID = None
        self.MaxOrderListID = None
        self.MaxOrderMataListID = None
        self.Printer = PrinterControl(self.logger, self.Setting)
        self.StaffLoad.join()
        self.MenuLoad.join()
        LoadStoreInfo.join()

    def LoadStoreInfo(self):
        try:
            data = self.get_data(
                f"select * from {self.config.STORE_INFO} where {self.config.StoreList.ID} = '{self.STORE_ID}';")
            if len(data) == 0:
                raise AttributeError(
                    f'Can not find data in Store List. Please check database setting for Store ({self.STORE_ID})')
            data = data.iloc[0]
            self.Setting.SetValue(self.config.StoreList.TABLE_ORDER,
                                  json.loads(data[self.config.StoreList.TABLE_ORDER]))
        except Exception as e:
            self.logger.error('online StoreInfo Load failed.', exc_info=e)

    def LoadStaffInfo(self):
        query = (f"select * from {self.config.Staff.NAME} where `{self.config.Staff.ID_STORE}` = '{self.STORE_ID}' and "
                 f"`{self.config.Staff.VALID}` = '1';")

        try:
            with self.Lock:
                self.logger.info(query)
                data = pd.read_sql(query, self.conn)
                self.SaveStaff(data)
                self.logger.info('Online staff list loaded.')
        except Exception as e:
            self.logger.error('Connection issue try to load local staff', exc_info=e)
            with self.LocalLock:
                with sqlite3.connect(Config.DataBase.PATH) as conn:
                    self.logger.info(f'query: {query}')
                    data = pd.read_sql(query, conn)
                    self.logger.info('Local staff loaded.')
        self.StaffList = data.set_index(self.config.Staff.STAFF_NAME)[self.config.Staff.ID].to_dict()

    def LoadMenuPage(self):

        try:
            query = (
                f"select * from {self.config.ManuPageList.NAME} where `{self.config.ManuPageList.ID_STORE}` = '"
                f"{self.STORE_ID}' and `{self.config.ManuPageList.VALID}` = '1'")
            self.logger.info(query)
            with self.Lock:
                data = pd.read_sql(query, self.conn)
            data = data.set_index(self.config.ManuPageList.ID)
            self.Setting.SetValue(Config.ValueSetting.Manu.EN_NAME,
                                  data[self.config.ManuPageList.EN_NAME].to_dict())
            self.Setting.SetValue(Config.ValueSetting.Manu.CN_NAME,
                                  data[self.config.ManuPageList.CN_NAME].to_dict())
        except Exception as e:
            self.logger.error('Connection issue during loading menu page. Start to use previous setting',
                              exc_info=e)

    def RefreshMenu(self):
        query = (f"select * from {self.config.MenuList.NAME} where {self.config.MenuList.ID_STORE} = "
                 f"'{self.STORE_ID}' and `{self.config.MenuList.VALID}` = '1'")

        try:
            self.logger.info(query)
            with self.Lock:
                data = pd.read_sql(query, self.conn)
                self.SaveMenu(data)
        except Exception as e:
            self.logger.error('Connection issue try to load local menu', exc_info=e)
            with self.LocalLock:
                with sqlite3.connect(Config.DataBase.PATH) as conn:
                    self.logger.info(f'query: {query}')
                    data = pd.read_sql(query, conn)
                    self.logger.info('Local menu loaded.')
        self.menu.clear()
        self.menu.setUp(data)

    def HardReloadData(self):
        self.LoadMenuPage()
        self.RefreshMenu()
        self.LoadStaffInfo()
        self.LoadStoreInfo()
        for i in self.config.TABLE_LIST:
            self.HardLoadData(i, True)

    def SaveMenu(self, data: pd.DataFrame):
        table = self.config.MenuList.NAME
        self.executeLocally(f'DELETE FROM {table} where 1=1')
        self.SaveLocalData(data, table)

    def SaveStaff(self, data: pd.DataFrame):
        table = self.config.Staff.NAME
        self.executeLocally(f'DELETE FROM {table} where 1=1')
        self.SaveLocalData(data, table)

    def UpdateOneLineLocally(self, data, table):
        Value = ''
        for field in table.COLUMNS:
            if Value != '':
                Value += ', '
            Value += f"`{field}`='{data[field]}'"
        self.executeLocally(
            f"Update {table.NAME} Set {Value}, `{self.config.UPDATED}`='1', `{self.config.LOADED}`='1' "
            f"where {table.ID_STORE} = {self.STORE_ID} and {table.ID} = {data[table.ID]}")

    def UpdateOneLine(self, data, table):
        if data[table.VALID]:
            Value = ''
            for field in table.COLUMNS:
                if Value != '':
                    Value += ', '
                Value += f"`{field}` = '{data[field]}'"
            self.execute(
                f"Update {table.NAME} Set {Value}, `{self.config.UPDATED}`=true, `{self.config.LOADED}`=true "
                f"where {table.ID_STORE} = {self.STORE_ID} and {table.ID} = {data[table.ID]}")
        else:
            query = f"delete from {table.NAME} where `{table.ID}`='{data[table.ID]}';"
            self.execute(query)
            self.executeLocally(query)

    def Update_(self):
        for table in [self.config.OrderList, self.config.OrderMetaData, self.config.HistoryOrderList,
                      self.config.HistoryOrderMetaData, self.config.CashBoxAmount, self.config.EODSummary,
                      self.config.OrderAccountList]:
            data = self.get_local_data(
                f"select * from {table.NAME} where {self.config.LOADED}='0' and {table.ID_STORE}={self.STORE_ID};")
            if len(data) > 0:
                data[self.config.LOADED] = True
                data[self.config.UPDATED] = True
                ExistIDList = self.IsDataExist(data[table.ID].to_list(), table, True)
                ExistData = data[data[table.ID].isin(ExistIDList)]
                if len(ExistData) > 0:
                    ExistData.apply(self.UpdateOneLine, axis=1, table=table)
                NewData = data[~data[table.ID].isin(ExistIDList)]
                NewValidData = NewData[NewData[table.VALID] == 1]
                NewInvalidData = NewData[NewData[table.VALID] == 0]
                if len(NewValidData) > 0:
                    self.SaveData(NewValidData, table.NAME)
                if len(NewInvalidData) > 0:
                    for RowID in NewInvalidData[table.ID].to_list():
                        query = (f"delete from {table.NAME} where `{table.ID}`='{RowID}' and "
                                 f"`{table.ID_STORE}`='{self.STORE_ID}';")
                        self.executeLocally(query)
                IDstr = "','".join(data[table.ID].astype(str))
                self.executeLocally(
                    f"update {table.NAME} set {self.config.LOADED}='1', {self.config.UPDATED}='1' where {table.ID_STORE} = "
                    f"{self.STORE_ID} and {table.ID} in ('{IDstr}')")

    def Download_(self):
        for table in [self.config.OrderList, self.config.OrderMetaData, self.config.PendingOnlineOrder,
                      self.config.HistoryOrderList, self.config.HistoryOrderMetaData, self.config.CashBoxAmount,
                      self.config.EODSummary, self.config.OrderAccountList]:
            data = self.get_data(
                f"select * from {table.NAME} where {self.config.LOADED}='0' and {table.ID_STORE}={self.STORE_ID};")
            if len(data) > 0:
                data[self.config.LOADED] = True
                data[self.config.UPDATED] = True
                ExistIDList = self.IsDataExist(data[table.ID].to_list(), table, False)
                ExistData = data[data[table.ID].isin(ExistIDList)]
                if len(ExistData) > 0:
                    ExistData.apply(self.UpdateOneLineLocally, axis=1, table=table)
                NewData = data[~data[table.ID].isin(ExistIDList)]
                if len(NewData) > 0:
                    self.SaveLocalData(NewData, table.NAME)

                self.execute(f"update {table.NAME} set {self.config.LOADED}='1', {self.config.UPDATED}='1' where "
                             f"{table.ID_STORE}={self.STORE_ID} and {table.ID} in "
                             f"({','.join(data[table.ID].astype(str))})")

            if table == self.config.PendingOnlineOrder:
                if len(data) > 0:
                    OrderData = data.apply(self.OnlineOrderConvert, axis=1)
                    self.SaveOrdersLocal(OrderData)
                    OrderData.apply(self._PrintOrder, axis=1)

    def IsDataExist(self, IDList, table, IsOnline=True):
        if len(IDList) == 0:
            return []
        IDListStr = "', '".join(map(str, IDList))
        if IsOnline:
            data = self.get_data(f"select {table.ID} from {table.NAME} where {table.ID} in ('{IDListStr}');")
        else:
            data = self.get_local_data(f"select {table.ID} from {table.NAME} where {table.ID} in ('{IDListStr}');")
        return data[table.ID].to_list()

    def SaveOrdersLocal(self, OrderData: pd.DataFrame):
        OrderData[self.config.LOADED] = False
        OrderData[self.config.UPDATED] = False
        OrderData[self.config.OrderList.ID_STORE] = self.STORE_ID
        OrderData[self.config.OrderList.CREATE_TIME] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        self.SaveLocalData(OrderData, self.config.OrderList.NAME)

    def _PrintOrder(self, Order):
        table = self.config.OrderList
        Name = self.menu.Foods[Order[table.ID_FOOD]].NameCN
        TableID = self.TableInfo.ByOrderIDDict[Order[table.ID_ORDER]].TablID
        Qty = Order[table.QTY]
        Note = Order[table.NOTE]
        Time = datetime.now()
        Type = self.menu.Foods[Order[table.ID_FOOD]].Type
        text = f'''Table: {TableID}
{Name}   X   {Qty}
{Note}
{Time}'''
        if Type in self.Setting.GetValue(Config.ValueSetting.Manu.EN_NAME):
            self.Printer.SendOrder(text, self.Printer.DefaultKitchenPrinters[Type])
        else:
            self.Printer.SendOrder(text, self.Printer.DefaultCashierPrinter)

    def AutoUpdate(self):
        while self.open:
            try:
                self.Download_()
                self.Update_()
            except Exception as e:
                self.logger.error('Unknown Error. Retry in 3 sec.', exc_info=e)
            finally:
                for _ in range(3):
                    time.sleep(1)
                    if not self.open:
                        break

    def GetOpenTableInfo2(self) -> AllTableInfoStore:
        with self.TableInfoLock:
            table = Config.DataBase.OrderMetaData
            query = (f"select {table.ID_ORDER} from {table.NAME} where "
                     f"{table.FIELD}='{table.Fields.IS_FINISHED}' and "
                     f"{table.VALUE}='False' and "
                     f"{table.ID_STORE}='{self.STORE_ID}' and {table.VALID}='1';")
            OpenTable = self.get_local_data(query)
            OpenOrderList = OpenTable[Config.DataBase.OrderMetaData.ID_ORDER].astype(str).to_list()
            TableInfo = AllTableInfoStore(self.logger)
            query = (f"select * from {table.NAME} where {table.ID_ORDER} in ({','.join(OpenOrderList)})"
                     f" and {table.VALID} = true;")
            OrderMetaData = self.get_local_data(query)
            TableInfo.AddOrderMetaInfo(OrderMetaData)
            query = (f"select * from {Config.DataBase.OrderList.NAME} where {Config.DataBase.OrderList.ID_ORDER} "
                     f"in ({','.join(OpenOrderList)})")
            OrderList = self.get_local_data(query)
            if len(OrderList) > 0:
                TableInfo.AddOrderInfo(OrderList)
            TableInfo.LoadMenu(self.menu)
            return TableInfo

    def GetTakeAwayOrders(self) -> AllTableInfoStore:
        with self.TableInfoLock:
            table = Config.DataBase.OrderMetaData
            query = (f"select {table.ID_ORDER} from {table.NAME} where "
                     f"{table.FIELD}='{table.Fields.ID_TABLE}' and "
                     f"{table.VALUE}='0' and "
                     f"{table.ID_STORE}='{self.STORE_ID}' and {table.VALID}='1';")
            OpenTable = self.get_local_data(query)
            OpenOrderList = OpenTable[Config.DataBase.OrderMetaData.ID_ORDER].astype(str).to_list()

            TableInfo = AllTableInfoStore(self.logger)
            if len(OpenOrderList) == 0:
                return TableInfo
            query = (f"select * from {table.NAME} where {table.ID_ORDER} in ({','.join(OpenOrderList)})"
                     f" and {table.VALID} = true;")
            OrderMetaData = self.get_local_data(query)
            TableInfo.AddOrderMetaInfo(OrderMetaData)
            query = (f"select * from {Config.DataBase.OrderList.NAME} where {Config.DataBase.OrderList.ID_ORDER} "
                     f"in ({','.join(OpenOrderList)})")
            OrderList = self.get_local_data(query)
            if len(OrderList) > 0:
                TableInfo.AddOrderInfo(OrderList)
            TableInfo.LoadMenu(self.menu)
            return TableInfo

    def SetUpTableColorUpdate(self, Event):
        self.color_auto_update = threading.Thread(target=self.AutoUpdateTableColor, args=[Event])
        self.color_auto_update.start()

    def AutoUpdateTableColor(self, Event):
        while self.open:
            try:
                TableInfo = self.GetOpenTableInfo2()
                Event(TableInfo)
            except Exception as e:
                self.logger.error(f'Error during AotoUpdateTableColor',
                                  exc_info=e)
            finally:
                time.sleep(2)

    def SetUpTakeAwayUpdate(self, Event):
        self.TakeAwayUpdate = threading.Thread(target=self.AotoUpdateTakeAway, args=[Event])
        self.TakeAwayUpdate.start()

    def AotoUpdateTakeAway(self, Event):
        while self.open:
            try:
                Event()
            except Exception as e:
                self.logger.error(f'Error during AotoUpdateTakeAway',
                                  exc_info=e)
            finally:
                time.sleep(2)

    def DataBaseCheck(self):
        tablelist = self.get_local_data(f"SELECT name FROM sqlite_master WHERE type='table';")
        for i in self.config.TABLE_LIST:
            if i.NAME not in tablelist['name'].to_list():
                self.executeLocally(i.INITIAL_QUERY)
                self.HardLoadData(i)

    def HardLoadData(self, Table, delete=False):
        data = self.get_data(f"select * from {Table.NAME} where {Table.ID_STORE}={self.STORE_ID};")
        if len(data) > 0 and self.config.LOADED in data.keys():
            update_data = data[(data[self.config.LOADED] == 0) | (data[self.config.UPDATED] == 0)]
            data[self.config.LOADED] = True
            data[self.config.UPDATED] = True
            if delete:
                self.executeLocally(f"Delete from {Table.NAME} where 1=1;")
            self.SaveLocalData(data, Table.NAME)
            if len(update_data) > 0:
                self.execute(
                    f"update {Table.NAME} set {self.config.LOADED}='1', {self.config.UPDATED}='1' where {Table.ID_STORE}="
                    f"{self.STORE_ID} and {Table.ID} in ({','.join(map(str, update_data[Table.ID].to_list()))})")
        elif len(data) > 0:
            if delete:
                self.executeLocally(f"Delete from {Table.NAME} where 1=1;")
            self.SaveLocalData(data, Table.NAME)

    def GetMaxOrderID(self):
        query = (f'select max({self.config.OrderMetaData.ID_ORDER}) from {self.config.OrderMetaData.NAME} where '
                 f'{self.config.OrderMetaData.ID_STORE}={self.STORE_ID};')
        data = self.get_local_data(query)
        if data is None:
            self.MaxOrderID = 0
            return
        if data.iloc[0, 0] is None:
            self.MaxOrderID = 0
        else:
            self.MaxOrderID = data.iloc[0, 0]

    def GetMaxOrderListID(self):
        query = (f'select max({self.config.OrderList.ID}) from {self.config.OrderList.NAME} where '
                 f'{self.config.OrderList.ID_STORE}={self.STORE_ID};')
        data = self.get_local_data(query)
        if data is None:
            self.MaxOrderListID = 0
            return
        if data.iloc[0, 0] is None:
            self.MaxOrderListID = 0
        else:
            self.MaxOrderListID = data.iloc[0, 0]

    def GetMaxOrderMataListID(self):
        query = (f'select max({self.config.OrderMetaData.ID}) from {self.config.OrderMetaData.NAME} where '
                 f'{self.config.OrderMetaData.ID_STORE}={self.STORE_ID};')
        data = self.get_local_data(query)
        if data is None:
            self.MaxOrderMataListID = 0
            return
        if data.iloc[0, 0] is None:
            self.MaxOrderMataListID = 0
        else:
            self.MaxOrderMataListID = data.iloc[0, 0]

    def GetMaxID(self, table):
        query = (f'select max({table.ID}) from {table.NAME} where '
                 f'{table.ID_STORE}={self.STORE_ID};')
        data = self.get_local_data(query)
        if data is None:
            return 0
        if data.iloc[0, 0] is None:
            return 0
        else:
            return data.iloc[0, 0]

    def InitialOrder(self, TableID, NumOfPeople=None, Name=None, Number=None, Note=None, AccountID=None):
        table = self.config.OrderMetaData
        TableInfo = self.GetOpenTableInfo2()
        if TableID not in TableInfo.ByTableIDDict or TableID == 0:
            if self.MaxOrderMataListID is None:
                self.GetMaxOrderMataListID()
            self.MaxOrderMataListID += 1
            if self.MaxOrderID is None:
                self.GetMaxOrderID()
            self.MaxOrderID += 1
            StartTime = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            data = pd.DataFrame({table.ID: [self.MaxOrderMataListID],
                                 table.ID_ORDER: [self.MaxOrderID],
                                 table.ID_STORE: [self.STORE_ID],
                                 table.FIELD: [table.Fields.START_TIME],
                                 table.VALUE: [StartTime]
                                 })
            self.MaxOrderMataListID += 1
            tmp = pd.DataFrame({table.ID: [self.MaxOrderMataListID],
                                table.ID_ORDER: [self.MaxOrderID],
                                table.ID_STORE: [self.STORE_ID],
                                table.FIELD: [table.Fields.ID_TABLE],
                                table.VALUE: [str(TableID)]
                                })
            data = data.append(tmp)
            self.MaxOrderMataListID += 1
            tmp = pd.DataFrame({table.ID: [self.MaxOrderMataListID],
                                table.ID_ORDER: [self.MaxOrderID],
                                table.ID_STORE: [self.STORE_ID],
                                table.FIELD: [table.Fields.IS_FINISHED],
                                table.VALUE: ['False']
                                })
            data = data.append(tmp)
            self.MaxOrderMataListID += 1
            ServiceCharge = self.Setting.GetValue(Config.ValueSetting.TableOrder.STR_DEFAULT_SERVICE_CHARGE_PERCENT)
            if ServiceCharge is None:
                ServiceCharge = 0
            tmp = pd.DataFrame({table.ID: [self.MaxOrderMataListID],
                                table.ID_ORDER: [self.MaxOrderID],
                                table.ID_STORE: [self.STORE_ID],
                                table.FIELD: [table.Fields.SERVICE_CHARGE_PERCENT],
                                table.VALUE: [str(ServiceCharge)]
                                })
            data = data.append(tmp)
            if Name is not None:
                self.MaxOrderMataListID += 1
                tmp = pd.DataFrame({table.ID: [self.MaxOrderMataListID],
                                    table.ID_ORDER: [self.MaxOrderID],
                                    table.ID_STORE: [self.STORE_ID],
                                    table.FIELD: [table.Fields.ORDER_NAME],
                                    table.VALUE: [Name]
                                    })
                data = data.append(tmp)

            if Number is not None:
                self.MaxOrderMataListID += 1
                tmp = pd.DataFrame({table.ID: [self.MaxOrderMataListID],
                                    table.ID_ORDER: [self.MaxOrderID],
                                    table.ID_STORE: [self.STORE_ID],
                                    table.FIELD: [table.Fields.ORDER_NUMBER],
                                    table.VALUE: [Number]
                                    })
                data = data.append(tmp)
            if Note is not None:
                self.MaxOrderMataListID += 1
                tmp = pd.DataFrame({table.ID: [self.MaxOrderMataListID],
                                    table.ID_ORDER: [self.MaxOrderID],
                                    table.ID_STORE: [self.STORE_ID],
                                    table.FIELD: [table.Fields.ORDER_NOTE],
                                    table.VALUE: [Note]
                                    })
                data = data.append(tmp)
            if AccountID is not None:
                self.MaxOrderMataListID += 1
                tmp = pd.DataFrame({table.ID: [self.MaxOrderMataListID],
                                    table.ID_ORDER: [self.MaxOrderID],
                                    table.ID_STORE: [self.STORE_ID],
                                    table.FIELD: [table.Fields.ACCOUNT_ID],
                                    table.VALUE: [AccountID]
                                    })
                data = data.append(tmp)
            if NumOfPeople is not None:
                self.MaxOrderMataListID += 1
                tmp = pd.DataFrame({table.ID: [self.MaxOrderMataListID],
                                    table.ID_ORDER: [self.MaxOrderID],
                                    table.ID_STORE: [self.STORE_ID],
                                    table.FIELD: [table.Fields.NUM_OF_PEOPLE],
                                    table.VALUE: [str(NumOfPeople)]
                                    })
                data = data.append(tmp)
                self.logger.info(
                    f"New Order Created: OrderID: {self.MaxOrderID}, TableID: {TableID}, #People: {NumOfPeople}")
            data[table.VALUE] = data[table.VALUE].astype(str)
            data[table.CREATE_TIME] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            self.SaveLocalData(data, table.NAME)
            return self.MaxOrderID
        else:
            OrderId = TableInfo.ByTableIDDict[TableID].OrderID
            self.logger.info(
                f"New Order Created Error: OrderID: {OrderId}, TableID: {TableID} already exist.")
            return OrderId

    def OnlineOrderConvert(self, Order):
        t1 = self.config.PendingOnlineOrder
        t2 = self.config.OrderList
        TableID = Order[t1.ID_TABLE]
        if TableID is None or pd.isna(TableID):
            return
        OrderID = None
        if self.TableInfo.ByTableIDDict[TableID].StartTime is None:
            # initial table
            OrderID = self.InitialOrder(TableID)
        else:
            OrderID = self.TableInfo.ByTableIDDict[TableID].OrderID
        resultData = {}
        self.MaxOrderListID += 1
        resultData[t2.ID] = self.MaxOrderListID
        resultData[t2.ID_ORDER] = OrderID
        resultData[t2.ID_STORE] = self.STORE_ID
        resultData[t2.ID_FOOD] = Order[t1.ID_FOOD]
        resultData[t2.QTY] = Order[t1.QTY]
        resultData[t2.UNIT_PRICE] = self.menu[Order[t1.ID_FOOD]].UnitPrice
        resultData[t2.NOTE] = Order[t1.NOTE]
        return pd.Series(resultData)

    def CloseTable(self, OrderID):
        metatable = self.config.OrderMetaData
        ordertable = self.config.OrderList
        Loaded = self.config.LOADED
        query = (f"Update {metatable.NAME} set {metatable.VALID}=false, {Loaded}=false "
                 f"where {metatable.ID_ORDER}={OrderID} and {metatable.ID_STORE}={self.STORE_ID}")
        self.executeLocally(query)
        query = (f"Update {ordertable.NAME} set {ordertable.VALID}=false, {Loaded}=false "
                 f"where {ordertable.ID_ORDER}={OrderID} and {ordertable.ID_STORE}={self.STORE_ID}")
        self.executeLocally(query)
        # self.TableInfo.ByOrderIDDict[OrderID].Clear()

    def PlaceOrder(self, Orders: TableInfoStore, Print: bool = True):
        try:
            if len(Orders.Orders) == 0:
                return
            table = self.config.OrderList
            OrderSeires = {table.ID: [],
                           table.ID_FOOD: [],
                           table.QTY: [],
                           table.UNIT_PRICE: [],
                           table.NOTE: []}
            self.GetMaxOrderListID()
            k = 1
            for Order in Orders.Orders:
                self.MaxOrderListID += 1
                OrderSeires[table.ID].append(self.MaxOrderListID)
                OrderSeires[table.ID_FOOD].append(Order.FoodID)
                OrderSeires[table.QTY].append(Order.Qty)
                OrderSeires[table.UNIT_PRICE].append(Order.UnitPrice)
                OrderSeires[table.NOTE].append(Order.Note)
            data = pd.DataFrame(OrderSeires)
            data[table.ID_STAFF] = Orders.Orders[0].StaffID
            data[table.ID_ORDER] = Orders.Orders[0].OrderID
            data[table.ID_STORE] = self.STORE_ID
            data[table.VALID] = 1
            data[table.CREATE_TIME] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            data[self.config.LOADED] = 0
            data[self.config.UPDATED] = 0
            self.SaveLocalData(data, table.NAME)
            if Print:
                self.Printer.PrintOrder(Orders)
        except Exception as e:
            self.logger.error("Error during placing order.", exc_info=e)

    def CheckOutTable(self, OrderID):
        try:
            table = self.config.OrderMetaData
            if self.MaxOrderMataListID is None:
                self.GetMaxOrderMataListID()
            self.MaxOrderMataListID += 1
            EndTime = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            self.logger.info(f'Order {OrderID} add end time {EndTime}.')
            data = {table.ID: [self.MaxOrderMataListID],
                    table.ID_ORDER: [OrderID],
                    table.FIELD: [table.Fields.END_TIME],
                    table.VALUE: [EndTime],
                    table.CREATE_TIME: [EndTime],
                    table.VALID: [True],
                    table.ID_STORE: [self.STORE_ID],
                    self.config.UPDATED: [False],
                    self.config.LOADED: [False]}
            data = pd.DataFrame(data)
            self.SaveLocalData(data, table.NAME)
        except Exception as e:
            self.logger.error(f'Error during adding order end time. OrderID: {OrderID}',
                              exc_info=e)

    def ReopenTable(self, OrderID):
        try:
            table = self.config.OrderMetaData
            self.executeLocally(f"Update {table.NAME} set `{table.VALID}` = false, `{self.config.LOADED}`=false where "
                                f"`{table.ID_STORE}`='{self.STORE_ID}' and `{table.FIELD}`='{table.Fields.END_TIME}'"
                                f" and `{table.ID_ORDER}`='{OrderID}'")
        except Exception as e:
            self.logger.error(f'Error during remove order end time. OrderID: {OrderID}',
                              exc_info=e)

    def AddCash(self, Cash, OrderID):
        self.AddMetaTableValue(Cash, OrderID, self.config.OrderMetaData.Fields.CASH)

    def AddCard(self, Card, OrderID):
        self.AddMetaTableValue(Card, OrderID, self.config.OrderMetaData.Fields.CARD)

    def AddServicePercent(self, ServicePercent, OrderID):
        self.AddMetaTableValue(ServicePercent, OrderID, self.config.OrderMetaData.Fields.SERVICE_CHARGE_PERCENT)

    def AddDiscountPercent(self, DiscountPercent, OrderID):
        self.AddMetaTableValue(DiscountPercent, OrderID, self.config.OrderMetaData.Fields.DISCOUNT_PERCENT)

    def FinishTable(self, OrderID):
        self.AddMetaTableValue(True, OrderID, Config.DataBase.OrderMetaData.Fields.IS_FINISHED)

    def AddMetaTableValue(self, Amount, OrderID, Field):
        try:
            table = self.config.OrderMetaData
            self.logger.info(f'Order {OrderID} update {Field} {Amount}.')
            query = (f"select * from {table.NAME} where `{table.FIELD}`='{Field}' and "
                     f"`{table.ID_ORDER}`='{OrderID}' and `{table.VALID}` = true")
            data = self.get_local_data(query)
            if len(data) > 0:
                self.logger.info(f"Order {OrderID} update {Field} from {data.iloc[0][table.VALID]} to {Amount}.")
                query = (f"Update {table.NAME} set `{table.VALUE}`='{Amount}', `{self.config.LOADED}`=false where "
                         f"`{table.ID}`='{data.iloc[0][table.ID]}' and `{table.FIELD}` = '{Field}'")
                self.executeLocally(query)
            else:
                if self.MaxOrderMataListID is None:
                    self.GetMaxOrderMataListID()
                self.MaxOrderMataListID += 1
                self.logger.info(f'Order {OrderID} add {Field} {Amount}.')
                data = {table.ID: [self.MaxOrderMataListID],
                        table.ID_ORDER: [OrderID],
                        table.FIELD: [Field],
                        table.VALUE: [Amount],
                        table.CREATE_TIME: [datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")],
                        table.VALID: [True],
                        table.ID_STORE: [self.STORE_ID],
                        self.config.UPDATED: [False],
                        self.config.LOADED: [False]}
                data = pd.DataFrame(data)
                self.SaveLocalData(data, table.NAME)

        except Exception as e:
            self.logger.error(f'Error during adding {Field} end time. TableID: {OrderID}',
                              exc_info=e)

    def UpdateOneLineLocally_LoadFalse(self, data, table):
        Value = ''
        for field in table.COLUMNS:
            if Value != '':
                Value += ', '
            Value += f"`{field}`='{data[field]}'"
        self.executeLocally(
            f"Update {table.NAME} Set {Value}, `{self.config.UPDATED}`='0', `{self.config.LOADED}`='0' "
            f"where {table.ID_STORE} = {self.STORE_ID} and {table.ID} = {data[table.ID]}")

    def SwitchTable(self, TableIDA, TableIDB):
        if TableIDA == TableIDB:
            return
        self.logger.info(f"switch Table {TableIDA}, {TableIDB}.")
        try:
            TableA = self.TableInfo.ByTableIDDict[TableIDA] if TableIDA in self.TableInfo.ByTableIDDict else None
            TableB = self.TableInfo.ByTableIDDict[TableIDB] if TableIDB in self.TableInfo.ByTableIDDict else None
            table = self.config.OrderMetaData
            dataA = None
            dataB = None
            if TableA is not None:
                query = (f"select * from {table.NAME} where `{table.FIELD}`='{table.Fields.ID_TABLE}' and "
                         f"`{table.ID_ORDER}`='{TableA.OrderID}' and `{table.VALID}`='1'")
                dataA = self.get_local_data(query)
            if TableB is not None:
                query = (f"select * from {table.NAME} where `{table.FIELD}`='{table.Fields.ID_TABLE}' and "
                         f"`{table.ID_ORDER}`='{TableB.OrderID}' and `{table.VALID}`='1'")
                dataB = self.get_local_data(query)
            if dataB is not None and len(dataB) > 0:
                dataB[table.VALUE] = TableIDA
                dataB[self.config.LOADED] = False
                self.UpdateOneLineLocally_LoadFalse(dataB.iloc[0], table)
            if dataA is not None and len(dataA) > 0:
                dataA[table.VALUE] = TableIDB
                dataA[self.config.LOADED] = False
                self.UpdateOneLineLocally_LoadFalse(dataA.iloc[0], table)
        except Exception as e:
            self.logger.error(f'Error during SwitchTable {TableIDA}, {TableIDB}',
                              exc_info=e)

    def EditOrder(self, aOrderInfo: OrderInfo):
        table = self.config.OrderList
        query = (f"Update {table.NAME} set `{table.QTY}` = '{aOrderInfo.Qty}', "
                 f"`{table.UNIT_PRICE}` = '{aOrderInfo.UnitPrice}', `{table.NOTE}`='{aOrderInfo.Note}', "
                 f"`{self.config.LOADED}`='0' where "
                 f"`{table.ID}`='{aOrderInfo.ID}' and `{table.ID_STORE}`='{self.STORE_ID}'")
        self.executeLocally(query)

    def GetStaffName(self, ID):
        for i in self.StaffList:
            if self.StaffList[i] == ID:
                return i
        return None

    def GetHistoryOrders(self) -> AllTableInfoStore:
        OrderMetaData = self.config.OrderMetaData
        query = (f"select * from {OrderMetaData.NAME} where `{OrderMetaData.VALID}`='1' and "
                 f"`{OrderMetaData.ID_STORE}`='{self.STORE_ID}'")
        data = self.get_local_data(query)
        TableInfo = AllTableInfoStore(self.logger)
        if len(data) > 0:
            TableInfo.AddOrderMetaInfo(data)
            OrderList = self.config.OrderList
            query = (f"select * from {OrderList.NAME} where `{OrderList.VALID}`='1' and "
                     f"`{OrderList.ID_STORE}`='{self.STORE_ID}'")
            data = self.get_local_data(query)
            TableInfo.AddOrderInfo(data)
            TableInfo.LoadMenu(self.menu)
        return TableInfo

    def LoadCashBoxAmount(self):
        table = self.config.CashBoxAmount
        query = (f"select max({table.CREATE_TIME}) from {table.NAME} where `{table.ID_STORE}`='{self.STORE_ID}' and "
                 f"`{table.VALID}`='1'")
        data = self.get_local_data(query)
        if data is None:
            return {}
        LastestTime = data.iloc[0, 0]
        if LastestTime is None:
            return {}
        query = (f"select * from {table.NAME} where `{table.ID_STORE}`='{self.STORE_ID}' and "
                 f"`{table.VALID}`='1' and `{table.CREATE_TIME}`='{LastestTime}'")
        data = self.get_local_data(query)
        data = data.set_index(table.CASH_TYPE)
        return data[table.CASH_AMOUNT].to_dict()

    def GetMaxID(self, table):
        query = (f"select max({table.ID}) from {table.NAME} where `{table.ID_STORE}`='{self.STORE_ID}' and "
                 f"`{table.VALID}`='1';")
        data = self.get_local_data(query)
        if data is None:
            return 0
        index = data.iloc[0, 0]
        if index is None:
            return 0
        else:
            return index

    def SaveTodayDataToHistoryTable(self):
        MetaTable = self.config.OrderMetaData
        query = (f"select * from {MetaTable.NAME} where `{MetaTable.ID_STORE}`='{self.STORE_ID}' and "
                 f"`{MetaTable.VALID}`='1';")
        MetaData = self.get_local_data(query)
        OrderTable = self.config.OrderList
        query = (f"select * from {OrderTable.NAME} where `{OrderTable.ID_STORE}`='{self.STORE_ID}' and "
                 f"`{OrderTable.VALID}`='1';")
        OrderData = self.get_local_data(query)
        OrderIDList = MetaData[
            (MetaData[MetaTable.FIELD] == MetaTable.Fields.IS_FINISHED) & (MetaData[MetaTable.VALUE] == 'True')][
            MetaTable.ID_ORDER].to_list()
        if len(OrderIDList) > 0:
            HistMetaTable = self.config.HistoryOrderMetaData
            HistOrderTable = self.config.HistoryOrderList
            query = (f"select max({HistMetaTable.ID_ORDER}) from {HistMetaTable.NAME} where"
                     f"`{HistMetaTable.ID_STORE}`='{self.STORE_ID}' and `{HistMetaTable.VALID}`='1';")
            MaxOrderID = self.get_local_data(query)
            if MaxOrderID is None:
                MaxOrderID = 0
            else:
                MaxOrderID = MaxOrderID.iloc[0, 0]
            if MaxOrderID is None:
                MaxOrderID = 0
            for OrderID in OrderIDList:
                MaxOrderID += 1
                SubMetaData = MetaData[MetaData[HistMetaTable.ID_ORDER] == OrderID]
                SubMetaData[HistMetaTable.ID_ORDER] = MaxOrderID
                # SubMetaData = SubMetaData.drop(HistMetaTable.ID, axis=1)
                MaxHisMetaID = self.GetMaxID(HistMetaTable) + 1
                SubMetaData = SubMetaData.reset_index(drop=True)
                for i in range(len(SubMetaData)):
                    SubMetaData.loc[i, HistMetaTable.ID] = i + MaxHisMetaID
                SubMetaData[self.config.LOADED] = False
                self.SaveLocalData(SubMetaData, HistMetaTable.NAME)
                SubOrderData = OrderData[OrderData[HistOrderTable.ID_ORDER] == OrderID]
                SubOrderData[HistOrderTable.ID_ORDER] = MaxOrderID
                # SubOrderData = SubOrderData.drop(HistOrderTable.ID, axis=1)
                MaxOrderListID = self.GetMaxID(HistOrderTable) + 1
                SubOrderData = SubOrderData.reset_index(drop=True)
                for i in range(len(SubOrderData)):
                    SubOrderData.loc[i, HistOrderTable.ID] = i + MaxOrderListID
                SubOrderData[self.config.LOADED] = False
                self.SaveLocalData(SubOrderData, HistOrderTable.NAME)
                query = (
                    f"update {MetaTable.NAME} set `{MetaTable.VALID}`='0', `{self.config.LOADED}`='0' where "
                    f"`{MetaTable.ID_STORE}`='{self.STORE_ID}'"
                    f" and `{MetaTable.ID_ORDER}`='{OrderID}';")
                self.executeLocally(query)
                query = (
                    f"update {OrderTable.NAME} set `{OrderTable.VALID}`='0', `{self.config.LOADED}`='0' where "
                    f"`{OrderTable.ID_STORE}`='{self.STORE_ID}' and "
                    f"`{OrderTable.ID_ORDER}`='{OrderID}';")
                self.executeLocally(query)

    def SaveCoinInfo(self, CoinDict):
        if len(CoinDict) == 0:
            return
        table = self.config.CashBoxAmount
        CoinDF = pd.DataFrame(CoinDict, index=[table.CASH_AMOUNT]).T.reset_index()
        CoinDF.columns = [table.CASH_TYPE, table.CASH_AMOUNT]
        CoinDF[table.VALID] = True
        CoinDF[table.ID_STORE] = self.STORE_ID
        CoinDF[table.STAFF_ID] = self.StaffList[self.StaffName]
        CoinDF[table.CREATE_TIME] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        CoinDF[self.config.LOADED] = False
        CoinDF[self.config.UPDATED] = False
        query = (f"select max({table.ID}) from {table.NAME} where `{table.ID_STORE}`='{self.STORE_ID}' and "
                 f"`{table.VALID}`='1';")
        MaxID = self.get_local_data(query)
        if MaxID is None:
            MaxID = 0
        else:
            MaxID = MaxID.iloc[0, 0]
        if MaxID is None:
            MaxID = 0
        CoinDF[table.ID] = MaxID + 1
        for i in range(len(CoinDF)):
            CoinDF.loc[i, table.ID] += i
        self.SaveLocalData(CoinDF, table.NAME)

    def SaveEODSummary(self, InfoDict):
        table = self.config.EODSummary
        SummaryDF = pd.DataFrame(InfoDict, index=[0])
        SummaryDF[table.VALID] = True
        SummaryDF[self.config.LOADED] = False
        SummaryDF[self.config.UPDATED] = False
        SummaryDF[table.ID_STORE] = self.STORE_ID
        SummaryDF[table.STAFF_ID] = self.StaffList[self.StaffName]
        SummaryDF[table.DATETIME] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        query = f"select max({table.ID}) from {table.NAME} where `{table.ID_STORE}`='{self.STORE_ID}';"
        MaxID = self.get_local_data(query)
        if MaxID is None:
            MaxID = 0
        else:
            MaxID = MaxID.iloc[0, 0]
        if MaxID is None:
            MaxID = 0
        MaxID += 1
        SummaryDF[table.ID] = MaxID
        self.SaveLocalData(SummaryDF, table.NAME)

    def DeleteOrder(self, OrderID):
        MetaTable = self.config.OrderMetaData
        query = (f"update {MetaTable.NAME} set `{MetaTable.VALID}`='0', `{self.config.UPDATED}`='0', "
                 f"`{self.config.LOADED}`='0' where `{MetaTable.ID_ORDER}`='{OrderID}';")
        self.executeLocally(query)
        OrderTable = self.config.OrderList
        query = (f"update {OrderTable.NAME} set `{OrderTable.VALID}`='0', `{self.config.UPDATED}`='0', "
                 f"`{self.config.LOADED}`='0' where `{OrderTable.ID_ORDER}`='{OrderID}';")
        self.executeLocally(query)

    def GetAccountList(self) -> pd.DataFrame:
        AccountList = self.config.OrderAccountList
        query = (
            f"select `{'`, `'.join(AccountList.COLUMNS)}` from {AccountList.NAME} where `{AccountList.VALID}` = '1'"
            f" and `{AccountList.ID_STORE}`='{self.STORE_ID}';")
        data = self.get_local_data(query)
        return data

    def ChangeAccount(self, Account, OrderID):
        AccountList = self.config.OrderAccountList
        query = (
            f"select `{AccountList.ID}` from {AccountList.NAME} where `{AccountList.ACCOUNT_NAME}`='{Account}' and "
            f"`{AccountList.VALID}`='1' and `{AccountList.ID_STORE}`='{self.STORE_ID}';")
        data = self.get_local_data(query)
        AccountId = None
        if len(data) > 0:
            AccountId = data.iloc[0, 0]
        OrderMeta = self.config.OrderMetaData
        query = (f"select * from {OrderMeta.NAME} where `{OrderMeta.ID_ORDER}`='{OrderID}' and "
                 f"`{OrderMeta.ID_STORE}`='{self.STORE_ID}' and `{OrderMeta.FIELD}`='{OrderMeta.Fields.ACCOUNT_ID}';")
        data = self.get_local_data(query)

        if len(data) == 0 and AccountId is not None:
            self.GetMaxOrderMataListID()
            MetaID = self.MaxOrderMataListID
            MetaID += 1
            DataDict = {OrderMeta.ID_ORDER: [OrderID],
                        OrderMeta.ID: [MetaID],
                        OrderMeta.ID_STORE: [self.STORE_ID],
                        OrderMeta.CREATE_TIME: [datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")],
                        OrderMeta.FIELD: [OrderMeta.Fields.ACCOUNT_ID],
                        OrderMeta.VALUE: [AccountId],
                        OrderMeta.VALID: [1],
                        self.config.LOADED: [0],
                        self.config.UPDATED: [0]}
            DF = pd.DataFrame(DataDict)
            self.SaveLocalData(DF, OrderMeta.NAME)
        elif len(data) > 0 and AccountId is not None:
            query = (f"update {OrderMeta.NAME} set `{OrderMeta.VALUE}`='{AccountId}', `{OrderMeta.VALID}`='1', "
                     f"`{OrderMeta.CREATE_TIME}`='{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}',"
                     f"`{self.config.LOADED}`='0', `{self.config.UPDATED}`='0'"
                     f" where `{OrderMeta.FIELD}`='{OrderMeta.Fields.ACCOUNT_ID}' and "
                     f"`{OrderMeta.ID_ORDER}`='{OrderID}' and `{OrderMeta.ID_STORE}`='{self.STORE_ID}';")
            self.executeLocally(query)
        elif len(data) > 0 and AccountId is None:
            query = (f"update {OrderMeta.NAME} set `{OrderMeta.VALID}`='0', `{self.config.UPDATED}`='0', "
                     f"`{self.config.LOADED}`='0' where `{OrderMeta.ID}`='{data.iloc[0][OrderMeta.ID]}';")
            self.executeLocally(query)

    def SaveNewAccount(self, AccountID, AccountName, AutoDelete, TotalAmount):
        AccountList = self.config.OrderAccountList
        if AccountName == '':
            return
        if AccountID is None:
            id = self.GetMaxID(AccountList)
            id += 1
            df = pd.DataFrame([{AccountList.ID: id,
                                AccountList.ACCOUNT_NAME: AccountName,
                                AccountList.ID_STORE: self.STORE_ID,
                                AccountList.AUTO_DELETE: AutoDelete,
                                AccountList.VALID: '1',
                                AccountList.TOTAL_AMOUNT: TotalAmount,
                                self.config.LOADED: 0,
                                self.config.UPDATED: 0}])
            self.SaveLocalData(df, AccountList.NAME)
        else:
            query = (f"Update {AccountList.NAME} set `{AccountList.ACCOUNT_NAME}`='{AccountName}', "
                     f"`{AccountList.AUTO_DELETE}`='{1 if AutoDelete else 0}', `{self.config.LOADED}`='0',"
                     f"`{AccountList.TOTAL_AMOUNT}`='{TotalAmount}'"
                     f"where `{AccountList.ID_STORE}`='{self.STORE_ID}' and `{AccountList.ID}`='{AccountID}'")
            self.executeLocally(query)
