import pandas as pd
import json
import networkx as nx
from itertools import combinations 
import matplotlib.pyplot as plt

def main():
    create_social_network('icd_codes.txt','num_codes.txt','patient_lib.txt')

def export_patient_codes_library(diagnoses_icd_file):

    Patient_lib = {}
    icd_codes = ['4019','25000','5849','42731','2724','51881','V053',
                 'V290','2859','41401','53081','2720','5990','4280']

    DIAGNOSES_ICD = pd.read_csv(diagnosis_icd_file)
    #eliminate unneeded colums
    VALID_DIAGNOSES_ICD = pd.DataFrame(columns = ('SUBJECT_ID','ICD9_CODE'))

    #only include rows with matching code in icd_codes
    for index, row in DIAGNOSES_ICD.iterrows():
        code = row['ICD9_CODE']
        patient = row['SUBJECT_ID']
        code = str(code)
        for ans_code in icd_codes:
            if(code == ans_code):
                TEMP_DF = pd.DataFrame([[patient, code]], columns  = ('SUBJECT_ID',
                                                                      'ICD9_CODE'))
                VALID_DIAGNOSES_ICD = VALID_DIAGNOSES_ICD.append(TEMP_DF)

    #create patient code library
    for index, row in VALID_DIAGNOSES_ICD.iterrows():
        code = row['ICD9_CODE']
        patient = row['SUBJECT_ID']
        Patient_lib.setdefault(patient, []).append(code)      
            

    with open('patient_lib.txt', 'w') as f:
        json.dump(Patient_lib, f)

def create_social_network(icd_codes_file, num_codes_file, patient_lib_file):

    icd_codes = []
    num_codes = []
    Edge_lib = {}

    with open (icd_codes_file) as f:
        icd_codes = json.load(f)

    with open (num_codes_file) as f:
        num_codes = json.load(f)

    with open (patient_lib_file) as f:
        Patient_lib = json.load(f)  

    i = 0
    for num in num_codes:     
        num_codes[i] = num/4
        i = i+1

    #Edges in network + weights
    for patient, codes_list in Patient_lib.items():           
            patient_codes = []
            for code in codes_list:
                patient_codes.append(code)
            if(len(patient_codes) > 1):
                comb = combinations(patient_codes,2)
                for code_comb in list(comb):
                    if (code_comb[0],code_comb[1]) in Edge_lib:
                        Edge_lib[(code_comb[0],code_comb[1])] += 1
                    else:
                        Edge_lib[(code_comb[0],code_comb[1])] = 1

    #Draw Network
    labels = {}
    all_weights = []
                        
    G = nx.Graph()
    G.add_nodes_from(icd_codes)
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G,pos,node_color='bisque',node_size=num_codes)

    for node_name in icd_codes:
        labels[str(node_name)] = str(node_name)
        
    nx.draw_networkx_labels(G,pos,labels,font_size=12)
     
    for code_tuple, weighted in Edge_lib.items():   
        G.add_edge(code_tuple[0],code_tuple[1],weight=weighted)
    
    for (node1,node2,data) in G.edges(data=True):
        all_weights.append(data['weight'])

    unique_weights = list(set(all_weights))

    for weight in unique_weights:
        weighted_edges = [(node1,node2) for (node1,node2,edge_attr) in
                          G.edges(data=True) if edge_attr['weight']==weight]
        width = weight*len(icd_codes)*4.0/sum(all_weights)
        nx.draw_networkx_edges(G,pos,edgelist=weighted_edges,width=width)
     
    plt.axis('off')
    plt.title('ICD9 Diagnoses Code Network from Patients')
    plt.savefig("patient_code_connections.png") 
    plt.show()

main()





     
