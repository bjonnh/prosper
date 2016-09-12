import time
import prosper_common
from collections import deque

from PyQt4 import QtCore


STOPABLE=0
NONSTOPABLE=1

class Worker(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False

        self.rawreturnvalue=None
        self.communicator=prosper_common.Communicator(self)
        self.queue=deque([])
        self.initialized=True
        self.state=STOPABLE
        self.needclear=False
        self.parent=parent
    def __del__(self):
        self.exiting = True
        self.wait()
    def log(self,typeof,msg):
        self.emit(QtCore.SIGNAL("log(QString,QString)"),typeof,msg)
    def waituser(self,msg):
        self.emit(QtCore.SIGNAL("waituser(QString)"),msg)
    def get_rawreturn_value(self):
        return(self.rawreturnvalue)
    def run(self):

        if self.needclear==True:
            self.clearqueue()
        if len(self.queue)!=0:
            couple = self.queue.popleft()
            action=couple[0]
            value=couple[1]
            globalaction=couple[2]

            while(self.parent.waitingforuser==True):
                time.sleep(0.1)
            self.log("WARNING","Launching "+action + " with value "+str(value))
            (self.returncode,self.returnvalue) = self.communicator.action(action,value)
            self.emit(QtCore.SIGNAL("sizeofqueue(int)"),len(self.queue))
            self.emit(QtCore.SIGNAL("donesignal(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)"),self.returncode,action,self.returnvalue)

            self.run()
    def actionstart(self,action,value=None):
        if action!=None and action!=False:
            self.action = action

            current_action = action.nextaction(value)     
            while current_action != False:
                self.queue.append(current_action+[action])

                current_action = action.nextaction(value)     
            if self.isRunning():
                return(0)
            else:
                self.start()
                return(1)
        else:
            return(1)
    def clearqueue(self):
        if self.state==STOPABLE:
            self.log("DEBUG","Queue is stopable")
            self.needclear=False
            self._clearqueue()
        else:
            self.log("DEBUG","Queue is not stopable setting needclean flag")
            self.needclear=True
    def _clearqueue(self):
        print("Cleaning queue")
        self.emit(QtCore.SIGNAL("sizeofqueue(int)"),len(self.queue))
        self.queue.clear()
    def panic(self):
        self._clearqueue()
        self.terminate()
        self.wait()

