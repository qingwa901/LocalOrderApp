import wx
from DataBase import DataBase
from Config import Config
from logging import Logger


class LoginPage(wx.Panel):
    """"""

    def __init__(self, parent, logger: Logger, DataBase: DataBase):
        self.parent = parent
        self._Logger = logger
        self._DataBase = DataBase
        wx.Panel.__init__(self, parent)

        vSizer = wx.BoxSizer(wx.VERTICAL)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "用户名: ")
        hSizer.Add(label)
        self.UserName = wx.TextCtrl(self, -1, size=(100, -1))
        hSizer.Add(self.UserName)
        vSizer.Add(hSizer, wx.EXPAND)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "密码: ")
        hSizer.Add(label)
        self.PassWord = wx.TextCtrl(self, -1, "", size=(175, -1), style=wx.TE_PASSWORD)
        hSizer.Add(self.PassWord)
        vSizer.Add(hSizer, wx.EXPAND)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.LoginBut = wx.Button(parent=self, id=-1,
                                  label=f"登入", size=(100, -1))

        hSizer.Add(self.LoginBut, wx.EXPAND)
        self.Back = wx.Button(parent=self, id=-1,
                              label=f"返回", size=(100, -1))

        hSizer.Add(self.Back, wx.EXPAND)
        vSizer.Add(hSizer)
        self.SetSizer(vSizer)
        self.Bind(wx.EVT_BUTTON, self.close, self.LoginBut)
        self.Bind(wx.EVT_BUTTON, self.close, self.Back)
        # self.Hide()
        self.LoginAction = None
        self.Centre()
        self.old_style = self.GetWindowStyle()
        self.SetWindowStyle(self.old_style | wx.STAY_ON_TOP)
        self.Hide()

    def Display(self):
        self.UserName.Clear()
        self.PassWord.Clear()
        self.SetSize((300, 200))
        self.Centre()
        self.Show(True)
        self.SetSize((300, 200))
        self.SetWindowStyle(wx.STAY_ON_TOP)

    def close(self, e):
        self.Hide()
        self.LoginAction()

    def Login(self, e):
        pass #Todo