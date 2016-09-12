import serial
import time

class Box:
    fd=None
    def __init__(self):
        self.port=None
        self.speed=9600
        self.timeout=1
        self.connected=False
        self.clean_codes()
        self.codes_false=None
        self.end_codes=None

    def set_rawreturncode(self,code):
        """ Get the answer and put it in self.rawreturncode """
        self.rawreturncode=code
    def treatanswer(self,code):

        if code[0] in self.codes_false or code in self.codes_false:
            # Should raise an error ?
            self.treatedanswer=False
        else:
            self.treatedanswer=True
        return(self.treatedanswer)
    def _query(self,action,value):
        self.clean_codes()
    def clean_codes(self):
        self.rawreturncode=None
        self.treatedanswer=None
        self.returnvalue=None
    def set_port(self,port):
        self.port=port
    def open(self):
        self.fd = serial.Serial(self.port,self.speed,timeout=self.timeout)
        self.connected=True
        self.read(self.isdatawaiting())
    def close(self):
        self.fd.close()
        self.connected=False
    def isdatawaiting(self):
        return self.fd.inWaiting()
    def read(self,size=1):
        return self.fd.read(size)
    def write(self,data):
        return self.fd.write(bytearray(data))
    def write_request(self,data):
        self.write(self.text2binary(data))
    def wait_request(self,answer_callback):
        if answer_callback==None:
            answer_callback=self.empty_callback
            print("ERROR: Empty CallBack for Box request")

        received_request=[]
        end=False
        while end==False:
            while self.isdatawaiting() == 0:
                time.sleep(0.05)
            
            out=self.read(1)
            received_request.append(ord(out))
            if ord(out) in self.end_codes: 
                answer_callback(received_request)
                end=True
    def write_and_wait(self,data,answer_callback):
        self.write_request(data)
        self.wait_request(answer_callback=answer_callback)
    def modulequery(self,action,value):
        return([True,True])
    def query(self,action,value):
        if action=="CONNECT":
            self.port=value
            self.open()
            return([True,True])
        elif action=="DISCONNECT":
            self.close()
            return([True,True])
        elif self.connected==True:
            return(self.modulequery(action,value))
        else:
            print("ERROR: Module not connected")


# Used to debug serial protocol
#
#                a=serial.to_bytes(received_request).decode()  # Array of ascii codes to string
#                for i in received_request:
#                    a=a+chr(i)
#                print("Receive: "+a)
