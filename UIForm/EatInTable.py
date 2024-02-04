# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 19:04:09 2024

@author: qingw
"""

import wx
from .TablePanel import TablePanel
from .SettingPanel import SettingPanel
from .BaseForm.SpWindow import SpWindow
from .MenuPanel import MenuPanel
from .StatusPanel import StatusPanel
from .ExistOrderPanel import ExistOrderPanel
from .NewOrderPanel import NewOrderPanel
from DataBase import DataBase
from ConfigSetting import ConfigSetting
from Config import Config
from logging import Logger


class EatInTable(wx.Frame):
    def __init__(self, parent, logger: Logger, DataBase: DataBase):
        wx.Frame.__init__(self, parent, -1, title='ZhangJi Order System',
                          size=(500, 400))
        self._logger = logger
        self._config = Config()
        self._DataBase = DataBase
        self.TableOrder = self._DataBase.Setting.GetValue(field=self._config.DataBase.StoreList.TABLE_ORDER)
        self.TableList = {}
        self.Centre()
        self.InitUI()

        self.Bind(wx.EVT_SIZE, self.OnSize)
        # self.Bind(wx.EVT_IDLE, self.OnIdle)

    def InitUI(self):
        self._logger.info('Initial EatInTable')
        self.CreatToolbar()
        self.MainPanel = SpWindow(self, 0)
        self.SettingPanel = SettingPanel(self, self.Size, self._logger, self._DataBase)
        TotalSizer = wx.BoxSizer(wx.VERTICAL)
        TotalSizer.Add(self.MainPanel, 1, wx.EXPAND)
        TotalSizer.Add(self.SettingPanel, 1, wx.EXPAND)
        self.SetSizer(TotalSizer)

        self.TablePanel = TablePanel(
            self.MainPanel.GetWindow1(), self.TableOrder)
        self.MainPanel.GetWindow1().AddMany([self.TablePanel])
        splitter2 = SpWindow(self.MainPanel.GetWindow2(), 1)
        self.MainPanel.GetWindow2().AddMany([splitter2])
        self.StatusPanel = StatusPanel(splitter2.GetWindow1())
        self.MenuPanel = MenuPanel(splitter2.GetWindow1())
        splitter2.GetWindow1().AddMany((self.StatusPanel, self.MenuPanel))

        self.ExistOrderPanel = ExistOrderPanel(splitter2.GetWindow2())
        self.NewOrderPanel = NewOrderPanel(splitter2.GetWindow2())
        splitter2.GetWindow2().AddMany((self.ExistOrderPanel,
                                        self.NewOrderPanel))
        self.MenuPanel.Hide()
        self.NewOrderPanel.Hide()
        self._logger.info('Initial EatInTable finished')

    def CreatToolbar(self):
        self._logger.info('Building toolbar')
        toolbar = self.CreateToolBar()
        bit = wx.Bitmap('img/quit.png')
        Size = self._config.UI.EatInPage.ToolBarSize
        wx.Bitmap.Rescale(bit, (Size, Size))
        quitbut = toolbar.AddTool(wx.ID_ANY, 'Quit', bit)
        bit = wx.Bitmap('img/setting.png')
        wx.Bitmap.Rescale(bit, (Size, Size))
        setbut = toolbar.AddTool(wx.ID_SETUP, 'Setting', bit)
        bit = wx.Bitmap('img/Table.png')
        wx.Bitmap.Rescale(bit, (Size, Size))
        Tablebut = toolbar.AddTool(wx.ID_FILE, 'Table', bit)
        toolbar.Realize()
        toolbar.SetToolBitmapSize((Size, Size))
        self.Bind(wx.EVT_TOOL, self.OnQuit, quitbut)
        self.Bind(wx.EVT_TOOL, self.OpenSetting, setbut)
        self.Bind(wx.EVT_TOOL, self.OpenTable, Tablebut)
        self._logger.info('Building toolbar finished')

    def OpenSetting(self, e):
        self.MainPanel.Hide()
        self.SettingPanel.Show()

    def OpenTable(self, e):
        self.MainPanel.Show()
        self.SettingPanel.Hide()

    def OnQuit(self, e):
        self._DataBase.open = False
        self._DataBase.Setting.open = False
        self.Close()

    def OnSize(self, e):
        self.MainPanel.SetSize((self.Size[0], self.Size[1] - 90))
        self.SettingPanel.SetSize((self.Size[0], self.Size[1] - 90))
