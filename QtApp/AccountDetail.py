# Form implementation generated from reading ui file 'Ui/AccountDetail.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets
from QtApp.Base import CFrame, CWidget, CPushButton
from QtApp.Base.EditBox import eValueType, EditBox


class AccountDetailPanel(CFrame):
    def __init__(self, aParent=None):
        CFrame.__init__(self, aParent)
        self.BlockPanel = aParent.BlockPanel
        self.setupUi()
        self.AccountID = None
        self.RefreshEvent = None
        self.ButtonConfirm.pressed.connect(self.SaveAndClose)
        self.pushButtonReturn.pressed.connect(self.BlockPanel.Close)
        self.SetBackgoundColor('Yellow')

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(400, 300)
        self.formLayoutWidget = CWidget(aParent=self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(19, 19, 371, 121))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.LabelAccountID = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.LabelAccountID.setObjectName("LabelAccountID")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.LabelAccountID)
        self.EditBoxName = EditBox(self.formLayoutWidget, eValueType.String)
        self.EditBoxName.setObjectName("EditBoxName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.EditBoxName)
        self.label_4 = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButtonDelete = QtWidgets.QRadioButton(parent=self.formLayoutWidget)
        self.radioButtonDelete.setObjectName("radioButtonDelete")
        self.verticalLayout.addWidget(self.radioButtonDelete)
        self.radioButtonKeep = QtWidgets.QRadioButton(parent=self.formLayoutWidget)
        self.radioButtonKeep.setChecked(True)
        self.radioButtonKeep.setObjectName("radioButtonKeep")
        self.verticalLayout.addWidget(self.radioButtonKeep)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.verticalLayout)

        self.label_5 = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)

        self.EditBoxTotalAmount = EditBox(self.formLayoutWidget, eValueType.Float)
        self.EditBoxTotalAmount.setObjectName("EditBoxTotalAmount")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.EditBoxTotalAmount)
        self.ButtonConfirm = CPushButton(self)
        self.ButtonConfirm.setGeometry(QtCore.QRect(30, 220, 75, 24))
        self.ButtonConfirm.setObjectName("ButtonConfirm")
        self.pushButtonDelete = CPushButton(self)
        self.pushButtonDelete.setGeometry(QtCore.QRect(160, 220, 75, 24))
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.pushButtonDelete.setVisible(False)
        self.pushButtonReturn = CPushButton(self)
        self.pushButtonReturn.setGeometry(QtCore.QRect(290, 220, 75, 24))
        self.pushButtonReturn.setObjectName("pushButtonReturn")
        self.radioButtonKeep.toggled.connect(self.KeepRadioEvent)
        self.radioButtonDelete.toggled.connect(self.DeleteRadioEvent)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "账户编号："))
        self.label_2.setText(_translate("Form", "账户名字："))
        self.LabelAccountID.setText(_translate("Form", ""))
        self.label_4.setText(_translate("Form", "是否在日终自动删除"))
        self.radioButtonDelete.setText(_translate("Form", "删除"))
        self.radioButtonKeep.setText(_translate("Form", "不删除"))
        self.ButtonConfirm.setText(_translate("Form", "确认"))
        self.pushButtonDelete.setText(_translate("Form", "删除"))
        self.pushButtonReturn.setText(_translate("Form", "返回"))
        self.label_5.setText(_translate("Form", "今日之前的总金额"))

    def Load(self, Account):
        self.Logger.info(f"Load Account {Account}")
        if Account == dict():
            return  # Edit without any selected row
        try:
            OrderAccountList = self.DataBase.config.OrderAccountList
            self.Clear()
            if Account is not None:
                self.LabelAccountID.setText(str(Account[OrderAccountList.ID]))
                self.AccountID = Account[OrderAccountList.ID]
                self.EditBoxName.setText(Account[OrderAccountList.ACCOUNT_NAME])
                if Account[OrderAccountList.AUTO_DELETE]:
                    self.radioButtonDelete.setChecked(True)
                    self.radioButtonKeep.setChecked(False)
                else:
                    self.radioButtonDelete.setChecked(False)
                    self.radioButtonKeep.setChecked(True)
                self.EditBoxTotalAmount.setText(str(Account[OrderAccountList.TOTAL_AMOUNT]))
        except Exception as e:
            self.Logger.error(f'Error during load account', exc_info=e)

        self.Open()

    def Open(self):
        try:
            self.setVisible(True)
            self.resize(600, 300)
            self.move(self.parent().width() // 2 - 300, self.parent().height() // 2 - 150)
            self.raise_()
            self.BlockPanel.Show(self, self.Close)
        except Exception as e:
            self.Logger.error(f'Error during show Account window', exc_info=e)

    def KeepRadioEvent(self):
        self.radioButtonDelete.setChecked(not self.radioButtonKeep.isChecked())

    def DeleteRadioEvent(self):
        self.radioButtonKeep.setChecked(not self.radioButtonDelete.isChecked())

    def Clear(self):
        self.LabelAccountID.setText('')
        self.radioButtonKeep.setChecked(True)
        self.radioButtonDelete.setChecked(False)
        self.EditBoxName.setText('')
        self.AccountID = None

    def SaveAndClose(self):
        self.DataBase.SaveNewAccount(
            AccountID=(None if self.LabelAccountID.text() == '' else int(self.LabelAccountID.text())),
            AccountName=self.EditBoxName.value(),
            AutoDelete=self.radioButtonDelete.isChecked(),
            TotalAmount=self.EditBoxTotalAmount.value()
        )
        self.BlockPanel.Close()

    def Close(self):
        self.setVisible(False)
        self.Clear()
        if self.RefreshEvent is not None:
            self.RefreshEvent()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = AccountDetailPanel()
    ui.setupUi()
    ui.show()
    sys.exit(app.exec())
