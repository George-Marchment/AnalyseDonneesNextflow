from process import *
from commonFunction import *
import re
"""
FIRST PART
""" 
keyWordsO = ['val', 'env', 'file', 'path', 'stdout', 'tuple', 'set']

listPatternO = []
for words in keyWordsO:
    string = "([^,]\\n+\\s*" + words + "[^a-zA-Z0-9])"
    listPatternO.append(string)

listPatternOb = []
for words in keyWordsO:
    string = "(" + words + "(\s|\(|\{|\[)\w+)"
    listPatternOb.append(string)

"""
SECOND PART - Class
"""
class Outputs:
    def __init__(self, strOutput):
        self.output_string = strOutput
        self.list_output = []
        self.list_qualifier = []
        self.list_words_workflow = []
        self.list_emit = []
        self.temp = []

    def printOutput(self):
        print(self.output_string)

    def printListOutput(self):
        for string in self.list_output:
            print(string)

    def numberOutputs(self):
        return len(self.list_output)

    def getQualifier(self):
        return self.list_qualifier
    
    def getOutputs(self):
        return self.list_output
    
    def getNameInWorkflow(self):
        return self.list_words_workflow

    def getEmit(self):
        return self.list_emit
        
    def splitOutput(self):
        self.list_output = split(listPatternO, self.output_string)
    
    def extractQualifier(self):
        self.list_qualifier = extractQ(self.list_output)
    
    def extractName(self):
        #Two Cases : 
        pattern = r'(\sinto\s((\w+\s*,?\s*))*)'
        for idx in range(len(self.temp)):
            start = -1 
            for match in re.finditer(pattern, self.temp[idx]):
                start = match.span()[0] + len("into") +1
                end = match.span()[1]
                work = self.temp[idx][start:end].lstrip().rstrip()
            #Precence of "into"
            if start >=0:
                comma = r'(,)'
                placeComma = []
                for match in re.finditer(comma,work):
                    placeComma.append(match.span())
                if len(placeComma) == 0:
                    endWord = r'($|\s)'
                    end = len(work)+1
                    for match in re.finditer(endWord, work):
                        if match.span()[0] < end:
                            end = match.span()[0]
                    string = work[:end].lstrip().rstrip()
                    self.list_words_workflow.append([idx,string])
                else:
                    placeComma.sort()
                    for i in range (len(placeComma)):
                        if i == 0:
                            string = work[0:placeComma[i][0]].lstrip().rstrip()
                        elif i == len(placeComma)-1:
                            string = work[placeComma[i-1][1]:placeComma[i][0]].lstrip().rstrip()
                            self.list_words_workflow.append([idx,string])
                            string = work[placeComma[i][1]:].lstrip().rstrip()
                        else:
                            string = work[placeComma[i-1][1]:placeComma[i][0]].lstrip().rstrip()
                        self.list_words_workflow.append([idx,string])
            #Without "into"
            else:
                startb = -1
                for i in range(len(listPatternOb)):
                    pat = listPatternOb[i]
                    for match in re.finditer(pat,self.temp[idx]):
                        startb = match.span()[0] + len(keyWordsO[i]) + 1
                        endb = match.span()[1]
                    if startb >=0:
                        string = self.temp[idx][startb:endb].lstrip().rstrip()
                        if string[0].isalpha():
                            self.list_words_workflow.append([idx,string])
                        else:
                            self.list_words_workflow.append([idx,string[1:]])
                        break


    def extractEmit(self):
        patEmit = r'(emit\s*:\s*\w+)'
        containEmit = []
        for idx in range (len(self.list_output)):
            for match in re.finditer(patEmit, self.list_output[idx]):
                start = match.span()[0] 
                end = match.span()[1]
                work = self.list_output[idx][start:end]
                pat = r'(emit\s*:)'
                for match in re.finditer(pat, work):
                    startb = match.span()[1]
                emit = work[startb:].lstrip().rstrip()
                self.list_emit.append([idx,emit])
                containEmit.append(idx)
        
        #Create self.temp to work on extractName in all the process except the ouptut with emit 
        for i in range (len(self.list_output)):
            if not (i in containEmit):
                self.temp.append(self.list_output[i])

    def extractO(self):
        self.splitOutput()
        self.extractQualifier()
        self.extractEmit()
        self.extractName()
    
if __name__ == "__main__":
    print("I shouldn't be executed as a main")
