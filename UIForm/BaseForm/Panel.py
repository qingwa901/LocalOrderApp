# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 22:47:13 2024

@author: qingw
"""

import wx


class Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=-1)

    def AddMany(self, Panels, direction=0):
        if direction == 0:
            vSizer = wx.BoxSizer(wx.VERTICAL)
        elif direction == 1:
            vSizer = wx.BoxSizer(wx.HORIZONTAL)
        for i in Panels:
            vSizer.Add(i, wx.EXPAND)
        self.SetSizer(vSizer)
