# Nextflow Analyzer
# Written by Clémence Sebe and George Marchment
# October 2021 - April 2022


from .commonFunction import *
from .toolFunction import *

class Script:
    def __init__(self, strScript):
            self.script_string = strScript
            self.language = None
            self.tools = []
            self.annotations = {}
            self.listTools  = []
            self.listToolsUrl = []
            self.listAnnotationsTools = []

    def printString(self):
        print(self.script_string)  
    
    def printLanguage(self):
        print(self.language)

    def getString(self):
        return self.script_string

    def getLanguage(self):
        return self.language
    
    def getTools(self):
        return self.tools
    
    def getAnnotations(self):
        return self.annotations
    
    def getListTools(self):
        if(self.listTools!=None):
            return self.listTools
        return []

    def getListToolsUrl(self):
        if(self.listToolsUrl!=None):
            return self.listToolsUrl
        return []
    
    def getListAnnotationsTools(self):
        if(self.listAnnotationsTools!=None):
            return self.listAnnotationsTools
        return []



    def whichLanguage(self):
        self.language = whichLanguage(self.script_string)

    def extractTools(self):
        if self.language == 'bash':
            #work = justScript(self.script_string)
            self.tools = get_toolnames(self.script_string)
            self.annotations = get_info_biotools_set_of_tools_dump(self.tools)

            #Add in a list - the tool name
            for a in self.annotations:
                bioId = self.annotations[a]['name']
                if not bioId in self.listTools:
                    self.listTools.append(bioId)
                    self.listToolsUrl.append(self.annotations[a]['uri'])
                    self.listAnnotationsTools.append(self.annotations[a])
                    #print(self.annotations[a])
                         
    def extractS(self):
        self.whichLanguage()
        self.extractTools()
