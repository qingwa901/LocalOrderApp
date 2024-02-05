# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 21:50:06 2024

@author: qingw
"""

import wx
from Config import Config
from DataBase import DataBase
from logging import Logger


class TableBut(wx.Button):
    def __init__(self, parent, TableNum, logger: Logger, DataBase: DataBase):
        self._logger = logger
        self._database = DataBase
        size = Config.UI.EatInPage.TableButSize
        wx.Button.__init__(self, parent=parent, id=-1,
                           label=f"{TableNum} 号桌", size=size)
        self._StartTime = None

    def BindEvent(self, event):
        self.Bind(wx.EVT_BUTTON, event)

    def SetStartTime(self, value):
        if value is None:
            self.SetBackgroundColour('white')
        else:
            self.SetBackgroundColour('Orange')
        self._StartTime = value

    def GetStartTime(self):
        return self._StartTime

    StartTime = property(GetStartTime, SetStartTime)


