import time
import serial
import array


from worker import STOPABLE, NONSTOPABLE
from pump import PumpBox # Module for handling pump requests
from prospekt import ProspektBox # Module for handling prospekt requests
from box import Box

def empty_callback(request):
    return(0)

# Serial stuff
import os
# chose an implementation, depending on os
if os.name == 'nt': #sys.platform == 'win32':
    from serial.tools.list_ports_windows import *
elif os.name == 'posix':
    from serial.tools.list_ports_posix import *
#~ elif os.name == 'java':
else:
    raise ImportError("Sorry: no implementation of serial port list for your platform ('%s') available" % (os.name,))


def convert_cartridge_position(clamp,value): # 1 : Left Clamp, 2: Right Clamp
    # abbcd   clamp,1A1=d,acb
    column="%02d"%int(value[2:])
    return(value[0]+column+str(ord(value[1])-ord('A')+1)+str(clamp))



class Communicator:
    def __init__(self,parent):
        self.initialized=True
        self.prospektbox=ProspektBox()
        self.pumpbox=PumpBox()
        self.parent=parent
    def get_comports(self):
        return comports()
    def action(self,rawaction,value):
        returncode=True
        action_splitted = rawaction.split(":")
        action=None
        module=None
        if len(action_splitted)>=1:
            module = action_splitted[0]
        if len(action_splitted)>=2:
            action = action_splitted[1]

        if module == "PROSPEKT":
            self.parent.log("DEBUG","PROSPEKT: "+str(action)+"("+str(value)+")")
            return(self.prospektbox.query(action,value))

        elif module == "PUMP":
            self.parent.log("DEBUG","PUMP: "+str(action)+"("+str(value)+")")
            return(self.pumpbox.query(action,value))
        elif module == "INTERNAL":
            if action == "WAIT":
                self.parent.log("DEBUG","INTERNAL: Sleeping for "+str(value))
                time.sleep(value)
            if action == "WAITUSER":
                self.parent.waituser(value)
            if action == "STOPABLE":
                self.parent.log("DEBUG","Unsetting nonstopable flag")
                self.parent.state=STOPABLE
            if action == "NONSTOPABLE":
                self.parent.log("DEBUG","Setting nonstopable flag")
                self.parent.state=NONSTOPABLE
            return([True,True])
        else:
            self.parent.log("ERROR","Communicator : unknown module "+module)
            return([None,None])
