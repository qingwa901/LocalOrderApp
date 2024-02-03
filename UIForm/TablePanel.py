# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 21:47:54 2024

@author: qingw
"""

import wx
from .TableBut import TableBut


class TablePanel(wx.Panel):
    """"""

    def __init__(self, parent, TableList):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.TableList = {}
        self.SetBackgroundColour('#ededed')
        #vbox = wx.BoxSizer(wx.VERTICAL)
        ColNum = max([len(x) for x in TableList])
        RowNum = len(TableList)
        gs = wx.GridSizer(RowNum, ColNum, 3, 3)
        for row in TableList:
            for table in row:
                print(table)
                if table is None:
                    gs.Add((100, -1), wx.ID_ANY, wx.EXPAND)
                else:
                    table_but = TableBut(self, table)
                    self.TableList[table] = table_but
                    gs.Add(table_but, wx.ID_ANY, wx.EXPAND)
        self.SetSizer(gs)
        #vbox.Add(gs, wx.ID_ANY, wx.EXPAND)
        # self.SetSizer(vbox)
