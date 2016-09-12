from PyQt4 import QtCore, QtGui

from prosper_dialog_racks_ui import Ui_Dialog_racks
from widgets import ImageWidget


class Dialog_Racks(QtGui.QDialog,Ui_Dialog_racks):
    def __init__(self,selection_type="SINGLE"):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.setModal(False)
        self.pushButton_clear_left.clicked.connect(self.unselect_left)
        self.pushButton_clear_right.clicked.connect(self.unselect_right)
        self.pushButton_clear_both.clicked.connect(self.unselect_both)

        for i in range(0,8):
            for j in range(0,12):
                self.rack_left.setCellWidget(j, i, ImageWidget(":/images/images/cartridge.svg",chr(ord('A')+i)+str(12-j),self))
                self.rack_right.setCellWidget(j, i, ImageWidget(":/images/images/cartridge.svg",chr(ord('A')+i)+str(12-j),self))

        if selection_type=="SINGLE":
            self.rack_left.setSelectionMode( QtGui.QAbstractItemView.SingleSelection)
            self.rack_right.setSelectionMode( QtGui.QAbstractItemView.SingleSelection)
            self.rack_left.currentCellChanged.connect(self.unselect_right)
            self.rack_right.currentCellChanged.connect(self.unselect_left)            
        else:
            self.rack_left.setSelectionMode( QtGui.QAbstractItemView.MultiSelection)
            self.rack_right.setSelectionMode( QtGui.QAbstractItemView.MultiSelection)    
    def unselect_left(self):
        self.rack_left.clearSelection()
    def unselect_right(self):
        self.rack_right.clearSelection()
    def unselect_both(self):
        self.unselect_left()
        self.unselect_right()
