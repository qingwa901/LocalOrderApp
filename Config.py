# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 22:29:57 2024

@author: qingw
"""


class Config:
    class DataBase:
        STORE_INFO = 'StoreList'
        STORE_ID = 0  # temperately put it in config. Later should put it into setting file.
        LOADED = 'Loaded'
        UPDATED = 'Updated'
        PATH = 'DataBase.sql'

        class MenuList:
            NAME = 'MenuList'
            ID = 'ID'
            STORE_ID = 'IDStore'
            FOOD_NAME = 'FoodName'
            PRICE = 'Price'
            FOOD_TYPE = 'FoodType'
            QTY = 'Qty'
            NOTE = 'Note'
            VALID = 'Valid'
            COLUMNS = [STORE_ID, FOOD_NAME,
                       PRICE, FOOD_TYPE, QTY, NOTE, VALID]

        class OrderMetaData:
            NAME = 'OrderMetaData'
            ID = 'ID'
            ID_ORDER = 'OrderID'
            ID_STORE = 'StoreID'
            FIELD = 'Field'
            VALUE = 'Value'
            CREATE_TIME = 'CreatTime'
            VALID = 'Valid'
            COLUMNS = [ID_ORDER, ID_STORE, FIELD, VALUE, CREATE_TIME, VALID]

            class Fields:
                START_TIME = 'StartTime'
                END_TIME = 'EndTime'
                IS_FINISHED = 'IsFinished'
                NUM_OF_PEOPLE = 'NumOfPeople'

        class OrderList:
            NAME = 'OrderList'
            ID = 'ID'
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
            VALID = 'Valid'
            COLUMNS = [ID_ORDER, ID_TABLE, ID_STORE, ID_FOOD, ID_STAFF, QTY, UNIT_PRICE, CREATE_TIME, NOTE, EOD_COUNTED,
                       VALID]

        class StoreList:
            ID = 'ID'
            STORE_NAME = 'StoreName'
            ID_MANAGER = 'IDManager'
            TABLE_ORDER = 'TableOrder'
            NOTE = 'Note'

    class UI:
        class EatInPage:
            ToolBarSize = 35
            StatusButSize = (50, 50)
            TableButSize = (100, 100)

