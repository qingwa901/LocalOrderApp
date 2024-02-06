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
from Config import Config
from logging import Logger
from .LoginPage import LoginPage


class EatInTable(wx.Frame):
    def __init__(self, parent, logger: Logger, DataBase: DataBase):
        self._logger = logger
        self._config = Config()
        self._DataBase = DataBase
        size = self._DataBase.Setting.GetValue('UI.EatInTable.Size')
        if size is None:
            size = (500,300)
        wx.Frame.__init__(self, parent, -1, title='ZhangJi Order System',
                          size=size)
        self.TableOrder = self._DataBase.Setting.GetValue(field=self._config.DataBase.StoreList.TABLE_ORDER)
        self.TableList = {}
        self.Centre()
        self.InitUI()

        self.Bind(wx.EVT_SIZE, self.OnSize)
        # self.Bind(wx.EVT_IDLE, self.OnIdle)

    def InitUI(self):
        self._logger.info('Initial EatInTable')
        self.CreatToolbar()

        self.LoginPage = LoginPage(self, self._logger, self._DataBase)

        self.LoginPage.LoginAction = self.AfterLogin
        self.MainPanel = SpWindow(self, 0)
        self.SettingPanel = SettingPanel(self, self.Size, self._logger, self._DataBase)
        TotalSizer = wx.BoxSizer(wx.VERTICAL)
        TotalSizer.Add(self.MainPanel, 1, wx.EXPAND)
        TotalSizer.Add(self.SettingPanel, 1, wx.EXPAND)
        self.SetSizer(TotalSizer)

        self.TablePanel = TablePanel(
            self.MainPanel.GetWindow1(), self._logger, self._DataBase)
        self.MainPanel.GetWindow1().AddMany([self.TablePanel])
        splitter2 = SpWindow(self.MainPanel.GetWindow2(), 1)
        self.MainPanel.GetWindow2().AddMany([splitter2])
        self.StatusPanel = StatusPanel(splitter2.GetWindow1(), self._logger, self._DataBase)
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
        self.toolbar = self.CreateToolBar()
        Size = self._config.UI.EatInPage.ToolBarSize

        bit = wx.Bitmap('img/quit.png')
        wx.Bitmap.Rescale(bit, (Size, Size))
        quitbut = self.toolbar.AddTool(wx.ID_ANY, 'Quit', bit)

        bit = wx.Bitmap('img/setting.png')
        wx.Bitmap.Rescale(bit, (Size, Size))
        setbut = self.toolbar.AddTool(wx.ID_SETUP, 'Setting', bit)

        bit = wx.Bitmap('img/Table.png')
        wx.Bitmap.Rescale(bit, (Size, Size))
        Tablebut = self.toolbar.AddTool(wx.ID_FILE, 'Table', bit)

        bit = wx.Bitmap('img/Login.png')
        wx.Bitmap.Rescale(bit, (Size, Size))
        LoginBut = self.toolbar.AddTool(-1, 'Login', bit)

        self.toolbar.Realize()
        self.toolbar.SetToolBitmapSize((Size, Size))
        self.Bind(wx.EVT_TOOL, self.OnQuit, quitbut)
        self.Bind(wx.EVT_TOOL, self.OpenSetting, setbut)
        self.Bind(wx.EVT_TOOL, self.OpenTable, Tablebut)
        self.Bind(wx.EVT_TOOL, self.Login, LoginBut)
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
        self._DataBase.Setting.SetValue('UI.EatInTable.Size', (self.Size[0], self.Size[1]))

    def Login(self, e):
        self.LoginPage.Display()
        self.MainPanel.Disable()
        self.toolbar.Disable()
        self.SettingPanel.Disable()

    def AfterLogin(self):
        self.MainPanel.Enable()
        self.SettingPanel.Enable()
        self.toolbar.Enable()