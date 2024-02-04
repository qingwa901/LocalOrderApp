# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 22:24:31 2024

@author: qingw
"""

import wx
from .Panel import Panel


class SpWindow(wx.SplitterWindow):
    def __init__(self, parent, direction=0):
        wx.SplitterWindow.__init__(self, parent=parent, id=-1)
        self.direction = direction
        self.SetMinimumPaneSize(100)
        panel1 = Panel(self)
        panel2 = Panel(self)
        if direction == 0:
            self.SplitVertically(panel1, panel2)
        elif direction == 1:
            self.SplitHorizontally(panel1, panel2)
        self.ratio = 0.5
        self.SetSashPosition(int(self.Size[self.direction]*self.ratio))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.OnSplitChange)

    def OnSize(self, e):
        self.SetSashPosition(int(self.Size[self.direction]*self.ratio))

    def OnSplitChange(self, e):
        self.ratio = self.SashPosition / self.Size[self.direction]
