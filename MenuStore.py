import pandas as pd
from Config import Config
from collections import defaultdict


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
        self.NameEN = data[confg.Name_EN]
        self.NameCN = data[confg.NAME_CN]
        self.RestQty = data[confg.QTY]
        self.Note = data[confg.NOTE]


class FullMenuList(dict):
    def __init__(self):
        dict.__init__(self)
        self._dict = defaultdict(Food)

    def clear(self):
        self._dict = defaultdict(Food)

    def _setUp(self, data: pd.Series):
        confg = Config.DataBase.MenuList
        self._dict[data[confg.ID]].setUp(data)

    def setUp(self, data: pd.DataFrame):
        self._dict.clear()
        data.apply(self._setUp, axis=1)
