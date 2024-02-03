# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 19:04:09 2024

@author: qingw
"""

import wx
from .TablePanel import TablePanel
from .SettingPanel import SettingPanel
from .BaseForm.SpWindow import SpWindow
from .StatusPanel import StatusPanel
from .ExistOrderPanel import ExistOrderPanel
from .NewOrderPanel import NewOrderPanel


class EatInTable(wx.Frame):
    def __init__(self, parent, logger, config, SQLControl=None):
        wx.Frame.__init__(self, parent, -1, title='ZhangJi Order System',
                          size=(500, 400))
        self.logger = logger
        self._config = config
        self.SQLControl = SQLControl
        self.TableListNum = TableList
        self.TableList = {}
        self.Centre()
        self.InitUI()

        self.Bind(wx.EVT_SIZE, self.OnSize)
        # self.Bind(wx.EVT_IDLE, self.OnIdle)

    def InitUI(self):
        toolbar = self.CreateToolBar()
        bit = wx.Bitmap('img/quit.png')
        wx.Bitmap.Rescale(bit, (35, 35))
        quitbut = toolbar.AddTool(wx.ID_ANY, 'Quit', bit)
        bit = wx.Bitmap('img/setting.png')
        wx.Bitmap.Rescale(bit, (35, 35))
        setbut = toolbar.AddTool(wx.ID_SETUP, 'Setting', bit)
        bit = wx.Bitmap('img/Table.png')
        wx.Bitmap.Rescale(bit, (35, 35))
        Tablebut = toolbar.AddTool(wx.ID_FILE, 'Table', bit)
        toolbar.Realize()
        toolbar.SetToolBitmapSize((35, 35))
        self.Bind(wx.EVT_TOOL, self.OnQuit, quitbut)
        self.Bind(wx.EVT_TOOL, self.OpenSetting, setbut)
        self.Bind(wx.EVT_TOOL, self.OpenTable, Tablebut)

        self.MainPanel = SpWindow(self, 0)
        self.SettingPanel = SettingPanel(self, self.Size)
        TotalSizer = wx.BoxSizer(wx.VERTICAL)
        TotalSizer.Add(self.MainPanel, 1, wx.EXPAND)
        TotalSizer.Add(self.SettingPanel, 1, wx.EXPAND)
        self.SetSizer(TotalSizer)

        self.TablePanel = TablePanel(
            self.MainPanel.GetWindow1(), self.TableListNum)
        self.MainPanel.GetWindow1().AddMany([self.TablePanel])
        splitter2 = SpWindow(self.MainPanel.GetWindow2(), 1)
        self.MainPanel.GetWindow2().AddMany([splitter2])
        self.StatusPanel = StatusPanel(splitter2.GetWindow1())
        self.SetMenuPanel(splitter2.GetWindow1())
        splitter2.GetWindow1().AddMany((self.StatusPanel, self.MenuPanel))

        self.ExistOrderPanel = ExistOrderPanel(splitter2.GetWindow2())
        self.NewOrderPanel = NewOrderPanel(splitter2.GetWindow2())
        splitter2.GetWindow2().AddMany((self.ExistOrderPanel,
                                        self.NewOrderPanel))

        self.MenuPanel.Hide()
        self.NewOrderPanel.Hide()

    def OpenSetting(self, e):
        self.MainPanel.Hide()
        self.SettingPanel.Show()

    def OpenTable(self, e):
        self.MainPanel.Show()
        self.SettingPanel.Hide()

    def OnQuit(self, e):
        self.Close()

    def OnSize(self, e):
        self.MainPanel.SetSize((self.Size[0], self.Size[1] - 90))
        self.SettingPanel.SetSize((self.Size[0], self.Size[1] - 90))
