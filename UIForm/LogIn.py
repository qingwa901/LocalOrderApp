# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 18:56:23 2024

@author: qingw
"""

import wx

class LogIn(wx.Frame):
    def __init__(self, parent, title):
        super(LogIn, self).__init__(parent, title=title,
          size=(300, 200))
        self.InitUI()
    
    def InitUI(self):

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)

        self.SetSize((300, 200))
        self.SetTitle('Simple menu')
        self.Centre()
    
    def OnQuit(self, e):
        self.Close()
