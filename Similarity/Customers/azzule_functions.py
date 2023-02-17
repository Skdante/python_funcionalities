import re
import json
from unidecode import unidecode
from datetime import datetime

'''
    function:      fnPreProcess
    param<column>: String para limpiar
    description:   Limpia los strings que se obtienen del archivo csv
    return:        String limpio
'''
def fnPreProcess(column):       
    try: 
        column = unidecode(column)
        column = re.sub('\n', ' ', column)
        column = re.sub('-', '', column)
        column = re.sub('/', ' ', column)
        column = re.sub("'", '', column)
        column = re.sub(",", '', column)
        column = re.sub(":", ' ', column)
        column = re.sub('  +', ' ', column)
        column = column.strip().strip('"').strip("'").lower().strip()
        if not column:
            column = None        
    except Exception as e:
        print("---|||||| ERROR: Azzule Functions fnPreProcess {0} ||||||---".format(e))  
        return None  
    return column 

'''
    function:           fnLoadCFGJSON
    param<strFilepath>: ruta del archivo json    
    description:        lee un archivo JSON 
    return:             diccionario apartir de un JSON
'''
def fnLoadCFGJSON(strFilepath): 
    try:
        objData = {}   
        if strFilepath != '':            
            with open(strFilepath) as json_file:
                objData = json.load(json_file)             
        else:
            print('--|||||| Please provide JSON CFG File ||||||---')
            return None
    except Exception as e:
         print("---|||||| ERROR: Azzule Functions fnLoadCFGJSON {0} ||||||---".format(e))  
         return None  
    return objData 

'''
    function:           fnMergeDictionaries
    param<strFilepath>: ruta del archivo json    
    description:        lee un archivo JSON 
    return:             diccionario apartir de un JSON
'''
def fnMergeDictionaries(dict1, dict2):    
    return {**dict1, **dict2}  

def fnGetDayName():
    now = datetime.now()
    return now.strftime("%A").lower()     