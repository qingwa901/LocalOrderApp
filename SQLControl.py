# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 21:17:19 2024

@author: qingw
"""

from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd
import time
import threading

_user = 'ZhangjiTestSQL'
_password = 'k|h{c^fFoZV|!u+3OZR*FtuBxk2a`c;m'
_host = 'ls-e8857edd09f969e89d8376a1f48de46125784e86.ch6q8iw28g5e.eu-west-2.rds.amazonaws.com'
_port = 3306
_database = 'bitnami_wordpress'
_sleepsec = 2


class SQLControl:
    def __init__(self, logger):
        self.open = True
        self.engine = create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            _user, _password, _host, _port, _database
        ))
        self.logger = logger
        self.Connected = False
        self.build_connection()
        self.Lock = threading.Lock()

    def build_connection(self):
        while self.open:
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
        while self.open:
            try:
                with self.Lock:
                    self.logger.info(f'query: {query}')
                    data = pd.read_sql(query, self.conn)
                    return data
            except sqlalchemy.exc.DBAPIError as e:
                self.logger.error(
                    "Lost connection. Try to reconnect database.", exc_info=e)
                self.Connected = False
                time.sleep(_sleepsec)
                self.build_connection()

    def SaveData(self, data: pd.DataFrame, Table):
        while self.open:
            try:
                with self.Lock:
                    self.logger.info(f'Table: {Table}')
                    data.to_sql(Table, self.conn)
                    return True
            except sqlalchemy.exc.DBAPIError as e:
                self.logger.error(
                    "Lost connection. Try to reconnect database.", exc_info=e)
                self.Connected = False
                time.sleep(_sleepsec)
                self.build_connection()

    def execute(self, query):
        while self.open:
            try:
                with self.Lock:
                    self.logger.info(f'query: {query}')
                    return self.conn.execute(query)
            except sqlalchemy.exc.DBAPIError as e:
                self.logger.error(
                    "Lost connection. Try to reconnect database.", exc_info=e)
                self.Connected = False
                time.sleep(_sleepsec)
                self.build_connection()
