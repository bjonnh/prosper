
###
# Simulation part
###

import prosper_common

class Module:
    def __init__(self,name):
        self.name=name
    def treat_request(self,request):
        return([0x6])

class HPD(Module):
    def __init__(self,name):
        Module.__init__(self,name)
        self.ready=True
        self.vhpdl=1
        self.vhpdr=1
        self.error=False
        self.hpdl_syringuevolume=2000
        self.hpdl_aspiratespeed=4000
        self.hpdl_dispensespeed=4000
        self.hpdl_aspiratevolume=0
        self.hpdl_dispensevolume=0
        self.hpdl_currentvolume=0
        self.hpdl_pressurelimit=300

        self.hpdr_syringuevolume=2000
        self.hpdr_aspiratespeed=4000
        self.hpdr_dispensespeed=4000
        self.hpdr_aspiratevolume=0
        self.hpdr_dispensevolume=0
        self.hpdr_currentvolume=0
        self.hpdr_pressurelimit=300

    def treat_request(self,request):
        answer=None
#        if request[2:6] !="1001" and request[2:6] != "1000":
#            print("HPD Request: "+request)
        if request[0:6]=="010000":

            if request[6:14]=="-000001":
                answer=[0x15]
        if request[0:6]=="011000": # Information request
            if request[6:13]=="002011": # L presure limit
                answer="35012011   %03d" % self.hpdl_pressurelimit
            if request[6:13]=="002031": # R presure limit
                answer="35012031   %03d" % self.hpdr_pressurelimit
            if request[6:13]=="002009": # L syringue volume
                answer="35012009  %04d" % self.hpdl_syringuevolume
            if request[6:13]=="002029": # R syringue volume
                answer="35012029  %04d" % self.hpdr_syringuevolume
            if request[6:13]=="002001": # L Aspirate_speed
                answer="35012001 %05d" % self.hpdl_aspiratespeed
            if request[6:13]=="002021": # R Aspirate_speed
                answer="35012021 %05d" % self.hpdr_aspiratespeed
            if request[6:13]=="002005": # L Dispense_speed
                answer="35012001 %05d" % self.hpdl_dispensespeed
            if request[6:13]=="002025": # R Dispense_speed
                answer="35012021 %05d" % self.hpdr_dispensespeed
        if request[0:6]=="011001": # Information request

            if request[6:13]=="000152": # Module state
                if self.ready==True:
                    if self.error==True:
                        answer="35010152001002"
                    else:
                        answer="35010152000000"
                        self.error=False
                else:
                    answer="35010152000042"
            if request[6:13]=="000155": # Module error state
                answer="35010155000450"
            if request[6:13]=="000156": # Module error state
                answer="35010156000000"
            if request[6:13]=="000158": # Module version ???
                answer="35010158000011"
            if request[6:13]=="000159": # Module version ???
                answer="35010159     2"
            if request[6:13]=="000607": # Counter HPD-L
                answer="35010607000100"
            if request[6:13]=="000609": # Counter HPD-R
                answer="35010609000100"
            if request[6:13]=="002000": # HPD-L Valve
                answer="3501200000000"+str(self.vhpdl)
            if request[6:13]=="002020": # HPD-R Valve
                answer="3501202000000"+str(self.vhpdr)
            if request[6:13]=="002016": # HPD-L Current volume
                answer="3501201600%04d" % self.hpdl_currentvolume
            if request[6:13]=="002036": # HPD-R Current volume
                answer="3501203600%04d" % self.hpdr_currentvolume
            if request[6:13]=="002010": # HPD-L Current Pressure
                answer="35012010000000"
            if request[6:13]=="002030": # HPD-R Current Pressure
                answer="35012030000000"

        elif request[0:6]=="015100": # Init
            answer=[0x6]
        elif request[0:6]=="012000": # Set HPD-L valve
            self.error=True
            self.vhpdl = request[11:12]
            answer=[0x6]
        elif request[0:6]=="012020": # Set HPD-R valve
            self.vhpdr = request[11:12]
            answer=[0x6]

        elif request[0:6]=="012001": # Set HPD-L aspirate speed
            self.hpdl_aspiratespeed = int(request[8:12])
            answer=[0x6]
        elif request[0:6]=="012002": # Set HPD-L aspirate volume

            self.hpdl_aspiratevolume = int(request[8:12])
            self.hpdl_currentvolume = self.hpdl_currentvolume + self.hpdl_aspiratevolume
            if self.hpdl_currentvolume > self.hpdl_syringuevolume :
                self.hpdl_currentvolume = self.hpdl_syringuevolume
            answer=[0x6]
        elif request[0:6]=="012005": # Set HPD-L dispense speed
            self.hpdl_dispensespeed = int(request[8:12])
            answer=[0x6]
        elif request[0:6]=="012006": # Set HPD-L dispense volume
            self.hpdl_dispensevolume = int(request[8:12])
            self.hpdl_currentvolume = self.hpdl_currentvolume - self.hpdl_dispensevolume
            if self.hpdl_currentvolume < 0 :
                self.hpdl_currentvolume = 0
            answer=[0x6]
        elif request[0:6]=="012011": # Set HPD-L pressure limit
            self.hpdl_pressurelimit = int(request[9:12])
            answer=[0x6]

        elif request[0:6]=="012021": # Set HPD-R aspirate speed
            self.hpdr_aspiratespeed = int(request[8:12])
            answer=[0x6]
        elif request[0:6]=="012022": # Set HPD-R aspirate volume
            self.hpdr_aspiratevolume = int(request[8:12])
            self.hpdr_currentvolume = self.hpdr_currentvolume + self.hpdr_aspiratevolume
            if self.hpdr_currentvolume > self.hpdr_syringuevolume :
                self.hpdr_currentvolume = self.hpdr_syringuevolume
            answer=[0x6]
        elif request[0:6]=="012025": # Set HPD-R dispense speed
            self.hpdr_dispensespeed = int(request[8:12])
            answer=[0x6]
        elif request[0:6]=="012026": # Set HPD-R dispense volume
            self.hpdr_dispensevolume = int(request[8:12])
            self.hpdr_currentvolume = self.hpdr_currentvolume - self.hpdr_dispensevolume
            if self.hpdr_currentvolume < 0 :
                self.hpdr_currentvolume = 0
            answer=[0x6]
        elif request[0:6]=="012031": # Set HPD-R pressure limit
            self.hpdr_pressurelimit = int(request[9:12])
            answer=[0x6]
        elif request[0:6]=="010156": # Resume error
            answer=[0x6]
            self.error=False

        if answer==None:
            print("Unknown HPD request "+str(request))
            answer=[0x6]
#        else:
 #           print("HPD request "+str(request))
        return(answer)
class ACE(Module):
    def __init__(self,name):
        Module.__init__(self,name)
        self.ready=True
        self.watchdog=1
        self.outputs=[0,0,0,0]
        self.vbnmi=0
        self.vclamp=0
        self.vprobe=0
        self.vhpd=1
        self.tray=0
        self.clampl=1
        self.clampr=1
        self.n2=1
        self.error=False
    def treat_request(self,request):
        answer=None
#        if request[2:6] !="1001":
#            print("ACE Request: "+request)
        if request[2:12]=="1001002130": # RFID L code rack
            answer = "30"+request[0:2]+"2130000001"
        elif request[2:12]=="1001002133": # RFID R code rack
            answer = "30"+request[0:2]+"2133000000"
        elif request[2:12]=="1001002172": # RFID L (passage des cartouches)
            answer = "30%02d2172000100" % int(request[0:2],16) 
        elif request[2:12]=="1001002173": # RFID R (passage des cartouches)
            answer = "30%02d2173000110" % int(request[0:2],16)

        elif request[0:6]=="011001": # Information request
            
            if request[6:13]=="000152": # Module state
                if self.ready==True:
                    if self.error==True:
                        answer="30010152001002"
                    else:
                        answer="30010152000000"
                else:
                    answer="30010152000042"

            elif request[6:13]=="000158": # Module identifier
                answer="30010158133100" 
            elif request[6:13]=="000159": # Module identifier
                answer="30010159     1"
            
            elif request[6:13]=="000635": # Module counter valve 4
                answer="30010635001224"
            elif request[6:13]=="000612": # Module counter valve 3
                answer="30010612000041"
            elif request[6:13]=="000614": # Module counter valve 1
                answer="30010614000111"
            elif request[6:13]=="000615": # Module counter Transport
                answer="30010615001823"
            elif request[6:13]=="000601": # Module counter valve 2
                answer="30010601000338"

            elif request[6:13]=="002112": # BNMI Valve
                answer="30012112     "+str(self.vbnmi)
            elif request[6:13]=="005106": # Clamp Valve
                answer="30015106     "+str(self.vclamp)
            elif request[6:13]=="002102": # Probe Valve
                answer="30012102     "+str(self.vprobe)
            elif request[6:13]=="002190": # HPD Valve
                answer="30012190     "+str(self.vhpd)

            elif request[6:13]=="000169": # Input (all are common on Bruker SPE)  0 darkgreen 1 green 2 red
                answer="30010169     "+str(self.n2)

            elif request[6:13]=="002110": # Clamp-L state 1 non init
                answer="30012110     "+str(self.clampl)
            elif request[6:13]=="002100": # Clamp-R state 1 non init
                answer="30012100     "+str(self.clampr)

            elif request[6:13]=="002200": # Cartridge in Clamp-L
                answer="30012200000109"
            elif request[6:13]=="002201": # Cartridge in Clamp-R
                answer="30012201000110"

            elif request[6:13]=="002132": # Left Rack type
                answer="30012132050056"
            elif request[6:13]=="002135": # Right Rack type
                answer="30012135050065"



            elif request[6:13]=="000160": # Get outputs ( Spare, BGH, BLG, Dry)
                answer="30010160  "+str(self.outputs[3])+str(self.outputs[2])+str(self.outputs[1])+str(self.outputs[0])
 
            elif request[6:13]=="002182": # Unknown
                answer=[0x15]
            else: 
                print("Unknown request : "+str(request))
                answer=[0x15]

        elif request[0:5]=="01016": # Change output
            self.outputs[int(request[5])-1]=request[-1]
            
            answer=[0x6]


        elif request[0:12]=="012120000021": # Tray unload
            self.tray=0
            answer=[0x6]
        elif request[0:12]=="012137000001": # Tray load
            self.tray=1
            answer=[0x6]
        elif request[0:6]=="012112": # Set BNMI valve
            self.vbnmi = request[11:12]
            answer=[0x6]
        elif request[0:6]=="015106": # Set Clamp valve
            self.vclamp = request[11:12]
            answer=[0x6]
        elif request[0:6]=="012102": # Set Probe valve
            self.vprobe = request[11:12]
            answer=[0x6]
        elif request[0:6]=="012190": # Set HPD valve
            self.vhpd = request[11:12]
            answer=[0x6]

        elif request[0:12]=="012110000001": # Clamp-L Initial
            self.clampl=3
            answer=[0x6]
        elif request[0:12]=="012110000000": # Clamp-L Default
            self.clampl=1
            answer=[0x6]
        elif request[0:12]=="012111000000": # Clamp-L Close
            self.clampl=5
            answer=[0x6]
        elif request[0:12]=="012111000001": # Clamp-L Open
            self.clampl=3
            answer=[0x6]


        elif request[0:12]=="012100000001": # Clamp-R Initial
            self.clampr=3
            answer=[0x6]
        elif request[0:12]=="012100000000": # Clamp-R Default
            self.clampr=1
            answer=[0x6]
        elif request[0:12]=="012101000000": # Clamp-R Close
            self.clampr=5
            answer=[0x6]
        elif request[0:12]=="012101000001": # Clamp-R Open
            self.clampr=3
            answer=[0x6]

        elif request[0:6]=="012122": # Load cartridge
#XXX
            answer=[0x6]
        elif request[0:6]=="012123": # Unload cartridge
#XXX
            answer=[0x6]

        elif request[0:6]=="012127": # Move gripper 1=L 2=R
#XXX
            print("Move gripper!")
            answer=[0x6]



        elif request[0:12]=="012205000001": # Cartridges back to tray
#XXX
            answer=[0x6]

        elif request[0:6]=="010160": # Pre-Init ACE?
            answer=[0x6]
        elif request[0:6]=="015100": # Init
            answer=[0x6]
        elif request[0:6]=="010156": # Resume error
            answer=[0x6]
            self.error=False

        else:
            print("Unknown ACE request "+str(request))
            answer=[0x6]
#        else:
 #           print("ACE request "+str(request)+" -> "+str(answer))
        return(answer)

class Simulator:
    box = None
    hpd=HPD("HPD")
    ace=ACE("ACE")
    def set_box(self,box):
        self.box = box
    def translate_request(self,request):
        tr_request=""
        for char in request:
            if char!=2 and char!=3:
                tr_request = tr_request + chr(char)
        return(tr_request)
            
    def answering_machine(self,request):
        answer=None # non géré
#12345678901234

#30011001002130
        # Versions
        # 3001: MCCB , 3002: Transport module, 3003: ClampL-Module, 3004: ClampL-Module, 3005: ISS module, 3006: RF module, 3007: TASPE, 3008: Feeder, 3009: MPV
        # 3501: MCCB , 3502: DispenserL, 3503: DispenserR, 3504: SSM
        code154= {"3001":42,"3002":42,"3003":42,"3004":42,"3005":42,"3006":42,"3007":42,"3008":42,"3009":42,"3501":42,"3502":42,"3503":42,"3504":42}

        # detect the request type
        tr_request = self.translate_request(request)

        if tr_request[4:14]=="1001000154": # Fake versions
            answer = tr_request[0:4]+"0154000%03d" % code154[tr_request[0:4]]
        elif tr_request[0:2]=="30":
            answer = self.ace.treat_request(tr_request[2:])
#            print(tr_request)
        elif tr_request[0:2]=="35":
            answer = self.hpd.treat_request(tr_request[2:])
        if answer==None:
            print("Unknown request: "+tr_request)
            answer=[0x6]

        self.box.write_request(answer)
