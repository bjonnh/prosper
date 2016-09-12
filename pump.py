from box import Box
import array

class PumpQuery:
    def __init__(self,query):
        self.query=query

class PumpBox(Box):
    def __init__(self):
        Box.__init__(self)
        self.codes_false=["?\x0d"]
        self.end_codes=[0x0d]
    def text2binary(self,data):
        request=[]
        for char in data:
            request.append(ord(char))
#        request.append(10)
        request.append(13)
        return(request)
    def get_query_value(self,query): # Get the value from the request
        queryval=array.array('B', query).tostring().decode()
        if queryval[0]=="F":
            return(float(queryval[1:])*1000)
        if(queryval=='' or queryval[0:2]=="OK" or queryval[0:1]=="?"):
            queryval=-1
        return(int(queryval))

    def modulequery(self,action,value=None):
        self._query(action,value)
        self.returncode=True
        query=self.request(action,value)
        if query !=None:
            self.write_and_wait(query.query,answer_callback=self.set_rawreturncode)
        self.treatanswer(self.rawreturncode)
        self.returnvalue=self.get_query_value(self.rawreturncode)
        return([self.returncode,self.returnvalue])
    def request(self,action,value):
        if action=="ON":
            return(PumpQuery("M1"))
        elif action=="OFF":
            return(PumpQuery("M0"))
        elif action=="FLOW_SET":
            return(PumpQuery("F"+str(value)))
        elif action=="STATE_GET":
            return(PumpQuery("S?"))
        elif action=="FLOW_GET":
            return(PumpQuery("F?"))
        else:
            return(None)
        
