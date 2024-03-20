from PySide6 import QtCore, QtWidgets
from QtApp.Base import CPushButton


class KeyBoardBtn(CPushButton):
    def __init__(self, aParent):
        CPushButton.__init__(self, aParent)
        self.target = None

    def setupUi(self, Number):
        self.Number = Number
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)

        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        # sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setObjectName(f"KeyBoardBtn{Number}")
        self.setStyleSheet('background-color: white;')
        _translate = QtCore.QCoreApplication.translate
        text = str(Number)
        if text == 'Delete':
            text = "撤回"
        elif text == 'Dot':
            text = '.'
        elif text == 'Enter':
            text = '回车'
        self.setText(_translate("Form", text))
        self.pressed.connect(self.PressEvent)

    def setTarget(self, target):
        self.target = target

    def removeTarget(self):
        self.target = None

    def PressEvent(self):
        if self.target is None:
            return
        text = str(self.Number)
        value = str(self.target.text())
        if text == 'Delete':
            if len(value) > 1:
                self.target.setText(value[:-1])
            else:
                self.target.setText('0')
        elif text == 'Dot':
            if '.' not in value:
                self.target.setText(value + '.')
        # elif text == 'Enter':
        #     text = '回车'
        elif text == '0':
            if value != '0':
                self.target.setText(value + text)
        else:
            if value != '0':
                self.target.setText(value + text)
            else:
                self.target.setText(text)
