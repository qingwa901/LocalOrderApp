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
from TableInfoStore import AllTableInfoStore
from MenuStore import FullMenuList
import sqlite3


class DataBase(SQLControl):
    def __init__(self, logger: logging.Logger, path):
        SQLControl.__init__(self, logger)
        self.logger = logger
        self.config = Config.DataBase
        self.Setting = ConfigSetting(logger)
        self.Printer = PrinterControl(self.logger, self.Setting)
        self.TableInfo = AllTableInfoStore()
        self.path = path
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.tmp_path = path + '/tmp'
        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)
        self.STORE_ID = self.config.STORE_ID  # Todo save store id to setting file
        self.menu = FullMenuList()
        self.DataBaseCheck()
        self.InitialLoadData()
        self.auto_update = threading.Thread(target=self.AutoUpdate)
        self.auto_update.start()
        self.MaxOrderID = None
        self.MaxOrderListID = None
        self.MaxOrderMataListID = None

    def InitialLoadData(self):
        data = self.get_data(
            f"select * from {self.config.STORE_INFO} where {self.config.StoreList.ID} = '{self.STORE_ID}';")
        if len(data) == 0:
            raise AttributeError(
                f'Can not find data in Store List. Please check database setting for Store ({self.STORE_ID})')
        data = data.iloc[0]
        self.Setting.SetValue(self.config.StoreList.TABLE_ORDER, json.loads(data[self.config.StoreList.TABLE_ORDER]))
        self.RefreshMenu()

    def RefreshMenu(self):
        with self.Lock:
            try:
                data = pd.read_sql(
                    f'select * from {self.config.MenuList.NAME} where {self.config.MenuList.STORE_ID} = '
                    f'{self.STORE_ID}',
                    self.conn)
                self.SaveMenu(data)
            except Exception:
                query = (f'select * from {self.config.MenuList.NAME} where {self.config.MenuList.STORE_ID} = '
                         f'{self.STORE_ID}')
                with sqlite3.connect(Config.DataBase.PATH) as conn:
                    self.logger.info(f'query: {query}')
                    data = pd.read_sql(query, conn)
        self.menu.clear()
        self.menu.setUp(data)

    def HardReloadData(self):
        pass  # Todo

    def SaveMenu(self, data: pd.DataFrame):
        table = self.config.MenuList.NAME
        self.SaveLocalData(data, table)

    def UpdateOneLineLocally(self, data, table):
        Value = ''
        for field in table.COLUMNS:
            if Value != '':
                Value += ', '
            Value += f"`{field}`='{data[field]}'"
        self.executeLocally(
            f"Update {table.NAME} Set {Value}, `{self.config.UPDATED}`=true, `{self.config.LOADED}`=true "
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
                f"select * from {table.NAME} where {self.config.LOADED} = false and {table.ID_STORE}={self.STORE_ID};")
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
                self.executeLocally(
                    f"update {table.NAME} set {self.config.LOADED}='1', {self.config.UPDATED}='1' where "
                    f"{self.STORE_ID} and {table.ID} in ({','.join(data[table.ID].astype(str))})")

    def Download_(self):
        for table in [self.config.OrderList, self.config.OrderMetaData, self.config.PendingOnlineOrder]:
            data = self.get_data(
                f"select * from {table.NAME} where {self.config.LOADED} = false and {table.ID_STORE}={self.STORE_ID};")
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
                             f"{table.ID_STORE}={self.STORE_ID} and {table.ID} in ({','.join(data[table.ID].astype(str))})")

            if table == self.config.OrderList:
                self.TableInfo.AddOrderInfo(data)
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
        Name = self.menu[Order[table.ID_FOOD]].NameCN
        TableID = self.TableInfo.ByOrderIDDict[Order[table.ID_ORDER]].TablID
        Qty = Order[table.QTY]
        Note = Order[table.NOTE]
        Time = datetime.now()
        Type = self.menu[Order[table.ID_FOOD]].Type
        text = f'''Table: {TableID}
{Name}   X   {Qty}
{Note}
{Time}'''
        if Type in [1, 2, 3, 4]:
            self.Printer.SendOrder(text, self.Printer.DefaultKitchenPrinter)
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
        self.TableInfo.UpdateTime = time.time()

    def DataBaseCheck(self):
        tablelist = self.get_local_data(f"SELECT name FROM sqlite_master WHERE type='table';")
        for i in [self.config.OrderList, self.config.OrderMetaData]:
            if i.NAME not in tablelist['name'].to_list():
                self.executeLocally(i.INITIAL_QUERY)
                self.HardLoadData(i)

    def HardLoadData(self, Table):
        data = self.get_data(f"select * from {Table.NAME} where {Table.ID_STORE}={self.STORE_ID};")
        if len(data) > 0:
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
