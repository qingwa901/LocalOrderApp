from QtApp.OrderDetailBase import OrderDetailBasePanel
from TableInfoStore import OrderInfo
import datetime
from Config import Config

LocalTimeZone = datetime.datetime.now().astimezone().tzinfo


class OrderDetail(OrderDetailBasePanel):
    def __init__(self, aParent):
        OrderDetailBasePanel.__init__(self, aParent)
        self.OrderInfo = None
        self.TableID = None
        self.BtnAddQty.pressed.connect(self.AddQty)
        self.BtnReduceQty.pressed.connect(self.ReduceQty)
        self.BtnCancel.pressed.connect(self.Cancel)
        self.BtnConfirm.pressed.connect(self.Confirm)
        self.ReloadOrderList = None
        self.BtnAddLabel.pressed.connect(self.AddSpecialNote)

    def SetupOrder(self, Orderinfo: OrderInfo, TableID: int):
        self.OrderInfo = Orderinfo
        self.TableID = TableID
        self.LBTableID.setText(str(TableID))
        self.LBFoodName.setText(Orderinfo.NameCN)
        self.EditPrice.setText(str(round(Orderinfo.UnitPrice, 2)))
        self.EditQty.setText(str(int(Orderinfo.Qty)))
        self.LBStaff.setText(self.DataBase.GetStaffName(Orderinfo.StaffID))
        if Orderinfo.CreateTime is None:
            self.LBCreateTime.setText('')
        else:
            self.LBCreateTime.setText(str(Orderinfo.CreateTime.tz_convert(LocalTimeZone)))
        self.LBExtraRequirement.setText(Orderinfo.Note)
        for TagBtn in self.TagList:
            TagBtn.Clear()
        i = 0
        if Orderinfo.MenuNote != None:
            for TagInfo in Orderinfo.MenuNote[Config.DisplaySetting.MenuTag.TAG]:
                while len(self.TagList) <= i:
                    self.AddNewTag()
                self.TagList[i].SetTag(TagInfo)
                i += 1

    def AddSpecialNote(self):
        TextList = self.LBExtraRequirement.text().split('/')
        Name = self.EditSpecialNote.value()
        if Name != '':
            if Name in TextList:
                TextList.remove(Name)
            else:
                TextList.append(Name)
            self.LBExtraRequirement.setText('/'.join(TextList))

    def AddQty(self):
        self.EditQty.setText(str(int(self.EditQty.text()) + 1))

    def ReduceQty(self):
        self.EditQty.setText(str(max(int(self.EditQty.text()) - 1, 0)))

    def Cancel(self):
        self.setVisible(False)
        self.DataBase.OpenPanel.pop(-1).setVisible(False)
        self.DataBase.OpenPanel[-1].setVisible(True)

    def Confirm(self):
        self.OrderInfo.Qty = int(self.EditQty.text())
        self.OrderInfo.UnitPrice = round(float(self.EditPrice.text()), 2)
        self.OrderInfo.Note = self.LBExtraRequirement.text()
        self.DataBase.EditOrder(self.OrderInfo)
        if self.ReloadOrderList is not None:
            self.ReloadOrderList()
        self.Cancel()
