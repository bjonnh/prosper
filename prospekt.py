import array
from box import Box

class ProspektQuery:
    def __init__(self,query,need152):
        self.query=query
        self.need152=need152

class ProspektBox(Box):
    def __init__(self):
        Box.__init__(self)
        self.codes_false=[0x15,0x18,0x24]
        self.end_codes=[0x3,0x6,0x18,0x15]
    def set_query_code(self,rawquerycode):
        self.querycode = rawquerycode
    def text2binary(self,data):
        if len(data)!=1: # It's a complex request
            request=[0x2]
            for char in data:
                if char not in ["-"]: # Removing decoration chars
                    request.append(ord(char))
            request.append(0x3)
            return(request)
        else: # It's just a return code
            return(data) 
    def get_query_value(self,query): # Get the value from the request
        queryval=array.array('B', query[9:15]).tostring().decode()
        if(queryval==''):
            queryval=-1
        return(int(queryval))
    def modulequery(self,action,value):
        self._query(action,value)
        self.querycode=None
        query=self.request(action,value) # Get the corresponding request code for action
        if query !=None: # If the query is known
            self.write_and_wait(query.query,answer_callback=self.set_rawreturncode)
            self.treatanswer(self.rawreturncode)
            if self.rawreturncode != None:
                self.returnvalue=self.get_query_value(self.rawreturncode)

            if (query.need152 == True) and self.treatedanswer == True: # This query needs a 152 type answer
                return152=-1;
                while return152!=0:
                    query152=self.request("IS_READY",query)
                    self.write_and_wait(query152.query,answer_callback=self.set_query_code)
                    return152=self.get_query_value(self.querycode)

        self.returncode=True
        return([self.returncode,self.returnvalue])

    def request(self,name,_value=None):
        """Construct the requests"""
        if _value !=None:
            try:
                value=int(_value)
            except:
                value=_value
        else:
            value=None

        if name == "ACE_TRAY_UNLOAD":
            return(ProspektQuery("30012120000021",True))
        elif name == "ACE_TRAY_LOAD":
            return(ProspektQuery("30012137000001",True))
        elif name == "ACE_PANIC":
            return(ProspektQuery("30010156000001",True))
        elif name == "HPD_PANIC":
            return(ProspektQuery("35010156000001",True))


        elif name == "ACE_VALVE1_SET":
            return(ProspektQuery("3001211200000"+str(value),True))
        elif name == "ACE_VALVE1_GET":
            return(ProspektQuery("30011001002112",False))
        elif name == "ACE_VALVE2_SET":
            return(ProspektQuery("3001510600000"+str(value),True))
        elif name == "ACE_VALVE2_GET":
            return(ProspektQuery("30011001005106",False))
        elif name == "ACE_VALVE3_SET":
            return(ProspektQuery("3001210200000"+str(value),True))
        elif name == "ACE_VALVE3_GET":
            return(ProspektQuery("30011001002102",False))
        elif name == "ACE_VALVE4_SET":
            return(ProspektQuery("3001219000000"+str(value),True))
        elif name == "ACE_VALVE4_GET":
            return(ProspektQuery("30011001002190",False))


        elif name == "ACE_GRIPPER":
            return(ProspektQuery("3501212700000"+str(value),True))

        elif name == "ACE_L_INIT":
            return(ProspektQuery("30012110000001",True))
        elif name == "ACE_L_DEFAULT":
            return(ProspektQuery("30012110000000",True))
        elif name == "ACE_L_OPEN":
            return(ProspektQuery("30012111000001",True))
        elif name == "ACE_L_CLOSE":
            return(ProspektQuery("30012111000000",True))
        elif name == "ACE_R_INIT":
            return(ProspektQuery("30012100000001",True))
        elif name == "ACE_R_DEFAULT":
            return(ProspektQuery("30012100000000",True))
        elif name == "ACE_R_OPEN":
            return(ProspektQuery("30012101000001",True))
        elif name == "ACE_R_CLOSE":
            return(ProspektQuery("30012101000000",True))
        elif name == "ACE_L_CLAMP_GET":
            return(ProspektQuery("30011001002110",False))
        elif name == "ACE_R_CLAMP_GET":
            return(ProspektQuery("30011001002100",False))

        elif name == "ACE_GETBACK":
            return(ProspektQuery("30012205000001",True))
        elif name == "ACE_PUT":
            return(ProspektQuery("300121220%05d"%value,True))
        elif name == "ACE_BACK":
            return(ProspektQuery("300121230%05d" % value,True))
        elif name == "ACE_OUT_SET":
            (out,val)=value.split("=")
            return(ProspektQuery("3001016"+out+"00" + val,False))
        elif name == "ACE_OUT_GET":
            return(ProspektQuery("30011001000160",False))
        elif name == "ACE_IN_GET": 
            return(ProspektQuery("30011001000169",False))

        elif name == "HPD_VALVEL_SET":
            return(ProspektQuery("3501200000000"+str(value),True))
        elif name == "HPD_VALVEL_GET":
            return(ProspektQuery("35011001002000",False))
        elif name == "HPD_VALVER_SET":
            return(ProspektQuery("3501202000000"+str(value),True))
        elif name == "HPD_VALVER_GET":
            return(ProspektQuery("35011001002020",False))
        elif name == "HPD_L_PRESSURE_GET":
            return(ProspektQuery("35011001002010",False))
        elif name == "HPD_R_PRESSURE_GET":
            return(ProspektQuery("35011001002030",False))

        elif name == "HPD_L_SYRVOL_GET":
            return(ProspektQuery("35011000002009",False))
        elif name == "HPD_R_SYRVOL_GET":
            return(ProspektQuery("35011000002029",False))


        elif name == "HPD_L_ASPIRATE_SPEED_SET":
            return(ProspektQuery("350120010%05d"% value,False))
        elif name == "HPD_L_ASPIRATE_SPEED_GET":
            return(ProspektQuery("35011000002001",False))
        elif name == "HPD_L_DISPENSE_SPEED_SET":
            return(ProspektQuery("350120050%05d" % value,False))
        elif name == "HPD_L_DISPENSE_SPEED_GET":
            return(ProspektQuery("35011000002005",False))

        elif name == "HPD_R_ASPIRATE_SPEED_SET":
            return(ProspektQuery("350120210%05d"% value,False))
        elif name == "HPD_R_ASPIRATE_SPEED_GET":
            return(ProspektQuery("35011000002021",False))
        elif name == "HPD_R_DISPENSE_SPEED_SET":
            return(ProspektQuery("350120250%05d" % value,False))
        elif name == "HPD_R_DISPENSE_SPEED_GET":
            return(ProspektQuery("35011000002025",False))
        elif name == "HPD_L_ASPIRATE":
            return(ProspektQuery("3501200200%04d"% value,True))
        elif name == "HPD_L_DISPENSE":
            return(ProspektQuery("3501200600%04d"% value,True))
        elif name == "HPD_R_ASPIRATE":
            return(ProspektQuery("3501202200%04d"% value,True))
        elif name == "HPD_R_DISPENSE":
            return(ProspektQuery("3501202600%04d"% value,True))

        elif name == "HPD_L_LIMIT_SET":
            return(ProspektQuery("35012011000%03d"% value,False))
        elif name == "HPD_R_LIMIT_SET":
            return(ProspektQuery("35012031000%03d"% value,False))
        elif name == "HPD_L_LIMIT_GET":
            return(ProspektQuery("35011000002011",False))
        elif name == "HPD_R_LIMIT_GET":
            return(ProspektQuery("35011000002031",False))



        elif name == "HPD_L_VOLUME_GET":
            return(ProspektQuery("35011001002016",False))
        elif name == "HPD_R_VOLUME_GET":
            return(ProspektQuery("35011001002036",False))

        elif name == "HPD_GET_VER_MCCB":
            return(ProspektQuery("35011001000154",False))
        elif name == "HPD_GET_VER_DISPENSERL":
            return(ProspektQuery("35021001000154",False))
        elif name == "HPD_GET_VER_DISPENSERR":
            return(ProspektQuery("35031001000154",False))
        elif name == "HPD_GET_VER_SSM":
            return(ProspektQuery("35041001000154",False))
        elif name == "HPD_GET_NUM_VALVEL":
            return(ProspektQuery("35011001000607",False))
        elif name == "HPD_GET_NUM_VALVER":
            return(ProspektQuery("35011001000609",False))

        elif name == "ACE_GET_VER_MCCB":
            return(ProspektQuery("30011001000154",False))
        elif name == "ACE_GET_VER_TRANSPORT":
            return(ProspektQuery("30021001000154",False))
        elif name == "ACE_GET_VER_CLAMPL":
            return(ProspektQuery("30031001000154",False))
        elif name == "ACE_GET_VER_CLAMPR":
            return(ProspektQuery("30041001000154",False))
        elif name == "ACE_GET_VER_ISS":
            return(ProspektQuery("30051001000154",False))
        elif name == "ACE_GET_VER_RF":
            return(ProspektQuery("30061001000154",False))
        elif name == "ACE_GET_VER_TASPE":
            return(ProspektQuery("30071001000154",False))
        elif name == "ACE_GET_VER_FEEDER":
            return(ProspektQuery("30081001000154",False))
        elif name == "ACE_GET_VER_MPV":
            return(ProspektQuery("30091001000154",False))
        elif name == "ACE_GET_NUM_VALVE1":
            return(ProspektQuery("30011001000614",False))
        elif name == "ACE_GET_NUM_VALVE2":
            return(ProspektQuery("30011001000601",False))
        elif name == "ACE_GET_NUM_VALVE3":
            return(ProspektQuery("30011001000612",False))
        elif name == "ACE_GET_NUM_VALVE4":
            return(ProspektQuery("30011001000635",False))
        elif name == "ACE_GET_NUM_TRANSPORT":
            return(ProspektQuery("30011001000615",False))

        elif name == "IS_READY":
            return(ProspektQuery(value.query[0:2]+"011001000152",True))
        else:
            return(None)

