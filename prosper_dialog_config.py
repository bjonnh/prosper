from PyQt4 import QtCore, QtGui
import os

from prosper_dialog_config_ui import Ui_Dialog_config

class Dialog_Config(QtGui.QDialog,Ui_Dialog_config):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        self.parent=parent
        self.setupUi(self)
        self.setModal(False)
        self.pushButton_refresh.clicked.connect(self.refresh)
        self.pushButton_disconnect_all.clicked.connect(self.parent.disconnect_all)
        self.pushButton_disconnect_prospekt.clicked.connect(self.parent.disconnect_prospekt)
        self.pushButton_disconnect_pump.clicked.connect(self.parent.disconnect_pump)
        self.pushButton_connect_prospekt.clicked.connect(self.connect_prospekt)
        self.pushButton_connect_pump.clicked.connect(self.connect_pump)
        self.accepted.connect(self.closing)
        self.prospekt_port = "Not connected"
        self.pump_port = "Not connected"
        fd=None
        try:
            fd=open("prosper.cf","r")
        except:
            print("ERROR: Configuration file does not exists")
        if fd !=None:
            for line in fd:
                linestrip = line.rstrip()
                linesplit = linestrip.split("=")
                if linesplit[0]=="PROSPEKT":
                    self.prospekt_port = linesplit[1]
                if linesplit[0]=="PUMP":
                    self.pump_port = linesplit[1]
            fd.close()
        self.refresh()
    def connect_pump(self):
        self.pump_port=self.comboBox_pump.currentText()
        self.parent.connect_pump()
    def connect_prospekt(self):
        self.prospekt_port=self.comboBox_prospekt.currentText()
        self.parent.connect_prospekt()
    def closing(self):
        self.copy_ports()

        fd=open("prosper.cf","w")
        fd.write("PROSPEKT="+self.prospekt_port+"\n")
        fd.write("PUMP="+self.pump_port+"\n")
        fd.close()        
    def copy_ports(self):
        self.prospekt_port=self.comboBox_prospekt.currentText()
        self.pump_port=self.comboBox_pump.currentText()
    def refresh(self):
        self.label_prospekt_port.setText(self.prospekt_port)
        self.label_pump_port.setText(self.pump_port)
        self.comboBox_prospekt.clear()
        other_ports=['/dev/pts/','/dev/ttyr0']
        for i in self.parent.thread.communicator.get_comports(): # From serial.tools.list_ports
            self.add_port(i[0])
        for j in other_ports:
            for k in range(0,9):
                if not os.path.exists(j+str(k)):
                    continue
                self.add_port(j+str(k))
        self.add_port(self.prospekt_port)
        self.add_port(self.pump_port)
        self.comboBox_prospekt.setCurrentIndex(self.comboBox_prospekt.findText(self.prospekt_port))
        self.comboBox_pump.setCurrentIndex(self.comboBox_pump.findText(self.pump_port))
    def add_port(self,port):
        self.comboBox_pump.addItem(port)
        self.comboBox_prospekt.addItem(port)
