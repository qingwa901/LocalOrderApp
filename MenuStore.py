import pandas as pd
from Config import Config
import json


class Food:
    ID = None
    Type = None
    UnitPrice = None
    RestQty = None
    NameEN = None
    NameCN = None
    Note = None

    def setUp(self, data: pd.Series):
        confg = Config.DataBase.MenuList
        self.ID = data[confg.ID]
        self.Type = data[confg.FOOD_TYPE]
        self.UnitPrice = data[confg.PRICE]
        self.NameEN = data[confg.NAME_EN]
        self.NameCN = data[confg.NAME_CN]
        self.RestQty = data[confg.QTY]
        if data[confg.NOTE] is not None:
            self.Note = json.loads(data[confg.NOTE])
            #{"Tag":{Name: "", PriceAdd: ""}}


class FullMenuList:
    def __init__(self):
        self.Foods = dict()

    def clear(self):
        self.Foods = dict()

    def _setUp(self, data: pd.Series):
        confg = Config.DataBase.MenuList
        if data[confg.ID] not in self.Foods:
            self.Foods[data[confg.ID]] = Food()
        self.Foods[data[confg.ID]].setUp(data)

    def setUp(self, data: pd.DataFrame):
        self.Foods.clear()
        data.apply(self._setUp, axis=1)
