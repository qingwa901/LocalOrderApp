# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 23:31:03 2024

@author: qingw
"""

import wx


class ComboBox(wx.ComboBox):
    def __init__(self, parent):
        wx.ComboBox.__init__(parent, -1)

    def widgetMaker(self, objects: dict):
        """"""
        for key, value in objects:
            self.Append(key, value)
