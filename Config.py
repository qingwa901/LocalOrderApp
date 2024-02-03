# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 22:29:57 2024

@author: qingw
"""


class Config:
    class DataBase:
        MENU_LIST = 'MenuList'
        ORDER_META_DATA = 'OrderMetaData'
        STORE_INFO = 'StoreList'
        ORDER_LIST = 'OrderList'
        STORE_ID = 0 # temperately put it in config. Later should put it into setting file.
        DOWNLOADED = 'Downloaded'
        UPLOADED = 'Uploaded'

        class MenuList:
            ID = 'ID'
            STORE_ID = 'IDStore'
            FOOD_NAME = 'FoodName'
            PRICE = 'Price'
            FOOD_TYPE = 'FoodType'
            QTY = 'Qty'
            NOTE = 'Note'
            VALID = 'Valid'
            COLUMNS = [ID, STORE_ID, FOOD_NAME,
                       PRICE, FOOD_TYPE, QTY, NOTE, VALID]

        class OrderMetaData:
            ORDER_ID = 'OrderID'
            STORE_ID = 'StoreID'
            TABLE_ID = 'TableID'
            FIELD = 'Field'
            VALUE = 'Value'
            CREATE_TIME = 'CreatTime'
            COLUMNS = [ORDER_ID, STORE_ID, TABLE_ID, FIELD, VALUE, CREATE_TIME]

        class OrderList:
            ID_ORDER = 'IDOrder'
            ID_TABLE = 'IDTable'
            ID_STORE = 'IDStore'
            ID_FOOD = 'IDFood'
            ID_STAFF = 'IDStaff'
            QTY = 'Qty'
            UNIT_PRICE = 'UnitPrice'
            CREATE_TIME = 'CreateTime'
            NOTE = 'Note'
            EOD_COUNTED = 'EODCounted'

        class StoreList:
            ID = 'ID'
            STORE_NAME = 'StoreName'
            ID_MANAGER = 'IDManager'
            TABLE_ORDER = 'TableOrder'
            NOTE = 'Note'
