# Nextflow Analyzer
# Written by Clémence Sebe and George Marchment
# October 2021 - April 2022

from .commonFunction import * 
from .toolFunction import *

class Stub:
    def __init__(self, strStub):
            self.stub_string = strStub
            self.language = None
            self.tools = []
            self.annotations = {}

    def printString(self):
        print(self.stub_string)  
    
    def printLanguage(self):
        print(self.language)

    def getString(self):
        return self.stub_string

    def getLanguage(self):
        return self.language
    
    def getTools(self):
        return self.tools
    
    def getAnnotations(self):
        return self.annotations

    def whichLanguage(self):
        self.language = whichLanguage(self.stub_string)

    def extractTools(self):
        if self.language == 'bash':
            #work = justScript(self.stub_string)
            self.tools = get_toolnames(self.stub_string)
            self.annotations = get_info_biotools_set_of_tools_dump(self.tools)

    def extractS(self):
        self.whichLanguage()
        self.extractTools()


