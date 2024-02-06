import wx
from DataBase import DataBase
from Config import Config
from logging import Logger


class InitialTablePanel(wx.Panel):
    """"""

    def __init__(self, parent, logger: Logger, DataBase: DataBase):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self._DataBase = DataBase
        self._Logger = logger

        vSizer = wx.BoxSizer(wx.VERTICAL)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "桌号: ")
        hSizer.Add(label)
        self.TableNumber = wx.StaticText(self, -1, "")
        hSizer.Add(self.TableNumber)
        vSizer.Add(hSizer)

