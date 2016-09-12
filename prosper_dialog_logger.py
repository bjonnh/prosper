from PyQt4 import QtCore, QtGui
import os

from prosper_dialog_logger_ui import Ui_Dialog_logger

class Dialog_Logger(QtGui.QDialog,Ui_Dialog_logger):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        self.parent=parent
        self.setupUi(self)
        self.setModal(False)
        self.log("DEBUG","Logger started")
        QtCore.QObject.connect(self.parent.thread,QtCore.SIGNAL("log(QString,QString)"),self.log)
    def log(self,msgtype,msg):
        if msgtype == "ERROR":
            prefix="<font color=\"#FF0000\">"
        if msgtype == "WARNING":
            prefix="<font color=\"#0000FF\">"            
        if msgtype == "DEBUG":
            prefix="<font color=\"#00FF00\">"            
        suffix="</font>"
        if msgtype == "WARNING" and not self.checkBox_warnings.isChecked() :
            return(False)
        if msgtype == "ERROR" and not self.checkBox_errors.isChecked() :
            return(False)
        if msgtype == "DEBUG" and not self.checkBox_debug.isChecked() :
            return(False)
        self.textEdit.append(prefix+msgtype+":"+msg+suffix)
        if self.checkBox_scroll.isChecked():
            self.textEdit.moveCursor(QtGui.QTextCursor.End)

