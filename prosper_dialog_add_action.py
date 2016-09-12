from PyQt4 import QtCore, QtGui


from prosper_dialog_add_action_ui import Ui_Dialog_add_action
from widgets import ImageWidget
from natural import natural # Natural sorting for cartridges
from prosper_common import convert_cartridge_position


class AutomationAction:
    def __init__(self,type="Condition",comment="",cartridges=[],parameters={}):
        self.type = type
        self.comment = comment
        self.cartridges = cartridges
        self.parameters = parameters
    def set(self,type="Condition",comment="",cartridges=[],parameters={}):
        self.type = type
        self.comment = comment
        self.cartridges = cartridges
        self.parameters = parameters

class AutomationActions:
    def choose_solvent(solvent):
        # TODO Add an intelligent system for HPD solvents
        if solvent >= 0 and solvent <=4:
            return([])
    def export_action(action):
        output_action=[]
        currentcartridge=None
        cartridges = sorted(action.cartridges,key=natural)

        output_action.append(AutomationActions.valve3(action)) # Choose the output
        output_action.append("PROSPEKT:ACE_VALVE1_SET(0)") 
        output_action.append("PROSPEKT:ACE_VALVE2_SET(1)") 

        # TODO Verif rack
        # TODO Alternate cartridges
        # TODO add non stopable/stopable
        for cartridge in cartridges:
            if currentcartridge != None:
                output_action.append("PROSPEKT:ACE_GETBACK("+currentcartridge+")")
            currentcartridge = convert_cartridge_position(1,cartridge)
            output_action.append("PROSPEKT:ACE_PUT("+currentcartridge+")")

            # Waiting for user action if needed
            if action.parameters['askcartridges'] == True :
                output_action.append("INTERNAL:WAITUSER(\"Hello\")")
            
            # Action specific
            if action.type == "Flow":
                if action.parameters['solvent1_flow'] !=0 and action.parameters['solvent1_volume'] !=0:
                    output_action.append("INTERNAL:NEEDEDSOLVENT("+str(action.parameters['solvent1_solvent'])+")")
                    output_action.append("INTERNAL:NEEDEDSOLVENTFLOW("+str(action.parameters['solvent1_flow'])+")")
                    output_action.append("INTERNAL:NEEDEDSOLVENTVOLUME("+str(action.parameters['solvent1_volume'])+")")
                    output_action.append("INTERNAL:NEEDEDSOLVENTACT")
                if action.parameters['solvent2_flow'] !=0 and action.parameters['solvent2_volume'] !=0:
                    output_action.append("INTERNAL:NEEDEDSOLVENT("+str(action.parameters['solvent2_solvent'])+")")
                    output_action.append("INTERNAL:NEEDEDSOLVENTFLOW("+str(action.parameters['solvent2_flow'])+")")
                    output_action.append("INTERNAL:NEEDEDSOLVENTVOLUME("+str(action.parameters['solvent2_volume'])+")")
                    output_action.append("INTERNAL:NEEDEDSOLVENTACT")
            elif action.type == "Dry":
                output_action.append("PROSPEKT:ACE_VALVE4_SET(3)") # TODO Check for N2
                output_action.append("PROSPEKT:ACE_OUT_SET(1111)") # TODO Mask for out
                output_action.append("INTERNAL:WAIT("+str(action.parameters['dry_drytime'])+")")
                output_action.append("PROSPEKT:ACE_OUT_SET(0000)") # TODO Mask for out
            elif action.type == "Input to SPE":
                print("Input to SPE")
        output_action.append("PROSPEKT:ACE_GETBACK("+currentcartridge+")") # Getting back the last cartridges
        print(action.type+" "+str(output_action))
        return(output_action)
    def valve3(action):
        # Check if it is the right order
        # Used to choose the output
        return("PROSPEKT:ACE_VALVE3_SET("+str(action.parameters['output'])+")")


class Dialog_Add_Action(QtGui.QDialog,Ui_Dialog_add_action):
    defined_actions=[]
    current_action=0
    addmode=False
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        self.parent=parent
        self.setupUi(self)
        self.setModal(False)
        self.pushButton_clear_left.clicked.connect(self.unselect_left)
        self.pushButton_clear_right.clicked.connect(self.unselect_right)
        self.pushButton_clear_both.clicked.connect(self.unselect_both)
        self.tabWidget.tabBar().setVisible(0)
        for i in range(0,8):
            for j in range(0,12):
                self.rack_left.setCellWidget(j, i, ImageWidget(":/images/images/cartridge.svg",chr(ord('A')+i)+str(12-j),self))
                self.rack_right.setCellWidget(j, i, ImageWidget(":/images/images/cartridge.svg",chr(ord('A')+i)+str(12-j),self))

        self.rack_left.setSelectionMode( QtGui.QAbstractItemView.MultiSelection)
        self.rack_right.setSelectionMode( QtGui.QAbstractItemView.MultiSelection)    

        self.accepted.connect(self.send_data_back)
    def send_data_back(self):
        if self.addmode==True:
            self.defined_actions.append(AutomationAction())
            self.current_action=len(self.defined_actions)-1
        self.grab_data()
        self.update_parent()
    def update_parent(self):
        self.emit(QtCore.SIGNAL("done_add_automation_action(PyQt_PyObject)"),self.get_items())
    def unselect_left(self):
        self.rack_left.clearSelection()
    def unselect_right(self):
        self.rack_right.clearSelection()
    def unselect_both(self):
        self.unselect_left()
        self.unselect_right()
    def add(self):
        self.addmode=True
        self.comboBox_action.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.show()
    def get_items(self):
        titles=[]
        for i in self.defined_actions:
            titles.append(i.type+" on "+str(len(i.cartridges))+" cartridges : "+i.comment)
        return(titles)
    def grab_data(self):
        type=self.comboBox_action.currentText()
        comment=self.lineEdit_comment.text()
        cartridges=self.grab_cartridges()
        parameters=self.grab_parameters()
        self.defined_actions[self.current_action].set(type,comment,cartridges,parameters)
    def grab_cartridges(self):
        cartridges=[]
        for i in self.rack_left.selectedIndexes():
            cartridges.append("1"+chr(ord('A')+i.column())+str(12-i.row()))
        for i in self.rack_right.selectedIndexes():
            cartridges.append("2"+chr(ord('A')+i.column())+str(12-i.row()))
        return(cartridges)
    def remove(self,index):
        del self.defined_actions[index]
        self.update_parent()
    def edit(self,index):
        self.addmode=False
        self.current_action=index
        currentitem=self.defined_actions[index]
        self.comboBox_action.setCurrentIndex(self.comboBox_action.findText(currentitem.type))
        self.tabWidget.setCurrentIndex(self.comboBox_action.findText(currentitem.type))
        self.lineEdit_comment.setText(currentitem.comment)
        self.set_cartridges(currentitem.cartridges)
        self.set_parameters(currentitem.parameters)
    def set_cartridges(self,cartridges):
        self.unselect_both()
        for cartridge in cartridges:
            x=ord(cartridge[1])-ord('A')
            y=12-int(cartridge[2:])
            range=QtGui.QTableWidgetSelectionRange(y,x,y,x)
            if cartridge[0]=="1":
                self.rack_left.setRangeSelected(range,True)
            else:
                self.rack_right.setRangeSelected(range,True)                
    def swap(self,old,new):
        if old !=-1:
            temp=self.defined_actions[old]
            self.defined_actions[old]=self.defined_actions[new]
            self.defined_actions[new]=temp
            self.update_parent()
            self.define_parent_selection(new)
        
    def define_parent_selection(self,index):
        self.emit(QtCore.SIGNAL("select_automation_action(int)"),index)



    def grab_parameters(self):
        parameters={}

        parameters['solvent1_solvent'] = self.comboBox_solvent1.currentIndex()
        parameters['solvent2_solvent'] = self.comboBox_solvent2.currentIndex()

        parameters['solvent1_volume'] = self.spinBox_solvent1volume.value()
        parameters['solvent2_volume'] = self.spinBox_solvent2volume.value()

        parameters['solvent1_flow'] = self.spinBox_solvent1flow.value()
        parameters['solvent2_flow'] = self.spinBox_solvent2flow.value()

        parameters['dry_drytime'] = self.spinBox_drytime.value()

        parameters['i2s_cycles'] = self.spinBox_cycles_i2s.value()
        parameters['i2s_push_solvent'] = self.comboBox_pushsolvent_i2s.currentIndex()
        parameters['i2s_push_flowrate'] = self.spinBox_pushflowrate_i2s.value()
        parameters['i2s_input_flowrate'] = self.spinBox_inputflowrate_i2s.value()

        parameters['i2s_looploadvolume'] = self.spinBox_looploadvolume_i2s.value()
        parameters['i2s_loopinjectvolume'] = self.spinBox_loopinjectvolume_i2s.value()

        parameters['i2s_pause'] = self.spinBox_pause_i2s.value()
        parameters['i2s_askcycles'] = self.checkBox_askcycles_i2s.isChecked()

        parameters['output'] = self.comboBox_output.currentIndex()
        parameters['askcartridges'] = self.checkBox_askcartridges.isChecked()

        return(parameters)

    def set_parameters(self,parameters):
        self.comboBox_solvent1.setCurrentIndex(parameters['solvent1_solvent'])
        self.comboBox_solvent2.setCurrentIndex(parameters['solvent2_solvent'])

        self.spinBox_solvent1volume.setValue(parameters['solvent1_volume'])
        self.spinBox_solvent2volume.setValue(parameters['solvent2_volume'])

        self.spinBox_solvent1flow.setValue(parameters['solvent1_flow'])
        self.spinBox_solvent2flow.setValue(parameters['solvent2_flow'])

        self.spinBox_drytime.setValue(parameters['dry_drytime'])

        self.spinBox_cycles_i2s.setValue(parameters['i2s_cycles'])
        self.comboBox_pushsolvent_i2s.setCurrentIndex(parameters['i2s_push_solvent'])
        self.spinBox_pushflowrate_i2s.setValue(parameters['i2s_push_flowrate'])
        self.spinBox_inputflowrate_i2s.setValue(parameters['i2s_input_flowrate'])

        self.spinBox_looploadvolume_i2s.setValue(parameters['i2s_looploadvolume'])
        self.spinBox_loopinjectvolume_i2s.setValue(parameters['i2s_loopinjectvolume'])

        self.spinBox_pause_i2s.setValue(parameters['i2s_pause'])
        self.checkBox_askcycles_i2s.setChecked(parameters['i2s_askcycles'])

        self.comboBox_output.setCurrentIndex(parameters['output'])
        self.checkBox_askcartridges.setChecked(parameters['askcartridges'])

    
    def launch(self):
        actions=[]
        action=0
        for i in self.defined_actions:
            actions = AutomationActions.export_action(i)
            self.emit(QtCore.SIGNAL("add_action_array(PyQt_PyObject)"),["AUTOMATION:"+str(action)+"_"+i.type]+actions)
            action = action + 1
        action=0
        for i in self.defined_actions:
            self.parent.emit(QtCore.SIGNAL("start_action(QString)"),"AUTOMATION:"+str(action)+"_"+i.type)
            action = action + 1

            
