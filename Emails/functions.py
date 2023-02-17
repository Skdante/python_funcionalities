import json
import os
from datetime import datetime
import string

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
         print("---|||||| ERROR: Functions fnLoadCFGJSON {0} ||||||---".format(e))  
         return None  
    return objData 

'''
    function:           fnRemoveFile
    param<strFilepath>: ruta del archivo a eliminar
    description:        elimina un archivo si existe    
'''
def fnRemoveFile(strFilepath):
    try:
        if os.path.exists(strFilepath):
           os.remove(strFilepath)    
    except Exception as e:        
        print('---|||||| ERROR: ' + str(e) + ' ||||||---')

'''
    function:           fnGetDayName
    description:        Obtiene el nombre del dia actual  
'''
def fnGetDayName():
    now = datetime.now()
    return now.strftime("%A").lower()  

def fnReturnLetterExcel(num_celda):

    if num_celda < 26:
        return string.ascii_uppercase[num_celda]
    else:
        return string.ascii_uppercase[num_celda // 26 - 1] + string.ascii_uppercase[num_celda % 26]

def fnChangeCaracters(word, characters, valuereplace = ""):

    for x in range(len(characters)):
        word = word.replace(characters[x],valuereplace)

    return word

def fnChangeString(word, characters, valuereplace = ""):
    
    word = word.replace(characters,valuereplace)

    return word