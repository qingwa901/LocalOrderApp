# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 21:40:23 2024

@author: qingw
"""
import os
import time

from .SQLControl import SQLControl
from .Config import Config
from .ConfigSetting import ConfigSetting
import pandas as pd
import threading
from datetime import datetime
import logging


class DataBase(SQLControl):
    def __init__(self, logger: logging.Logger, setting: ConfigSetting, path):
        SQLControl.__init__(self, logger)
        self._logger = logger
        self._setting = setting
        self.path = path
        self._config = Config().DataBase
        self.InitialLoadData()
        self.Lock = threading.Lock()

    def InitialLoadData(self):
        data = self.get_data(
            f'select * from {self._config.STORE_INFO} where {self._config.StoreList.ID} == {self._config.STORE_ID}')
        if len(data) == 0:
            raise AttributeError(
                f'Can not find data in Store List. Please check database setting for Store ({self._config.STORE_ID})')
        data = data[0]
        self._setting.ChangeValue(self._config.StoreList.TABLE_ORDER, data[self._config.StoreList.TABLE_ORDER])

    def SaveOrder(self, data: pd.DataFrame):
        table = self._config.ORDER_LIST
        data.to_parquet(self.path + '/' + table + '.parquet')
        path = self.path + f'/{table}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
        data.to_parquet(path)

    def SaveOrderDetail(self, data: pd.DataFrame):
        table = self._config.ORDER_META_DATA
        data.to_parquet(self.path + '/' + table + '.parquet')
        path = self.path + f'/{table}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
        data.to_parquet(path)

    def Update(self):
        while True:
            try:
                FileList = os.listdir(self.path)
                for filename in FileList:
                    if filename not in [self._config.ORDER_META_DATA + '.parquet', self._config.ORDER_LIST + '.parquest']:
                        data = pd.read_parquet(self.path + '/' + filename)
                        data[self._config.DOWNLOADED] = True
                        self.SaveData(data, filename.split('_')[0])
                        os.remove(self.path + '/' + filename)
            except Exception as e:
                self._logger.error("Unknown Error. Retry in 20 sec", exc_info=e)
                time.sleep(20)

    def Download(self):
        for table in [self._config.ORDER_LIST, self._config.ORDER_META_DATA]:
            data = self.get_data(f'select * from {table} where {self._config.DOWNLOADED}=false;')
            data.to_parquet()