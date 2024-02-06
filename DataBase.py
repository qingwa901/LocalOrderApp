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
from datetime import datetime
from PrinterControl import PrinterControl
import logging
import json
from TableInfoStore import AllTableInfoStore


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
        self.menu = None
        self.InitialLoadData()
        self.auto_update = threading.Thread(target=self.AutoUpdate)
        self.auto_update.start()

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
                data = pd.read_sql(
                    f'select * from {self.config.MenuList.NAME} where {self.config.MenuList.STORE_ID} = '
                    f'{self.STORE_ID}',
                    self.local_conn)
        self.menu = data

    def RefreshOrderList(self):
        with self.Lock:
            try:
                data = pd.read_sql(
                    f'select * from {self.config.MenuList.NAME} where {self.config.MenuList.STORE_ID} = '
                    f'{self.STORE_ID}',
                    self.conn)
                self.SaveMenu(data)
            except Exception:
                data = pd.read_csv(self.path + '/' + self.config.MenuList.NAME + '.csv')
        self.menu = data

    def SaveFile(self, data: pd.DataFrame, tablename: str):
        x = threading.Thread(target=self.AddLine, args=(data, tablename))
        x.start()

    def AddLine(self, tmp: pd.DataFrame, name: str):
        while True:
            try:
                with self.Lock:
                    if os.path.isfile(name):
                        tmp.to_csv(name, index=False, header=False, mode='a')
                    else:
                        tmp.to_csv(name, index=False, mode='a')
                return
            except OSError as e:
                self.logger.error('Meet error in save data. Retry in 1 sec.', exc_info=e)
                time.sleep(1)

    def HardReloadData(self):
        pass  # Todo

    def SaveMenu(self, data: pd.DataFrame):
        table = self.config.MenuList.NAME
        self.SaveLocalData(data, table)

    def SaveOrder(self, data: pd.DataFrame):
        table = self.config.OrderList.NAME
        self.AddLine(data, self.path + '/' + table + '.csv')
        path = self.tmp_path + f'/{table}_Save_{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
        self.AddLine(data, path)

    def SaveMetaOrder(self, data: pd.DataFrame):
        table = self.config.OrderMetaData.NAME
        self.AddLine(data, self.path + '/' + table + '.csv')
        path = self.tmp_path + f'/{table}_Save_{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
        self.AddLine(data, path)

    def UpdateOrder(self, data: pd.DataFrame):
        table = self.config.OrderList.NAME
        self.AddLine(data, self.path + '/' + table + '.csv')
        path = self.tmp_path + f'/{table}_Save_{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
        self.AddLine(data, path)

    def UpdateMetaOrder(self, data: pd.DataFrame):
        table = self.config.OrderMetaData.NAME
        self.AddLine(data, self.path + '/' + table + '.csv')
        path = self.tmp_path + f'/{table}_Save_{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
        self.AddLine(data, path)

    def UpdateOneLineLocally(self, data, table):
        Value = ''
        for field in table.COLUMNS:
            if Value != '':
                Value += ' and '
            Value += f"{field} = '{data[field]}'"
        self.executeLocally(
            f"Update {table.Name} Set ({Value} and {self.config.UPDATED} = true and {self.config.LOADED} = true) "
            f"where {table.ID_STORE} = {self.STORE_ID} and {table.ID} = {data[table.ID]}")

    def UpdateOneLine(self, data, table):
        Value = ''
        for field in table.COLUMNS:
            if Value != '':
                Value += ' and '
            Value += f"{field} = '{data[field]}'"
        self.execute(
            f"Update {table.Name} Set ({Value} and {self.config.UPDATED} = true and {self.config.LOADED} = true) "
            f"where {table.ID_STORE} = {self.STORE_ID} and {table.ID} = {data[table.ID]}")

    def Update(self):
        for table in [self.config.OrderList, self.config.OrderMetaData]:
            data = self.get_local_data(f"select * from {table.NAME} where {self.config.LOADED} = false")
            if len(data) > 0:
                data[self.config.LOADED] = True
                data[self.config.UPDATED] = True
                self.SaveData(data, table.NAME)
                self.executeLocally(
                    f"update {table.NAME} set ({self.config.LOADED}='1', {self.config.UPDATED}='1') where {table.ID_STORE}="
                    f"{self.STORE_ID} and {table.ID} in ({','.join(data[table.ID])})")

            data = self.get_local_data(
                f"select * from {table.NAME} where {self.config.UPDATED} = false and {self.config.LOADED} = true")
            if len(data) > 0:
                data[self.config.UPDATED] = True
                data.apply(self.UpdateOneLine, axis=1)
                self.executeLocally(
                    f"update {table.NAME} set ({self.config.UPDATED}='1') where {table.ID_STORE}= "
                    f"{self.STORE_ID} and {table.ID} in ({','.join(data[table.ID])})")

    def Download(self):
        for table in [self.config.OrderList, self.config.OrderMetaData]:
            data = self.get_data(f"select * from {table.NAME} where {self.config.LOADED} = false")
            if len(data) > 0:
                data[self.config.LOADED] = True
                data[self.config.UPDATED] = True
                self.SaveLocalData(data, table.NAME)
                self.execute(
                    f"update {table.NAME} set ({self.config.LOADED}='1', {self.config.UPDATED}='1') where {table.ID_STORE}="
                    f"{self.STORE_ID} and {table.ID} in ({','.join(data[table.ID])})")

            data = self.get_data(
                f"select * from {table.NAME} where {self.config.UPDATED} = false and {self.config.LOADED} = true")
            if len(data) > 0:
                data[self.config.UPDATED] = True
                data.apply(self.UpdateOneLineLocally, axis=1)
                self.execute(
                    f"update {table.NAME} set ({self.config.UPDATED}='1') where {table.ID_STORE}= "
                    f"{self.STORE_ID} and {table.ID} in ({','.join(data[table.ID])})")

    def AutoUpdate(self):
        while self.open:
            try:
                self.Update()
                self.Download()
            except Exception as e:
                self.logger.error('Unknown Error. Retry in 3 sec.', exc_info=e)
            finally:
                for _ in range(3):
                    time.sleep(1)
                    if not self.open:
                        break

    def GetOpenTableInfo(self):
        query = (f"select {Config.DataBase.OrderMetaData.ID_ORDER} from {Config.DataBase.OrderMetaData.NAME} where "
                 f"{Config.DataBase.OrderMetaData.FIELD}='{Config.DataBase.OrderMetaData.Fields.IS_FINISHED}' and "
                 f"{Config.DataBase.OrderMetaData.VALUE}=false and "
                 f"{Config.DataBase.OrderMetaData.ID_STORE}='{self.STORE_ID}'")
        OpenTable = self.get_local_data(query)
        self.OpenOrderList = OpenTable[Config.DataBase.OrderMetaData.ID_ORDER].to_list()
        self.TableInfo.Clear()
        if len(self.OpenOrderList) > 0:
            OpenOrderListStr = "', '".join(self.OpenOrderList)
            query = (f"select * from {Config.DataBase.OrderList.NAME} where "
                     f"{Config.DataBase.OrderList.ID_ORDER} in ('{OpenOrderListStr}' and "
                     f"{Config.DataBase.OrderList.ID_STORE}='{self.STORE_ID}'")
            OrderList = self.get_local_data(query)
            query = (f"select * from {Config.DataBase.OrderMetaData.NAME} where "
                     f"{Config.DataBase.OrderMetaData.ID_STORE}='{self.STORE_ID}'")
            OrderMetaList = self.get_local_data(query)
            self.TableInfo.UpdateTime = time.time()
            self.TableInfo.ConverOrderData(OrderList, OrderMetaList)
