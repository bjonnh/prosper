import sys
import time

import prosper_common  # Protocols
from worker import Worker # Communication thread
from actions import Actions # Action management

from prosper_common import convert_cartridge_position

# Interfaces
from PyQt4 import QtCore, QtGui
from prosper_ui import Ui_MainWindow

from prosper_dialog_config import Dialog_Config
from prosper_dialog_racks import Dialog_Racks
from prosper_dialog_logger import Dialog_Logger
from prosper_dialog_add_action import Dialog_Add_Action
from prosper_dialog_wait import Dialog_Wait

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

changed_stylesheet="background-color:rgb(125,185,255);"

class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.thread = Worker(self)
        self.logger = Dialog_Logger(self) # This is the log box
        self.dialog_waituser = Dialog_Wait(self) # This is the askuser box
        self.waitingforuser=False # Indicator for the user wait
        self.actions=Actions()

        self.single_dialog_racks = Dialog_Racks("SINGLE")

        self.dialog_config = Dialog_Config(self)
        self.dialog_add_action = Dialog_Add_Action(self)
        self.add_actions()
        
        self.add_cartridges()
        # Due to a Qt Designer Bug we must enable the checkboxes
        #self.ui.checkBox_IN.setEnabled(True)        
        self.ui.checkBox_OUT1.setEnabled(True)
        self.ui.checkBox_OUT2.setEnabled(True)
        self.ui.checkBox_OUT3.setEnabled(True)        
        self.ui.checkBox_OUT4.setEnabled(True)
        self.ui.checkBox_pumponoff.setEnabled(True)

        self.connectActions()
        self.connect_all()

        # Timer for continuous updates
        self.prospekt_timer=QtCore.QTimer(self)
        self.connect(self.prospekt_timer, QtCore.SIGNAL("timeout()"), self.update_normal)
        
    def add_cartridges(self): # Populating the cartridges list
        for rack in range(1,3):
            for column in range(0,8):
                for row in range(1,13):
                    self.ui.comboBox_cartridge.addItem(str(rack)+chr(ord('A')+column)+str(row))
    def update_normal(self):
        if not self.thread.isRunning():
            self.thread.actionstart(self.actions.Get("PROSPEKT:NORMAL_UPDATE"))

    def update_all(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ALL_UPDATE"))
        
    def add_actions(self):
        fd=open("actions.cf","r")
        for i in fd:
            j=i.rstrip()
            self.actions.append(j)
                    
    def accept_single_rack_selection(self):
        left = self.single_dialog_racks.rack_left.selectedIndexes()
        right = self.single_dialog_racks.rack_right.selectedIndexes()

        current = None
        if len(right)==0:
            current = left
            rack="1"
        elif len(left)==0:
            current = right
            rack="2"
        if current != None:
            self.ui.comboBox_cartridge.setCurrentIndex(self.ui.comboBox_cartridge.findText(rack+chr(ord('A')+current[0].column())+str(12-current[0].row())))
        
    def actiondone(self,returncode=None,action=None,returnvalue=None):
        if returncode==True:
            if action != None:
                if returnvalue != None:
                    self.update_ui(action,returnvalue)
        
                self.ui.statusbar.showMessage("Done : "+action+" "+str(returncode))

    def disconnect_prospekt(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:DISCONNECT"))
        self.prospekt_timer.stop()
        self.ui.tab_systemview.setEnabled(False)
        self.ui.tab_manual.setEnabled(False)

    def connect_prospekt(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:CONNECT"),self.dialog_config.prospekt_port)
    def disconnect_pump(self):
        self.thread.actionstart(self.actions.Get("PUMP:DISCONNECT"))
    def connect_pump(self):
        self.thread.actionstart(self.actions.Get("PUMP:CONNECT"),self.dialog_config.pump_port)
    def connect_all(self):
        self.connect_prospekt()
        self.connect_pump()
    def disconnect_all(self):
        self.disconnect_prospekt()
        self.disconnect_pump()

    def testparameters(self):
        self.thread.actionstart(self.actions.Get("INTERNAL:DRYL"),5)

    def tray_unload(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_TRAY_UNLOAD"))
    def tray_load(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_TRAY_LOAD"))

    def get_versions(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:GET_VERSIONS"))


    def ace_panic(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_PANIC"))
    def hpd_panic(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_PANIC"))
    def panic(self):
        self.thread.panic()
        self.thread.actionstart(self.actions.Get("PROSPEKT:PANIC"))

    def acel_init(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_L_INIT"))
    def acer_init(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_R_INIT"))
    def acel_default(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_L_DEFAULT"))
    def acer_default(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_R_DEFAULT"))
    def acel_open(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_L_OPEN"))
    def acer_open(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_R_OPEN"))
    def acel_close(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_L_CLOSE"))
    def acer_close(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_R_CLOSE"))

    def acel_put(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_PUT"),convert_cartridge_position(1,self.ui.comboBox_cartridge.currentText()))
    def acer_put(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_PUT"),convert_cartridge_position(2,self.ui.comboBox_cartridge.currentText()))

    def acel_getback(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_GETBACK"),convert_cartridge_position(1,self.ui.comboBox_cartridge.currentText()))
    def acer_getback(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_GETBACK"),convert_cartridge_position(2,self.ui.comboBox_cartridge.currentText()))
                
    def ace_getback(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_GETBACK"))

    def ace_gripperl(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_GRIPPER"))
    def ace_gripperr(self):
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_GRIPPER"))


    def set_out(self,value=None):
        out=["0","0","0","0"]
        if self.ui.checkBox_OUT1.isChecked():
            out[3]="1"
        if self.ui.checkBox_OUT2.isChecked():
            out[2]="1"
        if self.ui.checkBox_OUT3.isChecked():
            out[1]="1"
        if self.ui.checkBox_OUT4.isChecked():
            out[0]="1"
        for i in range(0,4):
            self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_OUT_SET"),str(i+1)+"="+out[i])


    def hpdl_aspirate_speed(self,value=None):
        if value==None:
            value = self.ui.spinBox_hpdl_aspirate_speed.value()
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_L_ASPIRATE_SPEED_SET"),value)
    def hpdl_dispense_speed(self,value=None):
        if value==None:
            value = self.ui.spinBox_hpdl_dispense_speed.value()
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_L_DISPENSE_SPEED_SET"),value)
    def hpdr_aspirate_speed(self,value=None):
        if value==None:
            value = self.ui.spinBox_hpdr_aspirate_speed.value()
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_R_ASPIRATE_SPEED_SET"),value)
    def hpdr_dispense_speed(self,value=None):
        if value==None:
            value = self.ui.spinBox_hpdr_dispense_speed.value()
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_R_DISPENSE_SPEED_SET"),value)
    def hpdl_aspirate(self,value):
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_L_ASPIRATE"),self.ui.spinBox_hpdl_aspirate_volume.value())
    def hpdl_dispense(self,value):
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_L_DISPENSE"),self.ui.spinBox_hpdl_dispense_volume.value())
    def hpdr_aspirate(self,value):
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_R_ASPIRATE"),self.ui.spinBox_hpdr_aspirate_volume.value())
    def hpdr_dispense(self,value):
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_R_DISPENSE"),self.ui.spinBox_hpdr_dispense_volume.value())
    def hpdl_limit(self,value=None):
        self.ui.spinBox_hpdl_limit.clearFocus()
        if value==None:
            value = self.ui.spinBox_hpdl_limit.value()
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_L_LIMIT_SET"),value)
    def hpdr_limit(self,value=None):
        self.ui.spinBox_hpdr_limit.clearFocus()
        if value==None:
            value = self.ui.spinBox_hpdr_limit.value()
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_R_LIMIT_SET"),value)

# Actions to valves 
    def valve1_change(self,value):
        self.ui.comboBox_valve1.clearFocus()  # We are clearing focus in order to allow updates of values
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_VALVE1_SET"),value)
    def valve2_change(self,value):
        self.ui.comboBox_valve2.clearFocus()
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_VALVE2_SET"),value)
    def valve3_change(self,value):
        self.ui.comboBox_valve3.clearFocus()
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_VALVE3_SET"),value)
    def valve4_change(self,value):
        self.ui.comboBox_valve4.clearFocus()
        self.thread.actionstart(self.actions.Get("PROSPEKT:ACE_VALVE4_SET"),value+1)
    def valvel_change(self,value):
        self.ui.comboBox_valvel.clearFocus()
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_VALVEL_SET"),value+1)
    def valver_change(self,value):
        self.ui.comboBox_valver.clearFocus()
        self.thread.actionstart(self.actions.Get("PROSPEKT:HPD_VALVER_SET"),value+1)

    def rotatevalve(self,object,value,pixmap,step):
        pixmap = QtGui.QPixmap(_fromUtf8(pixmap))
        ow = pixmap.width()
        oh = pixmap.height()
        transform = QtGui.QTransform()
        pixmap = pixmap.transformed(transform.rotate(step*value))
        nw = pixmap.width()
        nh = pixmap.height()
        pixmap = pixmap.copy(nw/2-ow/2,nh/2-oh/2,ow,oh)
        object.setPixmap(pixmap)

    def hpdl_limit_changed(self,value):
        self.ui.spinBox_hpdl_limit.setStyleSheet(changed_stylesheet)
    def hpdr_limit_changed(self,value):
        self.ui.spinBox_hpdr_limit.setStyleSheet(changed_stylesheet)

    def pumpon(self):
        if self.ui.checkBox_pumponoff.isChecked():
            self.thread.actionstart(self.actions.Get("PUMP:ON"))
        else:
            self.thread.actionstart(self.actions.Get("PUMP:OFF"))
    def pumpflow_limit_changed(self):
        self.ui.spinBox_pumpflow.setStyleSheet(changed_stylesheet)
    def pumpflow(self,value=None):
        self.ui.spinBox_pumpflow.clearFocus()
        if value==None:
            value = self.ui.spinBox_pumpflow.value()
        self.thread.actionstart(self.actions.Get("PUMP:FLOW_SET"),value)
    def pumpstatus(self):
            self.thread.actionstart(self.actions.Get("PUMP:STATE_GET"))

    def connectActions(self):
        self.ui.actionQuit.triggered.connect(QtGui.qApp.quit)

        self.ui.comboBox_valve1.activated.connect(self.valve1_change)
        self.ui.comboBox_valve2.activated.connect(self.valve2_change)
        self.ui.comboBox_valve3.activated.connect(self.valve3_change)
        self.ui.comboBox_valve4.activated.connect(self.valve4_change)

        self.ui.comboBox_valvel.activated.connect(self.valvel_change)
        self.ui.comboBox_valver.activated.connect(self.valver_change)
        self.ui.spinBox_hpdl_aspirate_speed.editingFinished.connect(self.hpdl_aspirate_speed)
        self.ui.pushButton_hpdl_aspirate.clicked.connect(self.hpdl_aspirate)
        self.ui.spinBox_hpdl_dispense_speed.editingFinished.connect(self.hpdl_dispense_speed)
        self.ui.pushButton_hpdl_dispense.clicked.connect(self.hpdl_dispense)
        self.ui.spinBox_hpdr_aspirate_speed.editingFinished.connect(self.hpdr_aspirate_speed)
        self.ui.pushButton_hpdr_aspirate.clicked.connect(self.hpdr_aspirate)
        self.ui.spinBox_hpdr_dispense_speed.editingFinished.connect(self.hpdr_dispense_speed)
        self.ui.pushButton_hpdr_dispense.clicked.connect(self.hpdr_dispense)

        self.ui.spinBox_hpdl_limit.editingFinished.connect(self.hpdl_limit)
        self.ui.spinBox_hpdr_limit.editingFinished.connect(self.hpdr_limit)

        self.ui.spinBox_hpdl_limit.valueChanged.connect(self.hpdl_limit_changed)
        self.ui.spinBox_hpdr_limit.valueChanged.connect(self.hpdr_limit_changed)

        self.ui.pushButton_acel_init.clicked.connect(self.acel_init)
        self.ui.pushButton_acer_init.clicked.connect(self.acer_init)
        self.ui.pushButton_acel_default.clicked.connect(self.acel_default)
        self.ui.pushButton_acer_default.clicked.connect(self.acer_default)
        self.ui.pushButton_acel_open.clicked.connect(self.acel_open)
        self.ui.pushButton_acer_open.clicked.connect(self.acer_open) 
        self.ui.pushButton_acel_close.clicked.connect(self.acel_close)
        self.ui.pushButton_acer_close.clicked.connect(self.acer_close)

        self.ui.pushButton_ace_getback.clicked.connect(self.ace_getback)
        
        self.ui.pushButton_acel_put_cartridge.clicked.connect(self.acel_put)
        self.ui.pushButton_acer_put_cartridge.clicked.connect(self.acer_put)
        self.ui.pushButton_acel_getback.clicked.connect(self.acel_getback)
        self.ui.pushButton_acer_getback.clicked.connect(self.acer_getback)

        self.ui.pushButton_ace_gripperl.clicked.connect(self.ace_gripperl)
        self.ui.pushButton_ace_gripperr.clicked.connect(self.ace_gripperr)

        self.ui.pushButton_ace_panic.clicked.connect(self.ace_panic)
        self.ui.pushButton_hpd_panic.clicked.connect(self.hpd_panic)
        self.ui.pushButton_panic.clicked.connect(self.panic)

        self.ui.checkBox_OUT1.clicked.connect(self.set_out)
        self.ui.checkBox_OUT2.clicked.connect(self.set_out)
        self.ui.checkBox_OUT3.clicked.connect(self.set_out)
        self.ui.checkBox_OUT4.clicked.connect(self.set_out)

        self.ui.pushButton_sys_inf.clicked.connect(self.get_versions)

        self.ui.pushButton_tray_unload.clicked.connect(self.tray_unload)
        self.ui.pushButton_tray_load.clicked.connect(self.tray_load)
        
        self.ui.pushButton_racks.clicked.connect(self.single_dialog_racks.show)

        self.connect(self.thread, QtCore.SIGNAL("donesignal(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)"), self.actiondone)
        self.connect(self.thread, QtCore.SIGNAL("sizeofqueue(int)"),self.update_queue)

        self.single_dialog_racks.accepted.connect(self.accept_single_rack_selection)

        self.ui.checkBox_pumponoff.clicked.connect(self.pumpon)
        self.ui.spinBox_pumpflow.editingFinished.connect(self.pumpflow)
        self.ui.spinBox_pumpflow.valueChanged.connect(self.pumpflow_limit_changed)

        self.ui.actionEdit.triggered.connect(self.dialog_config.show)
        self.ui.actionLog.triggered.connect(self.logger.show)


        # Automation part
        self.ui.pushButton_add.clicked.connect(self.add_automation_action)
        self.ui.pushButton_remove.clicked.connect(self.remove_automation_action)
        self.ui.pushButton_moveup.clicked.connect(self.moveup_automation_action)
        self.ui.pushButton_movedown.clicked.connect(self.movedown_automation_action)
        self.ui.pushButton_sys_inf.clicked.connect(self.get_versions)
        self.ui.pushButton_launch.clicked.connect(self.launch_actions)

        self.ui.listWidget_automation.doubleClicked.connect(self.edit_automation_action)
        self.connect(self.dialog_add_action, QtCore.SIGNAL("done_add_automation_action(PyQt_PyObject)"), self.done_add_automation_action)
        self.connect(self.dialog_add_action, QtCore.SIGNAL("select_automation_action(int)"), self.select_automation_action)
        self.connect(self.dialog_add_action, QtCore.SIGNAL("add_action_array(PyQt_PyObject)"), self.actions.append_array)
        self.connect(self, QtCore.SIGNAL("start_action(QString)"), self.start_action)
        self.connect(self, QtCore.SIGNAL("force_clearqueue()"), self.thread._clearqueue)

        self.ui.pushButton_clearqueue.clicked.connect(self.thread.clearqueue)

    def start_action(self,action):
        self.thread.actionstart(self.actions.Get(action))


    def select_automation_action(self,index):
        self.ui.listWidget_automation.setCurrentRow(index)
    def moveup_automation_action(self):
        index=self.ui.listWidget_automation.currentRow()
        if index !=0:
            self.dialog_add_action.swap(index,index-1)
    def movedown_automation_action(self):
        index=self.ui.listWidget_automation.currentRow()
        if index !=self.ui.listWidget_automation.count()-1:
            self.dialog_add_action.swap(index,index+1)

    def edit_automation_action(self):
        index=self.ui.listWidget_automation.currentRow()
        self.dialog_add_action.edit(index)
        self.dialog_add_action.show()
    def remove_automation_action(self):
        index=self.ui.listWidget_automation.currentRow()
        self.dialog_add_action.remove(index)
    def done_add_automation_action(self,titles):
        self.ui.listWidget_automation.clear()
        for title in titles:
            self.ui.listWidget_automation.addItem(title)
    def launch_actions(self):
        self.dialog_add_action.launch()
    def add_automation_action(self):
        self.dialog_add_action.add()
        self.dialog_add_action.show()
    def update_queue(self,value):
        self.ui.label_queuesize_val.setText(str(value))
    def update_ui(self,name,value):
        if name == "PROSPEKT:CONNECT":
            self.update_all()
            self.prospekt_timer.start(3000)
            self.ui.tab_systemview.setEnabled(True)
            self.ui.tab_manual.setEnabled(True)
            self.dialog_config.refresh()
        elif name == "PUMP:FLOW_GET":
            if not self.ui.spinBox_pumpflow.hasFocus():
                self.ui.spinBox_pumpflow.setValue(value)
                self.ui.spinBox_pumpflow.setStyleSheet("")                        
        elif name == "PROSPEKT:ACE_VALVE1_GET":
            self.ui.comboBox_valve1.setCurrentIndex(value)
            self.rotatevalve(self.ui.label_v1_finger,value,":/images/images/8valve_fingers.svg",45)
        elif name == "PROSPEKT:ACE_VALVE2_GET":
            self.ui.comboBox_valve2.setCurrentIndex(value)
            self.rotatevalve(self.ui.label_v2_finger,value,":/images/images/6valve_fingers.svg",60)
        elif name == "PROSPEKT:ACE_VALVE3_GET":
            self.ui.comboBox_valve3.setCurrentIndex(value)
            self.rotatevalve(self.ui.label_v3_finger,value,":/images/images/6valve_fingers.svg",60)
        elif name == "PROSPEKT:ACE_VALVE4_GET":
            value=value-1
            self.ui.comboBox_valve4.setCurrentIndex(value)
            self.rotatevalve(self.ui.label_v4_finger,value,":/images/images/9valve_fingers.svg",-45)
        elif name == "PROSPEKT:HPD_VALVEL_GET":
            value=value-1
            self.ui.comboBox_valvel.setCurrentIndex(value)
            self.rotatevalve(self.ui.label_vl_finger,value,":/images/images/7valve_finger.svg",-60)            
        elif name == "PROSPEKT:HPD_VALVER_GET":
            value=value-1
            self.ui.comboBox_valver.setCurrentIndex(value)
            self.rotatevalve(self.ui.label_vr_finger,value,":/images/images/7valve_finger.svg",-60)

        elif name == "PROSPEKT:HPD_L_LIMIT_GET":
            if not self.ui.spinBox_hpdl_limit.hasFocus():
                self.ui.spinBox_hpdl_limit.setValue(value)
                self.ui.spinBox_hpdl_limit.setStyleSheet("")            
        elif name == "PROSPEKT:HPD_R_LIMIT_GET":
            if not self.ui.spinBox_hpdr_limit.hasFocus():
                self.ui.spinBox_hpdr_limit.setValue(value)
                self.ui.spinBox_hpdr_limit.setStyleSheet("")            
        elif name == "PROSPEKT:HPD_L_SYRVOL_GET":
            self.ui.progressBar_hpdl.setMaximum(value)
        elif name == "PROSPEKT:HPD_R_SYRVOL_GET":
            self.ui.progressBar_hpdr.setMaximum(value)
        elif name == "PROSPEKT:HPD_L_PRESSURE_GET":
            self.ui.lcdNumber_hpdl.display(value)
        elif name == "PROSPEKT:HPD_R_PRESSURE_GET":
            self.ui.lcdNumber_hpdr.display(value)
        elif name == "PROSPEKT:ACE_IN_GET":
            value="%04d"%value
            if value[3]=="1":
                self.ui.checkBox_IN.setChecked(True)
        elif name == "PROSPEKT:ACE_OUT_GET":

            value="%04d"%value
            self.outs=value
            if value[3]=="1":
                self.ui.checkBox_OUT1.setChecked(True)
            if value[2]=="1":
                self.ui.checkBox_OUT2.setChecked(True)
            if value[1]=="1":
                self.ui.checkBox_OUT3.setChecked(True)
            if value[0]=="1":
                self.ui.checkBox_OUT4.setChecked(True)

        elif name == "PROSPEKT:ACE_L_CLAMP_GET":
            pass
        elif name == "PROSPEKT:ACE_R_CLAMP_GET":
            pass
        elif name == "PROSPEKT:HPD_L_ASPIRATE_SPEED_GET":
            self.ui.spinBox_hpdl_aspirate_speed.setValue(value)
        elif name == "PROSPEKT:HPD_L_DISPENSE_SPEED_GET":
            self.ui.spinBox_hpdl_dispense_speed.setValue(value)
        elif name == "PROSPEKT:HPD_R_ASPIRATE_SPEED_GET":
            self.ui.spinBox_hpdr_aspirate_speed.setValue(value)
        elif name == "PROSPEKT:HPD_R_DISPENSE_SPEED_GET":
            self.ui.spinBox_hpdr_dispense_speed.setValue(value)
        elif name == "PROSPEKT:HPD_L_VOLUME_GET":
            self.ui.spinBox_hpdl_dispense_volume.setMaximum(value)
            self.ui.spinBox_hpdl_aspirate_volume.setMaximum(self.ui.progressBar_hpdl.maximum()-value)
            self.ui.progressBar_hpdl.setValue(value)
        elif name == "PROSPEKT:HPD_R_VOLUME_GET":
            self.ui.spinBox_hpdr_dispense_volume.setMaximum(value)
            self.ui.spinBox_hpdr_aspirate_volume.setMaximum(self.ui.progressBar_hpdr.maximum()-value)
            self.ui.progressBar_hpdr.setValue(value)
# Versions stuff
        elif name == "PROSPEKT:ACE_GET_NUM_TRANSPORT":
            self.ui.label_sysinf_ace_transport_counter_val.setText(str(value))
        elif name == "PROSPEKT:ACE_GET_NUM_VALVE4":
            self.ui.label_sysinf_ace_valve4_val.setText(str(value))
        elif name == "PROSPEKT:ACE_GET_NUM_VALVE3":
            self.ui.label_sysinf_ace_valve3_val.setText(str(value))
        elif name == "PROSPEKT:ACE_GET_NUM_VALVE2":
            self.ui.label_sysinf_ace_valve2_val.setText(str(value))
        elif name == "PROSPEKT:ACE_GET_NUM_VALVE1":
            self.ui.label_sysinf_ace_valve1_val.setText(str(value))
        elif name == "PROSPEKT:HPD_GET_NUM_VALVER":
            self.ui.label_sysinf_hpd_valver_val.setText(str(value))
        elif name == "PROSPEKT:HPD_GET_NUM_VALVEL":
            self.ui.label_sysinf_hpd_valvel_val.setText(str(value))
        elif name == "PROSPEKT:ACE_GET_VER_MCCB":
            self.ui.label_sysinf_ace_MCCB_val.setText(str(value))
        elif name == "PROSPEKT:ACE_GET_VER_ISS":
            self.ui.label_sysinf_ace_ISS_val.setText(str(value))
        elif name == "PROSPEKT:ACE_GET_VER_RF":
            self.ui.label_sysinf_ace_RF_val.setText(str(value))
        elif name == "PROSPEKT:ACE_GET_VER_MPV":
            self.ui.label_sysinf_ace_MPV_val.setText(str(value))
        elif name == "PROSPEKT:ACE_GET_VER_TASPE":
            self.ui.label_sysinf_ace_TASPE_val.setText(str(value))            
        elif name == "PROSPEKT:ACE_GET_VER_TRANSPORT":
            self.ui.label_sysinf_ace_transport_val.setText(str(value))            
        elif name == "PROSPEKT:ACE_GET_VER_FEEDER":
            self.ui.label_sysinf_ace_feeder_val.setText(str(value))            
        elif name == "PROSPEKT:ACE_GET_VER_CLAMPL":
            self.ui.label_sysinf_ace_clampL_val.setText(str(value))            
        elif name == "PROSPEKT:ACE_GET_VER_CLAMPR":
            self.ui.label_sysinf_ace_clampR_val.setText(str(value))            
        elif name == "PROSPEKT:HPD_GET_VER_MCCB":
            self.ui.label_sysinf_hpd_MCCB_val.setText(str(value))            
        elif name == "PROSPEKT:HPD_GET_VER_SSM":
            self.ui.label_sysinf_hpd_SSM_val.setText(str(value))            
        elif name == "PROSPEKT:HPD_GET_VER_DISPENSERL":
            self.ui.label_sysinf_hpd_dispenserL_val.setText(str(value))      
        elif name == "PROSPEKT:HPD_GET_VER_DISPENSERR":
            self.ui.label_sysinf_hpd_dispenserR_val.setText(str(value))      
        else:
            self.logger.log("ERROR","UNKNOWN RETURN DATA: "+name+" = "+str(value))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    myapp = MyWindow()

    app.setStyle("Plastique")

    myapp.show()

    sys.exit(app.exec_())        


