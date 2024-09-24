import io
import glob
import json
import requests
import pandas as pd
from datetime import datetime
from functools import lru_cache
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor, as_completed

def flatten(nested_list):
    return [item for sublist in nested_list for item in sublist]

def get_pdb_info(pdb_id):
    session = requests.Session()
    # Retry configuration: total=3 retries, backoff_factor to increase wait time between attempts
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(f'https://www.ebi.ac.uk/pdbe/api/pdb/entry/entities/{pdb_id}', timeout=10)  # 10 seconds timeout
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return json.loads(response.text)[pdb_id]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {pdb_id}: {e}")
    return None

def get_entity_id(pdb_id):
    pdb_info = get_pdb_info(pdb_id)
    if not pdb_info:
        return None, None, "API Error"
    chain_info = {}
    for entry in pdb_info:
        if entry['molecule_type'] == 'polypeptide(L)':
          # modify the part below to take into account all naming possibilities regarding the organism of interest. such as 'Epstein-barr' or 'herpesvirus 4' for EBV
          if ('hsv' in entry['source'][0]['organism_scientific_name']) or ('HSV' in entry['source'][0]['organism_scientific_name']) or ('alphaherpesvirus' in entry['source'][0]['organism_scientific_name']): 
            if pdb_id not in chain_info.keys():
              chain_info[pdb_id] = []
              chain_info[pdb_id] = [entry['in_chains']]
            else:
              chain_info[pdb_id].append(entry['in_chains'])

    chain_info = {k: flatten(v) for k, v in chain_info.items()}
    return (chain_info)


sheets = ['h1n1', 'h5n1', 'hsv1', 'cmv', 'ebv']
# Read the path to Excel file that contains literature extracted PDB IDs for each virus.
data = pd.read_excel('all_pdbs.xlsx', sheet_name = sheets)
h1n1 = data['h1n1']
h5n1 = data['h5n1']
hsv = data['hsv1']
cmv = data['cmv']
ebv = data['ebv']

def get_pdb_list(df, file_name):
   
    df['chains'] = ''
    pdb_list = df.pdbID.to_list()
    pdb_list = [i.upper() for i in pdb_list]
    ind = 0
    for i in pdb_list:
        try:
            res_dict = get_entity_id(i.lower())
            id = list(res_dict.keys())[0]
            chains = list(res_dict.values())[0]
            df.at[ind, 'pdb_id'] = id
            df.at[ind, 'chains'] = chains
            ind += 1
        except:
            IndexError
            print(i, get_entity_id(i.lower()))

    df.pdbID = df.pdbID.apply(lambda x:x.upper())
    #df.pdb_id = df.pdb_id.apply(lambda x:x.upper() if type(x) != float else x)

    max_len = 0
    for i in df.index:
        if type(df.at[i,'chains']) != float:
            if len(df.at[i,'chains'].split(',')) > max_len:
                max_len = len(df.at[i,'chains'].split(','))
    col_add = []
    for i in range(max_len):
        col_add.append('col' + str(i))
    for col_name in col_add:
        h5n1[col_name] = None
    df_na = df[df.chains.isna()]
    df = df[~df.chains.isna()]
    df.chains = df.chains.apply(lambda x:x[1:-1])
    df[col_add] = df['chains'].str.split(',',expand=True)
    for col in df.columns:
        if (col != 'pdbID') & (col != 'chains'):
            df[col] = df[col].apply(lambda x: x.strip() if x != None else x)
            df[col] = df[col].apply(lambda x: x[1] if x != None else x)
    df.drop(columns = ['chains'], inplace=True)
    df.to_csv(f'{file_name}_chains.txt', sep='\t', index=False)


get_pdb_list(h1n1, 'h1n1') 
get_pdb_list(h5n1, 'h5n1') 
get_pdb_list(hsv, 'hsv') 
get_pdb_list(cmv, 'cmv') 
get_pdb_list(ebv, 'ebv') 




