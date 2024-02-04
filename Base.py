# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 18:49:08 2024

@author: qingw
"""

import wx
from Logger import CreateLogger
# from .LogIn import LogIn
from UIForm.EatInTable import EatInTable
from datetime import datetime
from DataBase import DataBase


class Base:
    def __init__(self, logger=None):
        if logger is None:
            filename = f"Log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            self._logger = CreateLogger(f'OrderSystem', filename)
        else:
            self._logger = logger
        self._DataBase = DataBase(self._logger, 'DataBase')
        self._logger.info('App start')
        self.app = wx.App()
        self.EatInTable = EatInTable(
            None, self._logger, self._DataBase)
        self.EatInTable.Show()

    def run(self):
        self.app.MainLoop()


if __name__ == '__main__':
    x = Base()
    x.run()
