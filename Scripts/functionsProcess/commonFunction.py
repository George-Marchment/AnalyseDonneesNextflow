import re
"""
This file contains all the functions which could be use in different Class
"""

"""
DIRECTIVE - INPUT - OUTPUT
"""

"""
Clean an element : no \n and no \
"""
def clean(txt):
    antiSlash = []
    for match in re.finditer(r"(\\)", txt):
        antiSlash.append(match.span())
    antiSlash.sort(reverse = True)
    for j in range(len(antiSlash)):
        txt = txt.replace(txt[antiSlash[j][0]:antiSlash[j][1]], " ")
    txt =" ".join(txt.split())
    return txt

"""
Split 
"""
def split(lists, txt):
    listEnd = []
    work = "a \n" + txt
    index = []
    for pattern in lists:
        for match in re.finditer(pattern, work):
            index.append(match.span()[0]+1)
    index.sort()
    for i in range (len(index)):
        if i == len(index)-1:
            study = work[index[i]:].lstrip().rstrip()
        else:   
            study = work[index[i]:index[i+1]].lstrip().rstrip()
        study = clean(study)
        listEnd.append(study)
    return listEnd

"""
Extract 
"""
def extractQ(txt):
    listEnd = []
    for i in range (len(txt)):
        cut = re.split("[^\w]",txt[i])
        key = cut[0] 
        listEnd.append([i,key])
    return listEnd


"""
SCRIPT - STUB
"""
"""
Analyse Language
"""
def whichLanguage(txt):
    language =""
    pattern = r'(#!/)'
    start = -1
    nb = -1
    for match in re.finditer(pattern, txt):
        start = match.span()[0]
        nb = 1
    if nb < 0:
        language = 'bash'
    else:
        patternEnd = r'(\n)'
        end = len(txt)
        for match in re.finditer(patternEnd, txt):
            if match.span()[0] < end and match.span()[0] > start:
                end = match.span()[0]
        work =txt[start:end].lstrip().rstrip()
        test1 = work.split()
        if len(test1) > 1:
            language = test1[-1]
        else:
            test2 = work.split('/')
            language = test2[-1]
    return language

"""
Prepare the string for the extraction of tools after
"""
import re
def justScript(txt):
    study = ''
    work = '\n' + txt + '\n'

    #Verify that the script is not empty:
    empty = True
    for char in txt:
        if char.isalpha():
            empty = False
    if not empty:
        #First delete comment : 
        patComment =  r'(s*\t*#.*\n)'
        tabIdx = []
        for match in re.finditer(patComment, work):
            tabIdx.append([match.span()[0],match.span()[1]])
        tabIdx.sort(reverse=True)
        for idx in tabIdx:
            work = work.replace(work[idx[0]:idx[1]].strip(), "\n")
                
        patLong = [r"(\n+\s*'''\n*)", r'(\n+\s*"""\n*)']
        tabIdx = []
        for pat in patLong:
            for match in re.finditer(pat, work):
                tabIdx.append([match.span()[0], match.span()[1]])
        tabIdx.sort()
        for i in range (0, len(tabIdx),2):
            study += work[tabIdx[i][1]:tabIdx[i+1][0]] + "\n"
        #clean work
        tabIdx.sort(reverse= True)
        for i in range (0, len(tabIdx),2):
            work = work.replace(work[tabIdx[i+1][0]:tabIdx[i][1]], "\n")

        #Short - one line
        pattern = [r'(\n+\s*".*"\n*)', r"(\n+\s*'.*'\n*)"]
        for pat in pattern:
            for match in re.finditer(pat,work):
                #enlever les " " ou ' '                
                temp = work[match.span()[0]: match.span()[1]].lstrip().rstrip()
                study += "\n" + temp[1:-1]
    return study