#10/28/2018
#Creates bar graph to show the number of occurrences for icd9 codes

import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

def main():
    plot_occurrences('icd_occurrences.txt','icd_E_occurrences.txt',
                     'icd_V_occurrences.txt',5000)

'''
export_ICD9_occurrences_libraries only needs to be called to produce icd9
    library files
'''
def export_ICD9_occurrence_libraries(icd_diagnoses_file):

    DIAGNOSES_ICD = pd.read_csv(icd_diagnoses_file)
    
    #3 occurrence libraries for each style of ICD9 codes
    ICD_lib = {}
    ICD_E_lib = {}
    ICD_V_lib = {}

    for index, row in DIAGNOSES_ICD.iterrows():   
        code = row['ICD9_CODE']
        code = str(code)

        #E-codes
        if(code[0] == 'E'):
            if(len(code) > 4):
                code = code[:4] + '.' + code[4:]
            E_code = code[1:]
            E_code = float(E_code.strip(' "'))
            if E_code in ICD_E_lib:
                ICD_E_lib[E_code] += 1 
            else:
                ICD_E_lib[E_code] = 1
         #V-codes
        elif(code[0] == 'V'):
            if(len(code) > 2):
                code = code[:3] + '.' + code[3:]
            V_code = code[1:]
            V_code = float(V_code.strip(' "'))
            if V_code in ICD_V_lib:
                ICD_V_lib[V_code] += 1 
            else:
                ICD_V_lib[V_code] = 1
        #Regular-codes
        else:        
            if(len(code) > 3):
                code = code[:3] + '.' + code[3:]
            code = float(code.strip(' "')) 
            if code in ICD_lib:
                ICD_lib[code] += 1 
            else:
                ICD_lib[code] = 1

    #export libraries to .txt files
    with open('icd_occurrences.txt', 'w') as f:
        json.dump(ICD_lib, f)

    with open('icd_E_occurrences.txt', 'w') as f:
        json.dump(ICD_E_lib, f)

    with open('icd_V_occurrences.txt', 'w') as f:
        json.dump(ICD_V_lib, f)
     
#min_occur is the minimum number of occurrences in file to be plotted
def plot_occurrences(icd_occur_file, E_icd_occur_file, V_icd_occur_file, min_occur):

    with open(icd_occur_file) as f:
        ICD_lib = json.load(f)

    with open(E_icd_occur_file) as f:
        ICD_E_lib = json.load(f)

    with open(V_icd_occur_file) as f:
        ICD_V_lib = json.load(f)

    icd_codes = []
    num_codes = []

    for key,val in ICD_lib.items():      
        if(val > min_occur):
            icd_codes.append(key)  
            num_codes.append(val)

    for key,val in ICD_E_lib.items():      
        if(val > min_occur):
            icd_codes.append("E" + str(key))  
            num_codes.append(val)
            
    for key,val in ICD_V_lib.items():      
        if(val > min_occur):
            icd_codes.append("V" + str(key))  
            num_codes.append(val)

    #export icd_codes and num_codes for social network mapping
    with open('icd_codes.txt', 'w') as f:
        json.dump(icd_codes, f)
    
    with open('num_codes.txt', 'w') as f:
        json.dump(num_codes, f)

    index = np.arange(len(icd_codes))
    plt.bar(index, num_codes)
    plt.xlabel('ICD Diagnose Code', fontsize=10)
    plt.ylabel('Number of Occurrences', fontsize=10)
    plt.xticks(index, icd_codes, fontsize=6, rotation=80)
    plt.title('MIMIC-iii ICD_Diagnose Occurrences')
    plt.show()

main()
   
