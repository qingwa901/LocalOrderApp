# Form implementation generated from reading ui file 'Ui/OrderDetail.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets
from QtApp.Base.FlowLayout import FlowLayout
from QtApp.Base.EditBox import EditBox, eValueType
from Logger import CreateLogger
from QtApp.Base.TagBut import CTagBtn
from QtApp.Base import CFrame, CWidget, CPushButton, CSplitter

class OrderDetailBasePanel(CFrame):
    def __init__(self, aParant):
        CFrame.__init__(self, aParant)
        self.TagList = []
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Form")
        self.setAutoFillBackground(True)
        self.setStyleSheet('background-color: lightgrey;')
        vlayout = QtWidgets.QVBoxLayout(self)
        self.splitter = CSplitter(aParent=self)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        vlayout.addWidget(self.splitter)
        self.setLayout(vlayout)
        self.frame = CFrame(aParent=self.splitter)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        vlayout = QtWidgets.QHBoxLayout(self.frame)

        self.formLayoutWidget = CWidget(aParent=self.frame)
        vlayout.addWidget(self.formLayoutWidget)
        vlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.frame.setLayout(vlayout)
        self.formLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 311, 262))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFormAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.LBTableID = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.LBTableID.setObjectName("LBTableID")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.LBTableID)
        self.label_2 = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.LBFoodName = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.LBFoodName.setObjectName("LBFoodName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.LBFoodName)
        self.label_3 = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.EditQty = EditBox(aParent=self.formLayoutWidget, aValueType=eValueType.Int)
        self.EditQty.setObjectName("EditQty")
        self.EditQty.setMinimum(0)
        self.horizontalLayout_4.addWidget(self.EditQty)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.BtnAddQty = CPushButton(aParent=self.formLayoutWidget)
        self.BtnAddQty.setObjectName("pushButton_6")
        self.verticalLayout.addWidget(self.BtnAddQty)
        self.BtnReduceQty = CPushButton(aParent=self.formLayoutWidget)
        self.BtnReduceQty.setObjectName("pushButton_7")
        self.verticalLayout.addWidget(self.BtnReduceQty)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_4)
        self.label_5 = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        # self.LBUnitPrice = QtWidgets.QLabel(parent=self.formLayoutWidget)
        # self.LBUnitPrice.setObjectName("LBUnitPrice")
        # self.horizontalLayout_3.addWidget(self.LBUnitPrice)
        self.EditPrice = EditBox(aParent=self.formLayoutWidget, aValueType=eValueType.Int)
        self.EditPrice.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.EditPrice)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_3)
        self.label_4 = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LBExtraRequirement = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.LBExtraRequirement.setObjectName("LBExtraRequirement")
        self.LBExtraRequirement.setWordWrap(True)
        self.horizontalLayout_2.addWidget(self.LBExtraRequirement)
        # self.pushButton_5 = QtWidgets.QPushButton(parent=self.formLayoutWidget)
        # self.pushButton_5.setObjectName("pushButton_5")
        # self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)
        self.LBCahierTag = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.LBCahierTag.setObjectName("LBCahierTag")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.LBCahierTag)
        self.LBStaff = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.LBStaff.setObjectName("LBCashier")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.LBStaff)

        self.LBCreateTimeTag = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.LBCreateTimeTag.setObjectName("LBCreateTimeTag")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.LBCreateTimeTag)
        self.LBCreateTime = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.LBCreateTime.setObjectName("LBCreateTime")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.LBCreateTime)

        self.BtnConfirm = CPushButton(aParent=self.formLayoutWidget)
        self.BtnConfirm.setObjectName("pushButton_9")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.BtnConfirm)
        self.BtnCancel = CPushButton(aParent=self.formLayoutWidget)
        self.BtnCancel.setObjectName("BtnCancel")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.ItemRole.FieldRole, self.BtnCancel)
        self.frame_2 = CFrame(aParent=self.splitter)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.EditSpecialNote = EditBox(aParent=self.frame_2, aValueType=eValueType.String)
        self.EditSpecialNote.setObjectName("EditBoxSpecialNote")
        self.horizontalLayout_6.addWidget(self.EditSpecialNote)
        self.BtnAddLabel = CPushButton(aParent=self.frame_2)
        self.BtnAddLabel.setObjectName("BtnAddLabel")
        self.horizontalLayout_6.addWidget(self.BtnAddLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.widget1 = CWidget(aParent=self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget1.sizePolicy().hasHeightForWidth())
        self.widget1.setSizePolicy(sizePolicy)
        self.widget1.setObjectName("widget1")
        self.FlowLayout = FlowLayout(self.widget1)

        self.verticalLayout_2.addWidget(self.widget1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "桌号"))
        self.LBTableID.setText(_translate("Form", "TextLabel"))
        self.label_2.setText(_translate("Form", "菜名"))
        self.LBFoodName.setText(_translate("Form", "TextLabel"))
        self.label_3.setText(_translate("Form", "数量"))
        self.EditQty.setText(_translate("Form", ""))
        self.BtnAddQty.setText(_translate("Form", "+"))
        self.BtnReduceQty.setText(_translate("Form", "-"))
        self.label_5.setText(_translate("Form", "单价"))
        # self.LBUnitPrice.setText(_translate("Form", "TextLabel"))
        self.label_4.setText(_translate("Form", "额外要求"))
        self.LBExtraRequirement.setText(_translate("Form", "TextLabel"))

        self.LBCahierTag.setText(_translate("Form", "服务员"))
        self.LBStaff.setText(_translate("Form", ""))
        self.LBCreateTimeTag.setText(_translate("Form", "下单时间"))
        self.LBCreateTime.setText(_translate("Form", ""))
        # self.pushButton_5.setText(_translate("Form", "PushButton"))
        self.BtnConfirm.setText(_translate("Form", "确认"))
        self.BtnCancel.setText(_translate("Form", "返回"))
        self.BtnAddLabel.setText(_translate("Form", "添加"))
        # self.pushButton_2.setText(_translate("Form", "PushButton"))
        # self.pushButton.setText(_translate("Form", "PushButton"))
        # self.pushButton_3.setText(_translate("Form", "PushButton"))
        # self.pushButton_4.setText(_translate("Form", "PushButton"))

    def AddNewTag(self):
        TagBtn = CTagBtn(self, len(self.TagList))
        TagBtn.NoteWeidget = self.LBExtraRequirement
        TagBtn.PriceWeidget = self.EditPrice
        self.FlowLayout.addWidget(TagBtn)
        self.TagList.append(TagBtn)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    logger = CreateLogger('test')
    ui = OrderDetailBasePanel(None)
    ui.show()
    sys.exit(app.exec())
