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

class DataBase(SQLControl):
    def __init__(self, logger: logging.Logger, path):
        SQLControl.__init__(self, logger)
        self.logger = logger
        self.Setting = ConfigSetting(logger)
        self.Printer = PrinterControl(self.logger, self.Setting)
        self.path = path
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.tmp_path = path + '/tmp'
        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)
        self.config = Config().DataBase
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
        self.GetMenu()

    def GetMenu(self):
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
        data.to_csv(self.path + '/' + table + '.csv')

    def SaveOrder(self, data: pd.DataFrame):
        table = self.config.OrderList.NAME
        self.AddLine(data, self.path + '/' + table + '.csv')
        path = self.tmp_path + f'/{table}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
        self.AddLine(data, path)

    def SaveMetaOrder(self, data: pd.DataFrame):
        table = self.config.OrderMetaData.NAME
        self.AddLine(data, self.path + '/' + table + '.csv')
        path = self.tmp_path + f'/{table}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
        self.AddLine(data, path)

    def Update(self):
        FileList = os.listdir(self.tmp_path)
        for filename in FileList:
            data = pd.read_csv(self.tmp_path + '/' + filename)
            data[self.config.DOWNLOADED] = True
            self.SaveData(data, filename.split('_')[0])
            os.remove(self.tmp_path + '/' + filename)

    def Download(self):
        table = self.config.OrderList
        data = self.get_data(f'select * from {table.NAME} where {self.config.DOWNLOADED}=false;')
        if len(data) > 0:
            self.AddLine(data, self.path + '/' + table.NAME + '.csv')
            self.execute(
                f"update {table.NAME} set {self.config.DOWNLOADED}='1' where {table.ID_STORE}= "
                f"{self.STORE_ID} and {table.ID} in ({','.join(data[table.ID])})")

        table = self.config.OrderMetaData
        data = self.get_data(f'select * from {table.NAME} where {self.config.DOWNLOADED}=false;')
        if len(data) > 0:
            self.AddLine(data, self.path + '/' + table.NAME + '.csv')
            self.execute(
                f"update {table.NAME} set {self.config.DOWNLOADED}='1' where {table.ID_STORE}= "
                f"{self.STORE_ID} and {table.ID_ORDER} in ({','.join(data[table.ID_ORDER])})")

    def AutoUpdate(self):
        while self.open:
            try:
                self.Update()
                self.Download()
            except Exception as e:
                self.logger.error('Unknown Error. Retry in 3 sec.', exc_info=e)
            finally:
                time.sleep(3)
