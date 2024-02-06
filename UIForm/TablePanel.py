# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 21:47:54 2024

@author: qingw
"""

import wx
from .TableBut import TableBut
from DataBase import DataBase
from logging import Logger
from Config import Config


class TablePanel(wx.Panel):
    """"""

    def __init__(self, parent, logger: Logger, DataBase: DataBase):
        """Constructor"""
        self._DataBase = DataBase
        wx.Panel.__init__(self, parent=parent)
        self.TableList = {}
        self._Logger = logger

        # vbox = wx.BoxSizer(wx.VERTICAL)
        TableList = DataBase.Setting.GetValue(Config.DataBase.StoreList.TABLE_ORDER)
        ColNum = max([len(x) for x in TableList])
        RowNum = len(TableList)
        gs = wx.GridSizer(RowNum, ColNum, 3, 3)
        for row in TableList:
            for table in row:
                if table is None:
                    gs.Add((100, -1), wx.ID_ANY)
                else:
                    table_but = TableBut(self, table, self._Logger, self._DataBase)
                    self.TableList[table] = table_but
                    gs.Add(table_but, wx.ID_ANY)
        self.SetSizer(gs)

    def RefreshTableDetail(self):

        pass #Todo
