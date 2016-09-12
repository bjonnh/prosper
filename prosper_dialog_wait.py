from PyQt4 import QtCore, QtGui
import os

from prosper_dialog_wait_ui import Ui_Dialog_wait

class Dialog_Wait(QtGui.QDialog,Ui_Dialog_wait):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        self.parent=parent
        self.setupUi(self)
        self.setModal(False)
        QtCore.QObject.connect(self.parent.thread,QtCore.SIGNAL("waituser(QString)"),self.waituser)
        self.pushButton_stop.clicked.connect(self.send_stop)
        self.pushButton_continue.clicked.connect(self.send_continue)
    def waituser(self,msg):
        self.show()
        self.parent.waitingforuser=True
    def send_stop(self):
        self.parent.waitingforuser=False
        self.parent.emit(QtCore.SIGNAL("force_clearqueue()"))
        self.hide()
    def send_continue(self):
        self.parent.waitingforuser=False
        self.hide()
