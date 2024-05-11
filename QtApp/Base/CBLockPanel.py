from .CWidget import CWidget


class BlockPanel(CWidget):
    def __init__(self, aParent):
        CWidget.__init__(self, aParent)
        self.PanelList = []
        self.mousePressEvent = lambda x: self.Close()

    def Resize(self):
        self.resize(self.parent().width(), self.parent().height())

    def Show(self, Panel, CloseEvent):
        self.setVisible(True)
        self.Resize()
        self.lower()
        self.stackUnder(Panel)
        self.PanelList.append((Panel, CloseEvent))

    def Close(self):
        if len(self.PanelList) > 0:
            panel, event = self.PanelList.pop()
            event()
        if len(self.PanelList) == 0:
            self.setVisible(False)
        else:
            self.setVisible(True)
            self.Resize()
            self.lower()
            self.stackUnder(self.PanelList[-1][0])

