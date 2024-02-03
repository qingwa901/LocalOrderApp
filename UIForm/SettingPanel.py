# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 22:07:36 2024

@author: qingw
"""

import wx


class SettingPanel(wx.Panel):
    """"""

    def __init__(self, parent, size):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent, size=size)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "Printer Setting:")
        vSizer.Add(label)
        self.SetSizer(vSizer)
        self.Hide()
