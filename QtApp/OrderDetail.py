from QtApp.OrderDetailBase import OrderDetailBasePanel
from TableInfoStore import OrderInfo
import datetime

LocalTimeZone = datetime.datetime.now().astimezone().tzinfo


class OrderDetail(OrderDetailBasePanel):
    def __init__(self, parent, logger):
        self.logger = logger
        OrderDetailBasePanel.__init__(self, parent, logger)
        self.OrderInfo = None
        self.TableID = None
        self.BtnAddQty.pressed.connect(self.AddQty)
        self.BtnReduceQty.pressed.connect(self.ReduceQty)
        self.BtnCancel.pressed.connect(self.Cancel)
        self.BtnConfirm.pressed.connect(self.Confirm)

    def SetupOrder(self, Orderinfo: OrderInfo, TableID: int):
        self.OrderInfo = OrderInfo
        self.TableID = TableID
        self.LBTableID.setText(str(TableID))
        self.LBFoodName.setText(Orderinfo.NameCN)
        self.LBUnitPrice.setText(str(round(Orderinfo.UnitPrice, 2)))
        self.EditQty.setText(str(int(Orderinfo.Qty)))
        self.LBCashier.setText(str(int(Orderinfo.StaffID)))
        self.LBCreateTime.setText(str(Orderinfo.CreateTime.tz_convert(LocalTimeZone)))
        self.LBExtraRequirement.setText(Orderinfo.Note)
        for TagBtn in self.TagList:
            TagBtn.Clear()
        i = 0
        for TagInfo in OrderInfo.MenuNote:
            while len(self.TagList) <= i:
                self.AddNewTag()
            self.TagList[i].SetTag(TagInfo)
            i += 1

    def AddQty(self):
        self.EditQty.setText(str(int(self.EditQty.text()) + 1))

    def ReduceQty(self):
        self.EditQty.setText(str(max(int(self.EditQty.text()) - 1, 0)))

    def Cancel(self):
        self.setVisible(False)

    def Confirm(self):
        self.OrderInfo.Qty = int(self.EditQty.text())
        self.OrderInfo.UnitPrice = round(self.OrderInfo.UnitPrice, 2)
        self.Cancel()
