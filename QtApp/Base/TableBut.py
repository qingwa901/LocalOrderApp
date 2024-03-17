from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QPixmap
from functools import partial


class TableStatus:
    Empty = 0
    Started = 1
    Finishing = 2


class TableBut(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.IsDrag = False

    def setupUi(self, TableNumber):
        self.TableNumber = TableNumber
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setObjectName(f"Table{TableNumber}")
        _translate = QtCore.QCoreApplication.translate
        self.setText(_translate("Form", f"{TableNumber}号桌"))

    def setupColor(self, Status):
        self.setAttribute(Qt.WA_StyledBackground, True)
        if Status == 0:
            self.setStyleSheet('background-color: white;')
        elif Status == 1:
            self.setStyleSheet('background-color: yellow;')
        elif Status == 2:
            self.setStyleSheet('background-color: red;')

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragStartPosition = event.pos()

    def mouseReleaseEvent(self, event):
        if ((event.pos() - self.dragStartPosition).manhattanLength()
                < QtWidgets.QApplication.startDragDistance()):
            self.ClickEvent()

    def mouseMoveEvent(self, event):
        if not (event.buttons() == QtCore.Qt.LeftButton):
            return
        if ((event.pos() - self.dragStartPosition).manhattanLength()
                < QtWidgets.QApplication.startDragDistance()):
            return
        self.IsDrag = True
        drag = QDrag(self)
        mime = QMimeData()
        drag.setMimeData(mime)
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.exec_(Qt.MoveAction)

    def BindEvent(self, Event):
        self.ClickEventFunction = Event

    def ClickEvent(self):
        if self.ClickEventFunction is not None:
            self.ClickEventFunction(self.TableNumber)
