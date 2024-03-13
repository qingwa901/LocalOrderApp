from PySide6 import QtCore, QtWidgets
from Config import Config
from QtApp.Base import CPushButton


class CTagBtn(CPushButton):
    def __init__(self, aParent, ID):
        self.ID = ID
        CPushButton.__init__(self, aParent)
        self.target = None
        self.NoteWeidget = None
        self.PriceWeidget = None
        self.setupUi()

    def setupUi(self):
        self.setObjectName(f"Tag{self.ID}")
        _translate = QtCore.QCoreApplication.translate
        self.setText(_translate("Form", 'None'))
        self.pressed.connect(self.PressEvent)

    def PressEvent(self):
        if self.NoteWeidget is None:
            return
        if self.TagInfo is None:
            return
        if self.PriceWeidget is None:
            return
        TextList = self.NoteWeidget.text().split('/')
        Price = round(float(self.PriceWeidget.text()), 2)
        Name = self.TagInfo[Config.DisplaySetting.MenuTag.NAME]
        PriceAdd = self.TagInfo[Config.DisplaySetting.MenuTag.PRICE_ADD]
        if Name in TextList:
            TextList.remove(Name)
            Price -= PriceAdd
        else:
            TextList.append(Name)
            Price += PriceAdd
        self.NoteWeidget.setText('/'.join(TextList))
        self.PriceWeidget.setText(str(round(Price, 2)))

    def Clear(self):
        self.setVisible(False)
        self.TagInfo = None
        _translate = QtCore.QCoreApplication.translate
        self.setText(_translate("Form", 'None'))

    def SetTag(self, TagInfo):
        self.TagInfo = TagInfo
        _translate = QtCore.QCoreApplication.translate
        self.setText(_translate("Form", TagInfo[Config.DisplaySetting.MenuTag.NAME]))
        self.setVisible(True)
