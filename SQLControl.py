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
from Config import Config
import sqlite3

_user = 'ZhangjiTestSQL'
_password = 'k|h{c^fFoZV|!u+3OZR*FtuBxk2a`c;m'
_host = 'ls-e8857edd09f969e89d8376a1f48de46125784e86.ch6q8iw28g5e.eu-west-2.rds.amazonaws.com'
_port = 3306
_database = 'bitnami_wordpress'
_sleepsec = 2


class SQLControl:
    def __init__(self, logger):
        self.open = True
        self.Lock = threading.Lock()
        self.LocalLock = threading.Lock()
        self.engine = create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            _user, _password, _host, _port, _database
        ))
        self.logger = logger
        self.Connected = False
        self.Local_Connected = False
        self.build_connection()
        self.build_local_connection()

    def build_local_connection(self):
        while self.open:
            try:
                with self.LocalLock:
                    self.local_conn = sqlite3.connect(Config.DataBase.PATH)
                    self.logger.info("Successfully connect to local database.")
                    self.Local_Connected = True
                    return
            except sqlalchemy.exc.DBAPIError as e:
                self.logger.error(
                    "Lost connection. Try to reconnect local database.", exc_info=e)
                time.sleep(_sleepsec)
                self.logger.info("Reconnecting local database.")

    def get_local_data(self, query):
        while self.open:
            try:
                with self.LocalLock:
                    self.logger.info(f'query: {query}')
                    data = pd.read_sql(query, self.local_conn)
                    return data
            except sqlalchemy.exc.DBAPIError as e:
                self.logger.error(
                    "Lost Local connection. Try to reconnect Local database.", exc_info=e)
                self.Local_Connected = False
                time.sleep(_sleepsec)
                self.build_local_connection()

    def SaveLocalData(self, data: pd.DataFrame, Table):
        while self.open:
            try:
                with self.LocalLock:
                    self.logger.info(f'Table: {Table}')
                    data.to_sql(Table, self.local_conn)
                    return True
            except sqlalchemy.exc.DBAPIError as e:
                self.logger.error(
                    "Lost Local connection. Try to reconnect Local database.", exc_info=e)
                self.Local_Connected = False
                time.sleep(_sleepsec)
                self.build_local_connection()

    def executeLocally(self, query):
        while self.open:
            try:
                with self.LocalLock:
                    self.logger.info(f'query: {query}')
                    return self.local_conn.execute(query)
            except sqlalchemy.exc.DBAPIError as e:
                self.logger.error(
                    "Lost Local connection. Try to reconnect Local database.", exc_info=e)
                self.Local_Connected = False
                time.sleep(_sleepsec)
                self.build_local_connection()

    def build_connection(self):
        while self.open:
            try:
                with self.Lock:
                    self.conn = self.engine.connect()
                    self.logger.info("Successfully connect to database.")
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
