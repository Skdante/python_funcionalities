import re
import json
from unidecode import unidecode

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

'''
    function:           fnLogging
    param<strType>: ruta del archivo json    
    description:        lee un archivo JSON 
    return:             diccionario apartir de un JSON
'''
#def fnLog(strLogger, strType, strMessage):
#    logger =  logging.getLogger(strLogger)
#    print(logger)
#    if logger == None:     
#        strFilename = datetime.today().strftime('%Y-%m-%d') + '-Logger.log'
#        fh = logging.FileHandler(strFilename) 
#        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))           
#        logger.addHandler(fh)                              
#    fnLogMessage(logger, strType, strMessage)


#def fnLogMessage(objLogger, strType, strMessage):
#    strType = strType.upper()
#    if strType == 'DEBUG':   
#        objLogger.setLevel(logging.DEBUG)                                     
#        logging.debug(strMessage)
#    if strType == 'INFO':        
#       objLogger.setLevel(logging.INFO)                          
#        logging.info(strMessage)
#    if strType == 'WARNING':        
#        objLogger.setLevel(logging.WARNING)                     
#        logging.warning(strMessage)
#    if strType == 'ERROR':        
#        objLogger.setLevel(logging.ERROR)                     
#        logging.error(strMessage)       