# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prosper_dialog_logger.ui'
#
# Created: Fri Mar 16 18:14:39 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog_logger(object):
    def setupUi(self, Dialog_logger):
        Dialog_logger.setObjectName(_fromUtf8("Dialog_logger"))
        Dialog_logger.resize(644, 506)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog_logger)
        self.buttonBox.setGeometry(QtCore.QRect(290, 470, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.textEdit = QtGui.QTextEdit(Dialog_logger)
        self.textEdit.setGeometry(QtCore.QRect(10, 30, 621, 431))
        self.textEdit.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);"))
        self.textEdit.setAutoFormatting(QtGui.QTextEdit.AutoAll)
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setAcceptRichText(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.checkBox_warnings = QtGui.QCheckBox(Dialog_logger)
        self.checkBox_warnings.setGeometry(QtCore.QRect(10, 10, 91, 20))
        self.checkBox_warnings.setObjectName(_fromUtf8("checkBox_warnings"))
        self.checkBox_errors = QtGui.QCheckBox(Dialog_logger)
        self.checkBox_errors.setGeometry(QtCore.QRect(100, 10, 91, 20))
        self.checkBox_errors.setChecked(True)
        self.checkBox_errors.setObjectName(_fromUtf8("checkBox_errors"))
        self.checkBox_debug = QtGui.QCheckBox(Dialog_logger)
        self.checkBox_debug.setGeometry(QtCore.QRect(560, 10, 71, 20))
        self.checkBox_debug.setObjectName(_fromUtf8("checkBox_debug"))
        self.checkBox_scroll = QtGui.QCheckBox(Dialog_logger)
        self.checkBox_scroll.setGeometry(QtCore.QRect(330, 10, 91, 20))
        self.checkBox_scroll.setChecked(True)
        self.checkBox_scroll.setObjectName(_fromUtf8("checkBox_scroll"))

        self.retranslateUi(Dialog_logger)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_logger.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_logger.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_logger)

    def retranslateUi(self, Dialog_logger):
        Dialog_logger.setWindowTitle(QtGui.QApplication.translate("Dialog_logger", "Prosper-Log", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_warnings.setText(QtGui.QApplication.translate("Dialog_logger", "Warnings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_errors.setText(QtGui.QApplication.translate("Dialog_logger", "Errors", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_debug.setText(QtGui.QApplication.translate("Dialog_logger", "Debug", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_scroll.setText(QtGui.QApplication.translate("Dialog_logger", "Auto-scroll", None, QtGui.QApplication.UnicodeUTF8))

