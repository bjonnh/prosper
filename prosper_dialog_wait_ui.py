# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prosper_dialog_wait.ui'
#
# Created: Fri Apr  6 15:29:51 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog_wait(object):
    def setupUi(self, Dialog_wait):
        Dialog_wait.setObjectName(_fromUtf8("Dialog_wait"))
        Dialog_wait.resize(400, 300)
        self.pushButton_stop = QtGui.QPushButton(Dialog_wait)
        self.pushButton_stop.setGeometry(QtCore.QRect(30, 220, 130, 60))
        self.pushButton_stop.setObjectName(_fromUtf8("pushButton_stop"))
        self.pushButton_continue = QtGui.QPushButton(Dialog_wait)
        self.pushButton_continue.setGeometry(QtCore.QRect(240, 220, 130, 60))
        self.pushButton_continue.setObjectName(_fromUtf8("pushButton_continue"))
        self.label = QtGui.QLabel(Dialog_wait)
        self.label.setGeometry(QtCore.QRect(30, 50, 341, 131))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(Dialog_wait)
        QtCore.QMetaObject.connectSlotsByName(Dialog_wait)

    def retranslateUi(self, Dialog_wait):
        Dialog_wait.setWindowTitle(QtGui.QApplication.translate("Dialog_wait", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_stop.setText(QtGui.QApplication.translate("Dialog_wait", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_continue.setText(QtGui.QApplication.translate("Dialog_wait", "Continue", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog_wait", "Next cartridge is ready, what\'s next ?", None, QtGui.QApplication.UnicodeUTF8))

