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
        TMP_PRINT_PDF_PATH = 'D:/Code/tmp2.pdf'

        class MenuList:
            NAME = 'MenuList'
            ID = 'ID'
            ID_STORE = 'IDStore'
            NAME_CN = 'NameCN'
            NAME_EN = 'NameEN'
            PRICE = 'Price'
            FOOD_TYPE = 'FoodType'
            QTY = 'Qty'
            NOTE = 'Note'
            VALID = 'Valid'
            COLUMNS = [ID_STORE, NAME_CN, NAME_EN,
                       PRICE, FOOD_TYPE, QTY, NOTE, VALID]
            DISPLAYLIST = [NAME_CN, QTY, PRICE, NOTE]

            INITIAL_QUERY = '''CREATE TABLE `MenuList` (
                      `ID` int NOT NULL,
                      `IDStore` int NOT NULL,
                      `NameCN` varchar(225) DEFAULT NULL,
                      `NameEN` varchar(225) NOT NULL,
                      `Price` decimal(10,2) NOT NULL,
                      `FoodType` int NOT NULL,
                      `Qty` int NOT NULL,
                      `Note` varchar(225) DEFAULT NULL,
                      `Valid` tinyint NOT NULL DEFAULT '1'
                    );
                    '''

        class OrderMetaData:
            NAME = 'OrderMetaData'
            ID = 'ID'
            ID_ORDER = 'OrderID'
            ID_STORE = 'StoreID'
            FIELD = 'Field'
            VALUE = 'Value'
            CREATE_TIME = 'CreateTime'
            VALID = 'Valid'
            COLUMNS = [ID_ORDER, ID_STORE, FIELD, VALUE, CREATE_TIME, VALID]
            INITIAL_QUERY = '''CREATE TABLE `OrderMetaData` (
              `ID` int NOT NULL,
              `OrderID` int NOT NULL,
              `StoreID` varchar(45) NOT NULL,
              `Field` varchar(225) NOT NULL,
              `Value` varchar(225) NOT NULL,
              `CreateTime` datetime NOT NULL,
              `Valid` tinyint NOT NULL DEFAULT '1',
              `Loaded` tinyint NOT NULL DEFAULT '0',
              `Updated` tinyint NOT NULL DEFAULT '1'
            ) ;
            '''

            class Fields:
                START_TIME = 'StartTime'
                END_TIME = 'EndTime'
                IS_FINISHED = 'IsFinished'
                NUM_OF_PEOPLE = 'NumOfPeople'
                ID_TABLE = 'IDTable'
                CASH = 'Cash'
                CARD = 'Card'
                DISCOUNT_PERCENT = 'DiscountPercent'
                SERVICE_CHARGE_PERCENT = 'ServiceChargePercent'

        class OrderList:
            NAME = 'OrderList'
            ID = 'ID'
            ID_ORDER = 'IDOrder'
            ID_STORE = 'IDStore'
            ID_FOOD = 'IDFood'
            ID_STAFF = 'IDStaff'
            QTY = 'Qty'
            UNIT_PRICE = 'UnitPrice'
            CREATE_TIME = 'CreateTime'
            NOTE = 'Note'
            EOD_COUNTED = 'EODCounted'
            VALID = 'Valid'
            COLUMNS = [ID_ORDER, ID_STORE, ID_FOOD, ID_STAFF, QTY, UNIT_PRICE, CREATE_TIME, NOTE, EOD_COUNTED,
                       VALID]
            INITIAL_QUERY = '''CREATE TABLE `OrderList` (
              `ID` int NOT NULL,
              `IDOrder` int NOT NULL,
              `IDStore` int NOT NULL,
              `IDFood` int NOT NULL,
              `IDStaff` bigint unsigned NOT NULL,
              `Qty` int NOT NULL,
              `UnitPrice` decimal(10,2) NOT NULL,
              `CreateTime` datetime NOT NULL,
              `Note` varchar(225) DEFAULT NULL,
              `EODCounted` tinyint NOT NULL DEFAULT '0',
              `Valid` tinyint NOT NULL DEFAULT '1',
              `Loaded` tinyint NOT NULL DEFAULT '0',
              `Updated` tinyint NOT NULL DEFAULT '1'
            );
            '''

        class StoreList:
            ID = 'ID'
            STORE_NAME = 'StoreName'
            ID_MANAGER = 'IDManager'
            TABLE_ORDER = 'TableOrder'
            NOTE = 'Note'
            NAME = 'StoreList'
            INITIAL_QUERY = '''CREATE TABLE `StoreList` (
              `ID` int NOT NULL,
              `StoreName` varchar(225) NOT NULL,
              `TableOrder` varchar(225) DEFAULT NULL,
              `Note` varchar(225) DEFAULT NULL
            ) ;
            '''

        class PendingOnlineOrder:
            NAME = 'PendingOnlineOrder'
            ID = 'ID'
            ID_TABLE = 'TableNumber'
            ID_STORE = 'StoreNumber'
            ID_FOOD = 'FoodID'
            QTY = 'Qty'
            NOTE = 'Note'
            CREATE_TIME = 'CreateTime'
            VALID = 'IsValid'
            COLUMNS = [ID, ID_TABLE, ID_STORE, ID_FOOD, QTY, NOTE, CREATE_TIME, VALID]
            INITIAL_QUERY = '''CREATE TABLE `PendingOnlineOrder` (
              `ID` int NOT NULL,
              `TableNumber` int NOT NULL,
              `StoreNumber` int NOT NULL,
              `FoodID` int NOT NULL,
              `Qty` int NOT NULL,
              `Note` varchar(225) DEFAULT NULL,
              `CreateTime` datetime NOT NULL,
              `IsValid` tinyint NOT NULL DEFAULT '1',
              `Loaded` tinyint NOT NULL DEFAULT '0',
              `Updated` tinyint NOT NULL DEFAULT '1'
            );'''

        class ManuPageList:
            ID = 'id'
            NAME = 'ManuPageList'
            ID_STORE = 'StoreID'
            EN_NAME = 'ENName'
            CN_NAME = 'CNName'
            VALID = 'Valid'
            INITIAL_QUERY = '''CREATE TABLE `ManuPageList` (
          `id` int NOT NULL,
          `StoreID` int NOT NULL,
          `ENName` varchar(225) NOT NULL,
          `CNName` varchar(225) NOT NULL,
          `Valid` tinyint NOT NULL DEFAULT '1'
        )'''

        class Staff:
            NAME = 'Staff'
            ID = 'ID'
            ID_STORE = 'StoreID'
            STAFF_NAME = 'StaffName'
            VALID = 'Valid'
            INITIAL_QUERY = '''CREATE TABLE `Staff` (
              `ID` int NOT NULL,
              `StoreID` int NOT NULL,
              `StaffName` varchar(225) NOT NULL,
              `Valid` tinyint NOT NULL DEFAULT '1'
            ) '''

    class UI:
        class EatInPage:
            ToolBarSize = 35
            StatusButSize = (50, 50)
            TableButSize = (100, 100)

    class DisplaySetting:
        class OrderTable:
            COL_NAME_EN = ['FoodName', 'Qty', 'UnitPrice', 'Note']
            COL_NAME_CN = ['菜名', '数量', '单价', '备注']

        class HistoryOrderTable:
            COL_NAME_EN = ['FinishTime', 'OrderID', 'TableID', 'TotalAmount', 'ServiceCharge', 'Discount', 'Cash',
                           'Card']
            COL_NAME_CN = ['结束时间', '订单号', '桌号', '总价', '服务费', '折扣', '现金', '刷卡']

        class MenuTag:
            TAG = "tag"
            NAME = "Name"
            PRICE_ADD = "PriceAdd"

    class ValueSetting:
        class TableOrder:
            SERVICE_CHARGE_PERCENT_LIST = [5, 7.5, 10, 12.5]
            DISCOUNT_PERCENT_LIST = [5, 10, 15, 20, 25, 30]
            STR_DEFAULT_SERVICE_CHARGE_PERCENT = 'DefaultServiceChargePercent'
            STR_DEFAULT_DISCOUNT_PERCENT_A = 'DefaultDiscountPercentA'
            STR_DEFAULT_DISCOUNT_PERCENT_B = 'DefaultDiscountPercentB'

        class Manu:
            EN_NAME = 'Menu.ENName'
            CN_NAME = 'Menu.CNName'

        class Printer:
            STR_CASHIER_PRINTER = 'Printer.DefaultCashierPrinter'
            STR_KITCHEN_PRINTER = 'Printer.DefaultKitchenPrinter'
