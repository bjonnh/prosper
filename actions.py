
class Action:
    def __init__(self,name,parameters=[]):
        self.pointer = 0
        self.content = []
        self.name = name
        self.parameters=parameters
        self.parameters_values={}
    def add_content(self,name,value=None):
        self.content.append([name,value])
    def nextaction(self,value=None):
        if self.pointer > len(self.content)-1:
            self.reset()
            return(False)
        else:
            returnvalue=self.currentaction(value)
            self.pointer=self.pointer+1
            return(returnvalue)
    def currentaction(self,value=None):
        current_value = self.content[self.pointer][1]  # Get the actual action value
        if value != None: # If we are giving a value
            # Checking if this is a named argument and if we have a value for it
            if current_value in self.parameters and current_value in self.parameters_values: 
                value = self.parameters_values[current_value]
            elif self.pointer>0: # Else, if we are in a macro already started
                value = current_value
        # If we are in the first part of a macro and that 
        if self.pointer==0 and self.parameters!=[] and len(self.content)>1:
            if type(value)==list:
                for i in self.parameters:
                    self.parameters_values[i]=value[self.parameters.index(i)]
            else:
                self.parameters_values[self.parameters[0]]=value

        if value == None :  # We are using the default value
            value = current_value
        return([self.content[self.pointer][0],value])
    def reset(self):
        self.pointer=0

class Actions:
    def __init__(self):
        self.actions={}

    def append(self,line):
        line_split=line.split(" -> ")
        self.append_array(line_split)
    def append_array(self,line_split):
        name_split = line_split[0].split("(")
        if len(name_split)>1:
            parameters=name_split[1].rstrip(")").split(",")
        else:
            parameters=[]
        macro_name = name_split[0]
        print("Adding "+str(line_split))
        # Creating the action
        self.actions[macro_name]=Action(macro_name,parameters=parameters)
        # Adding the first element
        self.actions[macro_name].add_content(macro_name)

        # We have a macro
        if len(line_split)>1:

            for element in line_split[1:]:
                element_split=element.split("(")
                element_name = element_split[0]
                element_value = None
                # Element has parameters
                if len(element_split)>1:
                    element_value=element_split[1].rstrip(")")
                if element_name in self.actions:
                    self.actions[macro_name].add_content(element_name,element_value)
                    if len(self.actions[element_name].content) > 1:
                        for data in self.actions[element_name].content[1:]:
                            self.actions[macro_name].add_content(data[0],data[1])
                else:
                    self.actions[macro_name].add_content(element_name,element_value)
        return(True)

    def Get(self,name):
        if name in self.actions:
            return(self.actions[name])
        else:
            return(False)
