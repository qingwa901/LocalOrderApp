# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 21:50:06 2024

@author: qingw
"""

import wx


class TableBut(wx.Button):
    def __init__(self, parent, TableNum):
        wx.Button.__init__(self, parent=parent, id=-1,
                           label=f"Table {TableNum}", size=(100, 100))

        # self.SetSize((50,50))
        # self.bind(wx.EVT_BUTTON, )
