# Nextflow Analyzer
# Written by Clémence Sebe and George Marchment
# October 2021 - April 2022

import argparse
from concurrent.futures import process 
from pathlib import Path
import os
import glob2

 
print('''
  _   _ _______  _______ _____ _     _____        __     _    _   _    _    _  __   ____________ ____  
 | \ | | ____\ \/ |_   _|  ___| |   / _ \ \      / /    / \  | \ | |  / \  | | \ \ / |__  | ____|  _ \ 
 |  \| |  _|  \  /  | | | |_  | |  | | | \ \ /\ / /    / _ \ |  \| | / _ \ | |  \ V /  / /|  _| | |_) |
 | |\  | |___ /  \  | | |  _| | |__| |_| |\ V  V /    / ___ \| |\  |/ ___ \| |___| |  / /_| |___|  _ < 
 |_| \_|_____/_/\_\ |_| |_|   |_____\___/  \_/\_/    /_/   \_|_| \_/_/   \_|_____|_| /____|_____|_| \_\ 
                                                                                                       
''')

print("""________________________________________________

Developped by Clemence Sebe and George Marchment
________________________________________________\n""")

from .workflow import *

def main():
    #Get current directory
    current_directory = os.getcwd()
    
    parser = argparse.ArgumentParser()
    #Obligatory
    #parser.add_argument('input') 
    #parser.add_argument('results_directory')
    #Facultative
    parser.add_argument('--input', default='') 
    parser.add_argument('--results_directory', default='')
    parser.add_argument('--name', default='Workflow_Analysis')
    parser.add_argument('--mode', default='single') #single mode is the default
    parser.add_argument('--dev', default='F') #For developpeur mode or not
    args = parser.parse_args() 
    
    #Setting the current directory to where the extracted data will be saved
    os.chdir(args.results_directory)

    if(args.input == ''):
        raise Exception('\x1b[1;37;41m' + f'The parameter "input" was not given!!'+ '\x1b[0m')
    if(args.results_directory == ''):
        raise Exception('\x1b[1;37;41m' + f'The parameter "results_directory" was not given!!'+ '\x1b[0m')
    #=========
    # SINGLE
    #=========
    if(args.mode == 'single'):
        print('')
        print('\x1b[1;37;42m' + 'Single Workflow analysis mode was selected' + '\x1b[0m')
        print('')
        
        #The file exists
        print(f'Analyzing the workflow : {args.input}')
        #Creating the new file if it doesn't exist
        os.system(f"mkdir -p {args.name}")
        #Setting the current directory to the file directory
        res=args.results_directory+'/'+args.name
        os.chdir(res)
        #Analysing the workflow
        w = Workflow(args.input)
        w.initialise()
        print(f'Results saved in : {res}')
        #Delete developper files if not in dev mode
        if(args.dev == 'F'):
            os.system('rm -f channels_extracted.nf')
            os.system('rm -f processes_extracted.nf')
        
    
    #=========
    # MULTI
    #=========
    elif(args.mode == 'multi'):
        total, DSL2, DSL1_analyzed, DSL1_not_analyzed, curly, problem_process= 0, 0, 0, 0, 0, 0
        errors, DSL2_tab, curlies_tab, analyzed_tab, process_tab = [], [], [], [], []
        print('')
        print('\x1b[7;33;40m' + 'Multiple Workflow analysis mode was selected' + '\x1b[0m')
        print('')
        #Checking that the input is not a file
        if Path(args.input).is_file():
            raise Exception('\x1b[1;37;41m' + f"'{args.input}' is file, a directory is expected for multi mode!!"+ '\x1b[0m')
        else:
            #Retrieving the addresses of the nextflow files found at the root of the file
            all_header_files = glob2.glob(args.input+'/*.nf')
            print(f'Found {len(all_header_files)} workflows to analyse in {args.input}')
            #Extract the names of the workflows
            names=[]
            for h in all_header_files:
                names.append( h[len(args.input+'/') :(-len('.nf'))])
            #For each workflow
            for i in range(len(names)):
                total+=1
                print(f'{i+1}/{len(all_header_files)}')
                print(f'Analyzing the workflow : {names[i]}')
                #Creating the new folder to save the data from the analyze
                res=args.results_directory+'/'+args.name+'/'+names[i]
                os.system(f"mkdir -p {res}")
                os.chdir(res)
                #Analysing the workflow
                try:
                    w = Workflow(all_header_files[i])
                    w.initialise()
                    DSL1_analyzed+=1
                    analyzed_tab.append(names[i])
                    #Delete developper files if in dev mode
                    if(args.dev != 'F'):
                        os.system('rm -f channels_extracted.nf')
                        os.system('rm -f processes_extracted.nf')
                except Exception as inst:
                    #Error DSL2
                    if (str(inst) == "Workflow written in DSL2 : I don't know how to analyze the workflow yet"):
                        print('\x1b[1;37;44m' + f"Workflow written in DSL2 : I don't know how to analyze the workflow yet"+ '\x1b[0m')
                        DSL2+=1
                        DSL2_tab.append(names[i])
                    #Error not the same number of curlies
                    elif (str(inst) == "WHEN A CURLY OPENS IT NEEDS TO BE CLOSED! : Didn't find the same number of open curlies then closing curlies"):
                        print('\x1b[1;37;45m' + f"Not the same number of open and closing curlies in Workflow : I don't know how to analyze the workflow yet"+ '\x1b[0m')
                        curly+=1
                        curlies_tab.append(names[i])
                    #Error with a process
                    elif (str(inst)[:28] == "Couldn't analyze the process"):
                        print('\x1b[1;37;46m' +str(inst)+ '\x1b[0m')
                        problem_process+=1
                        process_tab.append(names[i])
                    #Unknown Error 
                    else:
                        print('\x1b[1;37;41m' + f"Couldn't analyse Workflow : {str(inst)}"+ '\x1b[0m')
                        DSL1_not_analyzed+=1
                        errors.append([names[i], str(inst)])
                print('')
            #Setting current directory to the root of the results
            res=args.results_directory+'/'+args.name
            os.chdir(res)

            #Saving the results
            s = f'{total} Total\n'
            s+= f'{DSL1_analyzed} DSL1_analyzed\n'
            s+= f'{DSL1_not_analyzed} DSL1_not_analyzed\n'
            s+= f'{DSL2} DSL2\n'
            s+= f'{curly} Curlies\n'
            s+= f'{problem_process} Processes_not_analyzed'
            myText = open('summary'+'.txt','w')
            myText.write(s)
            myText.close()
            print(s )

            myText = open('erros'+'.txt','w')
            for e in errors:
                myText.write(f"file : {e[0]}\nerror : {e[1]}\n\n")
            myText.close()

            myText = open('DSL2_files'+'.txt','w')
            for e in DSL2_tab:
                myText.write(f"{e}\n")
            myText.close()

            myText = open('curlies_files'+'.txt','w')
            for e in curlies_tab:
                myText.write(f"{e}\n")
            myText.close()

            myText = open('analyzed_files'+'.txt','w')
            for e in analyzed_tab:
                myText.write(f"{e}\n")
            myText.close()

            myText = open('process_not_analyzed_files'+'.txt','w')
            for e in process_tab:
                myText.write(f"{e}\n")
            myText.close()


    #=========
    # ERROR
    #=========
    else:
        raise Exception(f"Neither single or multiple workflow analysis was selected, but '{args.mode}'")
    
    #When finished setting directory to the original directory
    os.chdir(current_directory)
