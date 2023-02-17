import json

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
            print('--|||||| Please provide JSON File ||||||---')
            return None
    except Exception as e:
         print("---|||||| ERROR: Functions fnLoadCFGJSON {0} ||||||---".format(e))  
         return None  
    return objData