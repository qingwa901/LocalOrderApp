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


class DataBase(SQLControl):
    def __init__(self, logger: logging.Logger, path):
        SQLControl.__init__(self, logger)
        self.logger = logger
        self.config = Config.DataBase
        self.Setting = ConfigSetting(logger)
        self.STORE_ID = self.config.STORE_ID  # Todo save store id to setting file
        self.MenuPageLoad = threading.Thread(target=self.LoadMenuPage)
        self.MenuPageLoad.start()
        self.StaffLoad = threading.Thread(target=self.LoadStaffInfo)
        self.StaffLoad.start()
        self.TableInfoLock = threading.Lock()
        self.TableInfo = AllTableInfoStore(self.logger)
        self.path = path
        self.StaffName = None
        self.StaffList = {}
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.tmp_path = path + '/tmp'
        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)
        self.menu = FullMenuList()
        self.DataBaseCheck()
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
        # LoadStoreInfo.join()

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
        pass  # Todo

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
        Value = ''
        for field in table.COLUMNS:
            if Value != '':
                Value += ', '
            Value += f"`{field}` = '{data[field]}'"
        self.execute(
            f"Update {table.NAME} Set {Value}, `{self.config.UPDATED}`=true, `{self.config.LOADED}`=true "
            f"where {table.ID_STORE} = {self.STORE_ID} and {table.ID} = {data[table.ID]}")

    def Update(self):
        for table in [self.config.OrderList, self.config.OrderMetaData]:
            data = self.get_local_data(
                f"select * from {table.NAME} where {self.config.LOADED} = false and {table.ID_STORE}={self.STORE_ID};")
            if len(data) > 0:
                data[self.config.LOADED] = True
                data[self.config.UPDATED] = True
                self.SaveData(data, table.NAME)
                self.executeLocally(
                    f"update {table.NAME} set {self.config.LOADED}='1', {self.config.UPDATED}='1' where "
                    f"{self.STORE_ID} and {table.ID} in ({','.join(data[table.ID])})")

            data = self.get_local_data(
                f"select * from {table.NAME} where {self.config.UPDATED} = false and {self.config.LOADED} = true")
            if len(data) > 0:
                data[self.config.UPDATED] = True
                data.apply(self.UpdateOneLine, axis=1, table=table)
                self.executeLocally(
                    f"update {table.NAME} set {self.config.UPDATED}='1' where {table.ID_STORE}= "
                    f"{self.STORE_ID} and {table.ID} in ({','.join(data[table.ID])})")

    def Download(self):
        # self.config.OrderList, self.config.OrderMetaData should only upload, download for remove update data only
        # So download do not trigger printing event.
        for table in [self.config.OrderList, self.config.OrderMetaData, self.config.PendingOnlineOrder]:
            data = self.get_data(
                f"select * from {table.NAME} where {self.config.LOADED} = false and {table.ID_STORE}={self.STORE_ID};")
            if len(data) > 0:
                data[self.config.LOADED] = True
                data[self.config.UPDATED] = True
                self.SaveLocalData(data, table.NAME)
                self.execute(
                    f"update {table.NAME} set {self.config.LOADED}='1', {self.config.UPDATED}='1' where {table.ID_STORE}="
                    f"{self.STORE_ID} and {table.ID} in ({','.join(data[table.ID])})")

            data = self.get_data(
                f"select * from {table.NAME} where {self.config.UPDATED} = false and {self.config.LOADED} = true "
                f"and {table.ID_STORE}={self.STORE_ID};")
            if len(data) > 0:
                data[self.config.UPDATED] = True
                data.apply(self.UpdateOneLineLocally, axis=1, table=table)
                self.execute(
                    f"update {table.NAME} set {self.config.UPDATED}='1' where {table.ID_STORE}= "
                    f"{self.STORE_ID} and {table.ID} in ({','.join(data[table.ID])})")
            if table == self.config.OrderList:
                self.TableInfo.AddOrderInfo(data)
            if table == self.config.PendingOnlineOrder:
                if len(data) > 0:
                    OrderData = data.apply(self.OnlineOrderConvert, axis=1)
                    self.SaveOrdersLocal(OrderData)
                    OrderData.apply(self._PrintOrder, axis=1)

    def Update_(self):
        for table in [self.config.OrderList, self.config.OrderMetaData]:
            data = self.get_local_data(
                f"select * from {table.NAME} where {self.config.LOADED} = '0' and {table.ID_STORE}={self.STORE_ID};")
            if len(data) > 0:
                data[self.config.LOADED] = True
                data[self.config.UPDATED] = True
                ExistIDList = self.IsDataExist(data[table.ID].to_list(), table, True)
                ExistData = data[data[table.ID].isin(ExistIDList)]
                if len(ExistData) > 0:
                    ExistData.apply(self.UpdateOneLine, axis=1, table=table)
                NewData = data[~data[table.ID].isin(ExistIDList)]
                if len(NewData) > 0:
                    self.SaveData(NewData, table.NAME)
                IDstr = "','".join(data[table.ID].astype(str))
                self.executeLocally(
                    f"update {table.NAME} set {self.config.LOADED}='1', {self.config.UPDATED}='1' where {table.ID_STORE} = "
                    f"{self.STORE_ID} and {table.ID} in ('{IDstr}')")

    def Download_(self):
        for table in [self.config.OrderList, self.config.OrderMetaData, self.config.PendingOnlineOrder]:
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

            # if table == self.config.OrderList:
            #     if len(data) > 0:
            #         self.TableInfo.AddOrderInfo(data)
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

    def GetOpenTableInfo(self):
        # if (self.TableInfo is not None and self.TableInfo.UpdateTime is not None
        #         and time.time() - self.TableInfo.UpdateTime < 1):
        #     # Table State Change unable to apply on the first time. Cause display error.
        #     return
        with self.TableInfoLock:
            table = Config.DataBase.OrderMetaData
            query = (f"select {table.ID_ORDER} from {table.NAME} where "
                     f"{table.FIELD}='{table.Fields.IS_FINISHED}' and "
                     f"{table.VALUE}='False' and "
                     f"{table.ID_STORE}='{self.STORE_ID}' and {table.VALID} = true")
            OpenTable = self.get_local_data(query)
            OpenOrderList = OpenTable[Config.DataBase.OrderMetaData.ID_ORDER].astype(str).to_list()
            self.TableInfo.Clear()
            query = (f"select * from {table.NAME} where {table.ID_ORDER} in ({','.join(OpenOrderList)})"
                     f" and {table.VALID} = true;")
            OrderMetaData = self.get_local_data(query)
            self.TableInfo.AddOrderMetaInfo(OrderMetaData)
            query = (f"select * from {Config.DataBase.OrderList.NAME} where {Config.DataBase.OrderList.ID_ORDER} "
                     f"in ({','.join(OpenOrderList)})")
            OrderList = self.get_local_data(query)
            if len(OrderList) > 0:
                self.TableInfo.AddOrderInfo(OrderList)
            self.TableInfo.LoadMenu(self.menu)
            self.TableInfo.UpdateTime = time.time()

    def SetUpTableColorUpdate(self, Event):
        self.color_auto_update = threading.Thread(target=self.AotoUpdateTableColor, args=[Event])
        self.color_auto_update.start()

    def AotoUpdateTableColor(self, Event):
        while self.open:
            try:
                self.GetOpenTableInfo()
                Event(self.TableInfo)
            except Exception as e:
                self.logger.error(f'Error during AotoUpdateTableColor',
                                  exc_info=e)
            finally:
                time.sleep(2)

    def DataBaseCheck(self):
        tablelist = self.get_local_data(f"SELECT name FROM sqlite_master WHERE type='table';")
        for i in [self.config.OrderList, self.config.OrderMetaData, self.config.Staff, self.config.MenuList,
                  self.config.ManuPageList]:
            if i.NAME not in tablelist['name'].to_list():
                self.executeLocally(i.INITIAL_QUERY)
                self.HardLoadData(i)

    def HardLoadData(self, Table):
        data = self.get_data(f"select * from {Table.NAME} where {Table.ID_STORE}={self.STORE_ID};")
        if len(data) > 0 and self.config.LOADED in data.keys():
            update_data = data[(data[self.config.LOADED] == 0) | (data[self.config.UPDATED] == 0)]
            data[self.config.LOADED] = True
            data[self.config.UPDATED] = True
            self.SaveLocalData(data, Table.NAME)
            if len(update_data) > 0:
                self.execute(
                    f"update {Table.NAME} set {self.config.LOADED}='1', {self.config.UPDATED}='1' where {Table.ID_STORE}="
                    f"{self.STORE_ID} and {Table.ID} in ({','.join(update_data[Table.ID])})")

    def GetMaxOrderID(self):
        query = (f'select max({self.config.OrderMetaData.ID_ORDER}) from {self.config.OrderMetaData.NAME} where '
                 f'{self.config.OrderMetaData.ID_STORE}={self.STORE_ID};')
        data = self.get_local_data(query)
        if data.iloc[0, 0] is None:
            self.MaxOrderID = 0
        else:
            self.MaxOrderID = data.iloc[0, 0]

    def GetMaxOrderListID(self):
        query = (f'select max({self.config.OrderList.ID}) from {self.config.OrderList.NAME} where '
                 f'{self.config.OrderList.ID_STORE}={self.STORE_ID};')
        data = self.get_local_data(query)
        if data.iloc[0, 0] is None:
            self.MaxOrderListID = 0
        else:
            self.MaxOrderListID = data.iloc[0, 0]

    def GetMaxOrderMataListID(self):
        query = (f'select max({self.config.OrderMetaData.ID}) from {self.config.OrderMetaData.NAME} where '
                 f'{self.config.OrderMetaData.ID_STORE}={self.STORE_ID};')
        data = self.get_local_data(query)
        if data.iloc[0, 0] is None:
            self.MaxOrderMataListID = 0
        else:
            self.MaxOrderMataListID = data.iloc[0, 0]

    def InitialOrder(self, TableID, NumOfPeople=None):
        table = self.config.OrderMetaData
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
        if self.MaxOrderID not in self.TableInfo.ByOrderIDDict:
            self.TableInfo.ByOrderIDDict[self.MaxOrderID] = TableInfoStore()
        self.TableInfo.ByOrderIDDict[self.MaxOrderID].OrderID = self.MaxOrderID
        self.TableInfo.ByOrderIDDict[self.MaxOrderID].StartTime = StartTime
        self.TableInfo.ByOrderIDDict[self.MaxOrderID].TablID = TableID
        self.TableInfo.ByTableIDDict[TableID] = self.TableInfo.ByOrderIDDict[self.MaxOrderID]
        if NumOfPeople is not None:
            self.MaxOrderMataListID += 1
            tmp = pd.DataFrame({table.ID: [self.MaxOrderMataListID],
                                table.ID_ORDER: [self.MaxOrderID],
                                table.ID_STORE: [self.STORE_ID],
                                table.FIELD: [table.Fields.NUM_OF_PEOPLE],
                                table.VALUE: [str(NumOfPeople)]
                                })
            data = data.append(tmp)
            self.TableInfo.ByOrderIDDict[self.MaxOrderID].NumOfPeople = NumOfPeople
            self.logger.info(
                f"New Order Created: OrderID: {self.MaxOrderID}, TableID: {TableID}, #People: {NumOfPeople}")
        data[table.VALUE] = data[table.VALUE].astype(str)
        data[table.CREATE_TIME] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        self.SaveLocalData(data, table.NAME)
        return self.MaxOrderID

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
        Update = self.config.UPDATED
        query = (f"Update {metatable.NAME} set {metatable.VALID}=false, {Update}=false "
                 f"where {metatable.ID_ORDER}={OrderID} and {metatable.ID_STORE}={self.STORE_ID}")
        self.executeLocally(query)
        query = (f"Update {ordertable.NAME} set {ordertable.VALID}=false, {Update}=false "
                 f"where {ordertable.ID_ORDER}={OrderID} and {ordertable.ID_STORE}={self.STORE_ID}")
        self.executeLocally(query)
        self.TableInfo.ByOrderIDDict[OrderID].Clear()

    def PlaceOrder(self, Orders: TableInfoStore):
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
            self.Printer.PrintOrder(Orders)
        except Exception as e:
            self.logger.error("Error during placing order.", exc_info=e)

    def CheckOutTable(self, TableNumber):
        try:
            table = self.config.OrderMetaData
            if self.MaxOrderMataListID is None:
                self.GetMaxOrderMataListID()
            self.MaxOrderMataListID += 1
            OrderID = self.TableInfo.ByTableIDDict[TableNumber].OrderID
            EndTime = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            self.logger.info(f'Order {OrderID} add end time {EndTime}.')
            data = {table.ID: [self.MaxOrderMataListID],
                    table.ID_ORDER: [OrderID],
                    table.FIELD: [table.Fields.END_TIME],
                    table.VALUE: [EndTime],
                    table.CREATE_TIME: [EndTime],
                    table.VALID: [True],
                    table.ID_STORE: [self.STORE_ID],
                    self.config.UPDATED: [True],
                    self.config.LOADED: [True]}
            data = pd.DataFrame(data)
            self.SaveLocalData(data, table.NAME)
        except Exception as e:
            self.logger.error(f'Error during adding order end time. TableID: {TableNumber}',
                              exc_info=e)

    def ReopenTable(self, TableNumber):
        try:
            table = self.config.OrderMetaData
            OrderID = self.TableInfo.ByTableIDDict[TableNumber].OrderID
            self.executeLocally(f"Update {table.NAME} set `{table.VALID}` = false, `{self.config.LOADED}`=false where "
                                f"`{table.ID_STORE}`='{self.STORE_ID}' and `{table.FIELD}`='{table.Fields.END_TIME}'"
                                f" and `{table.ID_ORDER}`='{OrderID}'")
        except Exception as e:
            self.logger.error(f'Error during remove order end time. TableID: {TableNumber}',
                              exc_info=e)

    def AddCash(self, Cash, TableNumber):
        self.AddMetaTableValue(Cash, TableNumber, self.config.OrderMetaData.Fields.CASH)

    def AddCard(self, Card, TableNumber):
        self.AddMetaTableValue(Card, TableNumber, self.config.OrderMetaData.Fields.CARD)

    def AddServicePercent(self, ServicePercent, TableNumber):
        self.AddMetaTableValue(ServicePercent, TableNumber, self.config.OrderMetaData.Fields.SERVICE_CHARGE_PERCENT)

    def AddDiscountPercent(self, DiscountPercent, TableNumber):
        self.AddMetaTableValue(DiscountPercent, TableNumber, self.config.OrderMetaData.Fields.DISCOUNT_PERCENT)

    def FinishTable(self, TableNumber):
        self.AddMetaTableValue(True, TableNumber, Config.DataBase.OrderMetaData.Fields.IS_FINISHED)

    def AddMetaTableValue(self, Amount, TableNumber, Field):
        try:
            table = self.config.OrderMetaData
            OrderID = self.TableInfo.ByTableIDDict[TableNumber].OrderID
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
            self.logger.error(f'Error during adding {Field} end time. TableID: {TableNumber}',
                              exc_info=e)

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
                self.UpdateOneLineLocally(dataB.iloc[0], table)
            if dataA is not None and len(dataA) > 0:
                dataA[table.VALUE] = TableIDB
                dataA[self.config.LOADED] = False
                self.UpdateOneLineLocally(dataA.iloc[0], table)
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
        TableInfo.AddOrderMetaInfo(data)
        OrderList = self.config.OrderList
        query = (f"select * from {OrderList.NAME} where `{OrderList.VALID}`='1' and "
                 f"`{OrderList.ID_STORE}`='{self.STORE_ID}'")
        data = self.get_local_data(query)
        TableInfo.AddOrderInfo(data)
        return TableInfo