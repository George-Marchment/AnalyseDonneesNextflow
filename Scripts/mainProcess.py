from process import *
from helpPrint import *
import matplotlib.pyplot as plt
import os
import glob

if __name__ == "__main__":
    print("-----------------------------START-----------------------------")
    #"""
    path = "/home/clemence/FAC/Master/M1/S1/TER/AnalyseDonneesNextflow/Workflows/Tuto_Nextflow/bddProcess"+"/**/*.txt"
    bddProcess = glob.glob(path, recursive= True)
    print("Taille de la bdd :", len(bddProcess))
    currentPath = os.getcwd() 

    languageScript = {}
    keyword = {'directives':0, 'input':0, 'output':0, 'when':0, 'script':0, 'stub':0}
    faute = 0
    for i in range (len(bddProcess)):
        try:
            print("******************************************")
            f = open(bddProcess[i],"r")
            process = f.read()
            p = Process(process) 
            p.extractProcess()
            inputs, outputs, emit = p.extractAll()
            print("FILE : ", bddProcess[i])
            #print(p.script.tools)
            print("Emit : ", emit)

            #print(p.script.annotations)
            print("Inputs: ", inputs)
            print("Outputs: ",outputs)
            #print(p.script.script_string)
            informations = p.getAll()
            for part, k in zip(informations[1:], keyword):
                if part != None:
                    keyword[k] += 1
                if k == 'script':
                    l = part.getLanguage()
                    if l in languageScript:
                        languageScript[l] +=1
                    else:
                        languageScript.update({l: 1})
            f.close()
        except:
            print("ERROR ", bddProcess[i])
            faute += 1
            None
    print("NB FAUTES :" , faute)
    os.chdir("/home/clemence/FAC/Master/M1/S1/TER/AnalyseDonneesNextflow/Analyse")
    docs = open("statParts.csv", "w")
    txt = "Database size : {}\n".format(len(bddProcess))
    docs.write(txt)
    txt = "\tPresent\tNot Present\n"
    docs.write(txt)
    #Histogram 
    for k in keyword:
        fig,ax = plt.subplots()
        val = [keyword[k], len(bddProcess)-keyword[k]]
        plt.bar(["Present", "Not Present"], val, color = ['#00429d', '#7f40a2'])
        plt.title(k)
        plt.ylabel('Number')
        name = k + ".png"
        plt.savefig(name)

        nb = keyword[k]
        nb2 = len(bddProcess)-keyword[k]
        txt = "{}\t{}\t{}\n".format(k, nb, nb2)
        docs.write(txt)
    docs.close()

    #Language
    docs = open("statLanguage.csv", "w")
    txt = "Database size : {}\n".format(len(bddProcess))
    docs.write(txt)
    x = []
    y = []
    for l in languageScript:
        fig,ax = plt.subplots()
        x.append(l)
        y.append(languageScript[l])

        txt = "{}\t{}\n".format(l, languageScript[l])
        docs.write(txt)
    docs.close()
    plt.bar(x,y)  
    plt.title("Language Script")
    plt.ylabel("Number")
    plt.savefig("languageScript.png")
    os.chdir(currentPath)

    """
    #print(os.getcwd() )
    adress = "/home/clemence/FAC/Master/M1/S1/TER/AnalyseDonneesNextflow/Workflows/Tuto_Nextflow/test2.txt"
    f = open(adress,"r")
    lines = f.read()

    p = Process(lines) 
    p.extractProcess()
    inputs, outputs, emit = p.extractAll()
    #print(p.output.list_output)
    print("Inputs: ", inputs)
    print("Outputs: ",outputs)
    print("Emit : ", emit)
    #print(p.script.script_string)
    #print("TOOLS : ", p.script.tools)
    #print("ANNOTATIONS : ", p.script.annotations)
    #printInformations(p)
    #printNameInWorkflow(p)
    #printLanguage(p)
    #printQualifier(p)
    f.close()
    """
    print("-----------------------------END-----------------------------")
