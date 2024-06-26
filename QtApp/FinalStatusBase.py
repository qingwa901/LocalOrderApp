# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui/FinalStatus.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets
from QtApp.Base import CFrame, CWidget, CPushButton, CComboBox
from QtApp.Base.EditBox import EditBox, eValueType
from logging import Logger
from QtApp.Base.CAccountCombo import AccountCombo


class FinalStatusBase(CFrame):
    def __init__(self, aParent=None):
        CFrame.__init__(self, aParent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("FinalStatusPanels")
        self.resize(418, 372)
        self.formLayoutWidget = CWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 0, 385, 301))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.LBTableNumber = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBTableNumber.setObjectName("LBTableNumber")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.LBTableNumber)

        self.label0 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label0.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label0)
        self.label0.setText("订单号")
        self.LBOrderID = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBOrderID.setObjectName("LBTableNumber")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.LBOrderID)

        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.LBNumOfPeople = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBNumOfPeople.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LBNumOfPeople.setObjectName("LBNumOfPeople")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.LBNumOfPeople)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.LBStartTime = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBStartTime.setObjectName("LBStartTime")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.LBStartTime)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.LBEndTime = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBEndTime.setObjectName("LBEndTime")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.LBEndTime)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.LBTotalAmount = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBTotalAmount.setObjectName("LBTotalAmount")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.LBTotalAmount)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LBPaidCard = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBPaidCard.setObjectName("LBPaidCard")
        self.horizontalLayout.addWidget(self.LBPaidCard)
        self.BtnCardRemove = CPushButton(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BtnCardRemove.sizePolicy().hasHeightForWidth())
        self.BtnCardRemove.setSizePolicy(sizePolicy)
        self.BtnCardRemove.setObjectName("BtnCardRemove")
        self.horizontalLayout.addWidget(self.BtnCardRemove)
        self.formLayout.setLayout(9, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.LBLablePayment = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBLablePayment.setObjectName("LBLablePayment")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.LBLablePayment)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.EditBoxToPayAmount = EditBox(self.formLayoutWidget, eValueType.Float)
        self.EditBoxToPayAmount.setMinimum(0)
        self.EditBoxToPayAmount.setObjectName("EditBoxToPayAmount")
        self.horizontalLayout_3.addWidget(self.EditBoxToPayAmount)
        self.BtnPayByCard = CPushButton(self.formLayoutWidget)
        self.BtnPayByCard.setObjectName("BtnPayByCard")
        self.horizontalLayout_3.addWidget(self.BtnPayByCard)
        self.BtnPayByCash = CPushButton(self.formLayoutWidget)
        self.BtnPayByCash.setObjectName("BtnPayByCash")
        self.horizontalLayout_3.addWidget(self.BtnPayByCash)
        self.formLayout.setLayout(10, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.BtnPay5Cash = CPushButton(self.formLayoutWidget)
        self.BtnPay5Cash.setObjectName("BtnPay5Cash")
        self.horizontalLayout_4.addWidget(self.BtnPay5Cash)
        self.BtnPay10Cash = CPushButton(self.formLayoutWidget)
        self.BtnPay10Cash.setObjectName("BtnPay10Cash")
        self.horizontalLayout_4.addWidget(self.BtnPay10Cash)
        self.BtnPay20Cash = CPushButton(self.formLayoutWidget)
        self.BtnPay20Cash.setObjectName("BtnPay20Cash")
        self.horizontalLayout_4.addWidget(self.BtnPay20Cash)
        self.formLayout.setLayout(11, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.LBPaiedCash_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBPaiedCash_2.setObjectName("LBPaiedCash_2")
        self.horizontalLayout_5.addWidget(self.LBPaiedCash_2)
        self.BtnCashRemove = CPushButton(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BtnCashRemove.sizePolicy().hasHeightForWidth())
        self.BtnCashRemove.setSizePolicy(sizePolicy)
        self.BtnCashRemove.setObjectName("BtnCashRemove_2")
        self.horizontalLayout_5.addWidget(self.BtnCashRemove)
        self.formLayout.setLayout(8, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label_8 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.label_9 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LBServiceCharge = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBServiceCharge.setObjectName("LBServiceCharge")
        self.horizontalLayout_2.addWidget(self.LBServiceCharge)
        self.BtnAddRemoveServiceCharge = QtWidgets.QPushButton(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BtnAddRemoveServiceCharge.sizePolicy().hasHeightForWidth())
        self.BtnAddRemoveServiceCharge.setSizePolicy(sizePolicy)
        self.BtnAddRemoveServiceCharge.setObjectName("BtnAddRemoveServiceCharge")
        self.horizontalLayout_2.addWidget(self.BtnAddRemoveServiceCharge)
        self.formLayout.setLayout(6, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_10 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.LBDiscountAmount = QtWidgets.QLabel(self.formLayoutWidget)
        self.LBDiscountAmount.setObjectName("LBDiscountAmount")
        self.horizontalLayout_6.addWidget(self.LBDiscountAmount)
        self.BtnRemoveDiscount = CPushButton(self.formLayoutWidget)
        self.BtnRemoveDiscount.setObjectName("RemoveDiscount")
        self.horizontalLayout_6.addWidget(self.BtnRemoveDiscount)
        self.ButDiscountA = CPushButton(self.formLayoutWidget)
        self.ButDiscountA.setObjectName("pushButton_3")
        self.horizontalLayout_6.addWidget(self.ButDiscountA)
        self.ButDiscountB = CPushButton(self.formLayoutWidget)
        self.ButDiscountB.setObjectName("pushButton")
        self.horizontalLayout_6.addWidget(self.ButDiscountB)
        self.formLayout.setLayout(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.formLayout.setLayout(12, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_7)
        self.gridLayoutWidget = CWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 320, 295, 31))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.BtnReOpen = CPushButton(self.gridLayoutWidget)
        self.BtnReOpen.setObjectName("BtnReOpen")
        self.gridLayout.addWidget(self.BtnReOpen, 0, 0, 1, 1)
        self.BtnPrintReceipt = CPushButton(self.gridLayoutWidget)
        self.BtnPrintReceipt.setObjectName("BtnPrintReceipt")
        self.gridLayout.addWidget(self.BtnPrintReceipt, 0, 1, 1, 1)
        self.BtnCleanTable = CPushButton(self.gridLayoutWidget)
        self.BtnCleanTable.setObjectName("BtnCleanTable")
        self.gridLayout.addWidget(self.BtnCleanTable, 0, 2, 1, 1)
        self.BtnDeleteOrder = CPushButton(self.gridLayoutWidget)
        self.BtnDeleteOrder.setObjectName("BtnDeleteOrder")
        self.gridLayout.addWidget(self.BtnDeleteOrder, 0, 3, 1, 1)

        self.hLayhoutWidge = CWidget(self)
        self.hLayhoutWidge.setGeometry(QtCore.QRect(10, 360, 295, 31))
        self.hLayhout = QtWidgets.QHBoxLayout(self.hLayhoutWidge)
        self.hLayhout.setContentsMargins(0, 0, 0, 0)
        self.hLayhout.setObjectName('hLayout')
        self.AccountLabel = QtWidgets.QLabel(self.hLayhoutWidge)
        self.hLayhout.addWidget(self.AccountLabel)
        self.AccountCombo = AccountCombo(self.hLayhoutWidge)
        self.hLayhout.addWidget(self.AccountCombo)
        self.BtnAddToAccount = CPushButton(self.hLayhoutWidge)
        self.BtnAddToAccount.setVisible(False)
        self.hLayhout.addWidget(self.BtnAddToAccount)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "FinalStatusPanel"))
        self.label.setText(_translate("Form", "桌号"))
        self.LBTableNumber.setText(_translate("Form", "None"))
        self.label_2.setText(_translate("Form", "人数"))
        self.LBNumOfPeople.setText(_translate("Form", "None"))
        self.label_3.setText(_translate("Form", "开始时间"))
        self.LBStartTime.setText(_translate("Form", "None"))
        self.label_4.setText(_translate("Form", "结账时间"))
        self.LBEndTime.setText(_translate("Form", "None"))
        self.label_5.setText(_translate("Form", "总金额"))
        self.LBTotalAmount.setText(_translate("Form", "None"))
        self.label_6.setText(_translate("Form", "现金金额"))
        self.label_7.setText(_translate("Form", "刷卡金额"))
        self.LBPaidCard.setText(_translate("Form", "None"))
        self.BtnCardRemove.setText(_translate("Form", "X"))
        self.LBLablePayment.setText(_translate("Form", "未付"))
        self.BtnPayByCard.setText(_translate("Form", "刷卡"))
        self.BtnPayByCash.setText(_translate("Form", "现金"))
        self.BtnPay5Cash.setText(_translate("Form", "£5"))
        self.BtnPay10Cash.setText(_translate("Form", "£10"))
        self.BtnPay20Cash.setText(_translate("Form", "£20"))
        self.LBPaiedCash_2.setText(_translate("Form", "None"))
        self.BtnCashRemove.setText(_translate("Form", "X"))
        self.label_8.setText(_translate("Form", "现金"))
        self.label_9.setText(_translate("Form", "服务费"))
        self.LBServiceCharge.setText(_translate("Form", "None"))
        self.BtnAddRemoveServiceCharge.setText(_translate("Form", "去除/添加服务费"))
        self.label_10.setText(_translate("Form", "折扣"))
        self.LBDiscountAmount.setText(_translate("Form", "None"))
        self.BtnRemoveDiscount.setText(_translate("Form", "X"))
        self.BtnReOpen.setText(_translate("Form", "重开台"))
        self.BtnPrintReceipt.setText(_translate("Form", "打单"))
        self.BtnCleanTable.setText(_translate("Form", "清台"))
        self.BtnDeleteOrder.setText(_translate("Form", "删单"))
        self.AccountLabel.setText(_translate("From", "挂单账户："))
        self.BtnAddToAccount.setText(_translate("Form", "添加至账户"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = FinalStatusBase()
    ui.show()
    sys.exit(app.exec_())
