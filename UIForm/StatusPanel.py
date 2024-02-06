# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 20:15:56 2024

@author: qingw
"""

import wx
from DataBase import DataBase
from Config import Config
from logging import Logger


class StatusPanel(wx.Panel):
    """"""

    def __init__(self, parent, logger: Logger, DataBase: DataBase):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self._DataBase = DataBase
        self._Logger = logger

        vSizer = wx.BoxSizer(wx.VERTICAL)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "桌号: ")
        hSizer.Add(label)
        self.TableNumber = wx.StaticText(self, -1, "")
        hSizer.Add(self.TableNumber)
        vSizer.Add(hSizer)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "人数: ")
        hSizer.Add(label)
        self.NumOfPeople = wx.StaticText(self, -1, "")
        hSizer.Add(self.NumOfPeople)
        vSizer.Add(hSizer)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "开始时间: ")
        hSizer.Add(label)
        self.StartTime = wx.StaticText(self, -1, "")
        hSizer.Add(self.StartTime)
        vSizer.Add(hSizer)

        gs = wx.GridSizer(1, 3, 3, 3)
        self.NewOrderBut = wx.Button(parent=self, id=-1,
                                     label=f"下单", size=Config.UI.EatInPage.StatusButSize)
        gs.Add(self.NewOrderBut)
        self.CheckOut = wx.Button(parent=self, id=-1,
                                  label=f"结账", size=Config.UI.EatInPage.StatusButSize)
        gs.Add(self.CheckOut)
        self.CleanTable = wx.Button(parent=self, id=-1,
                                    label=f"清台", size=Config.UI.EatInPage.StatusButSize)
        gs.Add(self.CleanTable)
        vSizer.Add(gs)
        self.SetSizer(vSizer)

    def ShowStatus(self, TableID):
        table = self._DataBase.TableInfo[str(TableID)]
        self.TableNumber.SetLabel(table)
        if table.StartTime is not None:
            self.StartTime.SetLabel(table.StartTime)
        if table.NumOfPeople is not None:
            self.NumOfPeople.SetLabel(table.NumOfPeople)

    def Clear(self):
        self.TableNumber.SetLabel("")
        self.StartTime.SetLabel("")
        self.NumOfPeople.SetLabel("")

