# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prosper_dialog_config.ui'
#
# Created: Fri Mar 16 19:38:41 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog_config(object):
    def setupUi(self, Dialog_config):
        Dialog_config.setObjectName(_fromUtf8("Dialog_config"))
        Dialog_config.resize(568, 429)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog_config)
        self.buttonBox.setGeometry(QtCore.QRect(220, 390, 341, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.comboBox_prospekt = QtGui.QComboBox(Dialog_config)
        self.comboBox_prospekt.setGeometry(QtCore.QRect(230, 160, 171, 25))
        self.comboBox_prospekt.setEditable(True)
        self.comboBox_prospekt.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.comboBox_prospekt.setObjectName(_fromUtf8("comboBox_prospekt"))
        self.label_prospekt = QtGui.QLabel(Dialog_config)
        self.label_prospekt.setGeometry(QtCore.QRect(100, 165, 131, 16))
        self.label_prospekt.setObjectName(_fromUtf8("label_prospekt"))
        self.comboBox_pump = QtGui.QComboBox(Dialog_config)
        self.comboBox_pump.setGeometry(QtCore.QRect(230, 190, 171, 25))
        self.comboBox_pump.setEditable(True)
        self.comboBox_pump.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.comboBox_pump.setObjectName(_fromUtf8("comboBox_pump"))
        self.label_pump = QtGui.QLabel(Dialog_config)
        self.label_pump.setGeometry(QtCore.QRect(100, 200, 131, 16))
        self.label_pump.setObjectName(_fromUtf8("label_pump"))
        self.pushButton_refresh = QtGui.QPushButton(Dialog_config)
        self.pushButton_refresh.setGeometry(QtCore.QRect(200, 120, 92, 27))
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.pushButton_disconnect_prospekt = QtGui.QPushButton(Dialog_config)
        self.pushButton_disconnect_prospekt.setGeometry(QtCore.QRect(480, 160, 81, 27))
        self.pushButton_disconnect_prospekt.setObjectName(_fromUtf8("pushButton_disconnect_prospekt"))
        self.pushButton_disconnect_pump = QtGui.QPushButton(Dialog_config)
        self.pushButton_disconnect_pump.setGeometry(QtCore.QRect(480, 190, 81, 27))
        self.pushButton_disconnect_pump.setObjectName(_fromUtf8("pushButton_disconnect_pump"))
        self.pushButton_disconnect_all = QtGui.QPushButton(Dialog_config)
        self.pushButton_disconnect_all.setGeometry(QtCore.QRect(290, 120, 111, 27))
        self.pushButton_disconnect_all.setObjectName(_fromUtf8("pushButton_disconnect_all"))
        self.pushButton_connect_pump = QtGui.QPushButton(Dialog_config)
        self.pushButton_connect_pump.setGeometry(QtCore.QRect(400, 190, 81, 27))
        self.pushButton_connect_pump.setObjectName(_fromUtf8("pushButton_connect_pump"))
        self.pushButton_connect_prospekt = QtGui.QPushButton(Dialog_config)
        self.pushButton_connect_prospekt.setGeometry(QtCore.QRect(400, 160, 81, 27))
        self.pushButton_connect_prospekt.setObjectName(_fromUtf8("pushButton_connect_prospekt"))
        self.label = QtGui.QLabel(Dialog_config)
        self.label.setGeometry(QtCore.QRect(100, 260, 161, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog_config)
        self.label_2.setGeometry(QtCore.QRect(100, 280, 161, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_prospekt_port = QtGui.QLabel(Dialog_config)
        self.label_prospekt_port.setGeometry(QtCore.QRect(250, 260, 191, 16))
        self.label_prospekt_port.setText(_fromUtf8(""))
        self.label_prospekt_port.setObjectName(_fromUtf8("label_prospekt_port"))
        self.label_pump_port = QtGui.QLabel(Dialog_config)
        self.label_pump_port.setGeometry(QtCore.QRect(250, 280, 191, 16))
        self.label_pump_port.setText(_fromUtf8(""))
        self.label_pump_port.setObjectName(_fromUtf8("label_pump_port"))

        self.retranslateUi(Dialog_config)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_config.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_config.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_config)

    def retranslateUi(self, Dialog_config):
        Dialog_config.setWindowTitle(QtGui.QApplication.translate("Dialog_config", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_prospekt.setText(QtGui.QApplication.translate("Dialog_config", "Prospekt serial port", None, QtGui.QApplication.UnicodeUTF8))
        self.label_pump.setText(QtGui.QApplication.translate("Dialog_config", "Pump serial port", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_refresh.setText(QtGui.QApplication.translate("Dialog_config", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_disconnect_prospekt.setText(QtGui.QApplication.translate("Dialog_config", "Disconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_disconnect_pump.setText(QtGui.QApplication.translate("Dialog_config", "Disconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_disconnect_all.setText(QtGui.QApplication.translate("Dialog_config", "Disconnect all", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_connect_pump.setText(QtGui.QApplication.translate("Dialog_config", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_connect_prospekt.setText(QtGui.QApplication.translate("Dialog_config", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog_config", "Actual prospekt port :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog_config", "Actual pump port :", None, QtGui.QApplication.UnicodeUTF8))

