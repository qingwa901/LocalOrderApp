# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 21:17:19 2024

@author: qingw
"""

from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd
import time

_user = 'usagimai_WPJIU'
_password = 'H1a!=gYrc6Wyi&)!R'
_host = 'www.usagimaid.com'
_port = 3306
_database = 'usagimai_WPJIU'
_sleepsec = 2


class SQLControl:
    def __init__(self, logger):
        self.engine = create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            _user, _password, _host, _port, _database
        ))
        self.logger = logger
        self.Connected = False
        self.build_connection()

    def build_connection(self):
        while True:
            try:
                self.conn = self.engine.connect()
                self.logger.info("Succesfully connect to database.")
                self.Connected = True
                return
            except sqlalchemy.exc.DBAPIError as e:
                self.logger.error(
                    "Lost connection. Try to reconnect database.", exc_info=e)
                time.sleep(_sleepsec)
                self.logger.info("Reconnecting database.")

    def get_data(self, query):
        while True:
            try:
                data = pd.read_sql(query, self.conn)
                return data
            except sqlalchemy.exc.DBAPIError as e:
                self.logger.error(
                    "Lost connection. Try to reconnect database.", exc_info=e)
                self.Connected = False
                time.sleep(_sleepsec)
                self.build_connection()

    def SaveData(self, data:pd.DataFrame, Table):
        while True:
            try:
                data.to_sql(Table,self.conn)
                return True
            except sqlalchemy.exc.DBAPIError as e:
                self.logger.error(
                    "Lost connection. Try to reconnect database.", exc_info=e)
                self.Connected = False
                time.sleep(_sleepsec)
                self.build_connection()

    def execute(self, query):
        while True:
            try:
                return self.conn.execute(query)
            except sqlalchemy.exc.DBAPIError as e:
                self.logger.error(
                    "Lost connection. Try to reconnect database.", exc_info=e)
                self.Connected = False
                time.sleep(_sleepsec)
                self.build_connection()
