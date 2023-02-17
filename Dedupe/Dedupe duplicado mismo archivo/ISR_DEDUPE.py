import azzule_send_email as ase
import azzule_dao_sql as asql
import azzule_csv as acsv
import azzule_functions as af
import codecs
import dedupe
import csv
import os
import time
import re
import logging
from datetime import datetime
from collections import OrderedDict
from csvsort import csvsort
from unidecode import unidecode


def preProcess(column):
    """
    Do a little bit of data cleaning with the help of Unidecode and Regex.
    Things like casing, extra spaces, quotes and new lines can be ignored.
    """
    column = unidecode(column)
    column = re.sub('  +', ' ', column)
    column = re.sub('\n', ' ', column)
    column = column.strip().strip('"').strip("'").lower().strip()
    # If data is missing, indicate that by setting the value to `None`
    if not column:
        column = None
    return column


def readData(filename):
    """
    Read in our data from a CSV file and create a dictionary of records,
    where the key is a unique record ID and each value is dict
    """

    data_d = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = [(k, preProcess(v)) for (k, v) in row.items()]
            row_id = int(row['EntityID'])
            data_d[row_id] = dict(clean_row)

    return data_d


'''
    function:                 fnGetSettingAndTraining
    param<arrDataCannonical>: Array de diccionarios con los datos canonicos    
    description:              Obtiene o Genera un nuevo entrenamiento
    return:                   Objeto dedupe
'''
def fnGetSettingAndTraining(arrDataCannonical, objCFG):
    print('---|||||| Training ||||||---')
    settingsFile = objCFG["files"]["settings"]
    trainingFile = objCFG["files"]["training"]
    arrFields = objCFG["fields"]    
    objDDP = {}
       
    try:
        if os.path.exists(settingsFile):
            print('---|||||| Reading from : ' + settingsFile + ' ||||||---')
            with open(settingsFile, 'rb') as sf: 
                objDDP = dedupe.StaticDedupe(sf)
        else:
            print('---|||||| ' + settingsFile + ' file doesn''t exist ||||||---')          
            objDDP = dedupe.Dedupe(arrFields)

            if os.path.exists(trainingFile):
                print('---|||||| Reading labeled examples from: ' +  trainingFile + ' ||||||---')
                with open(trainingFile) as tf:
                    objDDP.prepare_training(arrDataCannonical,training_file=tf)
            else:
                print('---|||||| ' + trainingFile + ' file doesn''t exist need training ||||||---') 
                print('arrDataCannonical')            
                objDDP.prepare_training(arrDataCannonical)
                        
            print('---||||||  Starting active labeling ||||||---')            
            dedupe.console_label(objDDP) 

            objDDP.train()   
                        
            print('---||||||  Creating file ' + trainingFile + '  ||||||---')        
            with open(trainingFile, 'w') as tf:
                objDDP.write_training(tf)
                                                                            
            print('---||||||  Creating file ' + settingsFile + '  ||||||---')
            with open(settingsFile, 'wb') as sf:
                objDDP.write_settings(sf)
            
            objDDP.cleanup_training()  

    except Exception as e:
        print('---|||||| ERROR fnGetSettingAndTraining: ' + str(e) + ' ||||||---')                
                
    return objDDP

'''
    function:              fnFormClusterDDP
    param<objLinker>:      Objeto dedupe
    param<dataCannonical>: Array de diccionarios con los datos canonicos    
    param<objCFG>:         Objeto con la configuracion de los usuarios
    description:           Obtiene los cluster
    return:                Array de clusters
'''
def fnFormClusterDDP(objDDP, dataCannonical, objCFG):
    print('---|||||| Clustering ||||||---')
    arrCluster = {}  
    arrClusteredDupes = objDDP.partition(dataCannonical, threshold=objCFG["threshold"]) 
    for intClusterID, (records, scores) in enumerate(arrClusteredDupes):
        for intID, dblScore in zip(records, scores):            
            arrCluster[intID] = {
                objCFG["cols"]["clusterid"] : intClusterID,
                objCFG["cols"]["score"]: dblScore
            }
    return arrCluster 


'''
    function:          fnCreateCSV
    param<arrCluster>: array de clusters
    param<objCFG>:     objeto de configuracion del usuario
    description:       Crea archivo final con scores y clusters
'''
def fnCreateCSV(arrCluster, objCFG):    
    outfile = objCFG["files"]["outfile"]
    print('---|||||| Creating final CSV File: ' +  outfile + '  ||||||---')
    cannonical = objCFG["files"]["cannonical"]  
    clusterid = objCFG["cols"]["clusterid"]
    score = objCFG["cols"]["score"]   
    colRef =  objCFG["cols"]["colref"]
    threshold = objCFG["threshold"]
    with open(outfile, 'w', newline = '') as f_output, open(cannonical, ) as f_input:   
        objReader = csv.DictReader(f_input)        
        arrFieldnames = [clusterid, score] + objReader.fieldnames
        objWriter = csv.DictWriter(f_output, fieldnames=arrFieldnames)
        objWriter.writeheader()
        for objRow in objReader: 
            cluster_details = arrCluster[int(objRow[colRef])]
            if cluster_details != {}:                 
                if cluster_details[score] >= threshold and cluster_details[score] <= 1:              
                    objRow.update(arrCluster[int(objRow[colRef])])
                    objWriter.writerow(objRow)                            

'''
    function:       fnValidateJSONCFG
    param<objDict>: objeto de configuracion de usuario 
    description:    valida la informacion que proporciona el usuario
    return:         Boolean
'''
def fnValidateJSONCFG(objDict):
    methods = ['dedupe','gazetter','recordlinkage']
    if objDict["files"]["settings"] == '':
        print('---|||||| ERROR: Provide settings filename ||||||---')
        return False
    if objDict["files"]["training"] == '':
        print('---|||||| ERROR: Provide training filename ||||||---')
        return False
    if objDict["threshold"] == '':
        print('---|||||| ERROR: Provide threshold ||||||---')
        return False         
    if objDict["files"]["cannonical"] == '':
        print('---|||||| ERROR: Provide cannonical file ||||||---')
        return False      
    if objDict["files"]["outfile"] == '':
        print('---|||||| ERROR: Provide out file ||||||---')
        return False          
    if objDict["cols"]["clusterid"] == '':
        print('---|||||| ERROR: Provide column clusterid ||||||---')
        return False   
    if objDict["cols"]["score"] == '':
        print('---|||||| ERROR: Provide column score ||||||---')
        return False        
    if objDict["cols"]["colref"] == '':
        print('---|||||| ERROR: Provide column colref ||||||---')
        return False                                       
    if objDict["fields"] == None or len(objDict["fields"]) == 0:
        print('---|||||| ERROR: Provide fields configuration ||||||---')
        return False
    if objDict["method"] == None or objDict["fields"] == "":    
        print('---|||||| ERROR: Provide method||||||---')
        return False  
    if objDict["method"] not in methods:
        print('---|||||| ERROR: Provide valid method ||||||---')
        return False                         
    return True  

'''
    function:          fnCreateCSVBySQL
    param<strConnstr>: string de conexion a sql 
    param<strQuery>:   string sql query
    param<strFile>:    string file path
    description:       crea un csv apartir de datos de sql
    return:            Boolean
'''
def fnCreateCSVBySQL(strConnstr, strQuery, strFile):
    print("---|||||| Creating file " + strFile + " ||||||---")        
    objConnCann = asql.fnConnect(strConnstr)
    strDayName = fnGetDayName()
    if strDayName == 'monday':
        strQuery = strQuery.replace('|DAYS|', "-3")
    else:
        strQuery = strQuery.replace('|DAYS|', "-1")
    arrData = asql.fnGetDataTables(objConnCann,strQuery)
    if len(arrData) > 0:
        acsv.fnCreateCSV(arrData, strFile)
    else: 
       return False
    return True

'''
    function:          fnSendMail
    param<objMessage>: objeto de configuracion para envio de mensajes 
    description:       envia un email
'''
def fnSendMail(objMessage):
    print("---|||||| Sending email ||||||---")        
    ase.fnSendEmail({
        "subject": "Daily Dedupe Notification {0}".format(objMessage.get('subject','')),
        "from": "roberto.rodriguez@primuslabs.com",
        #"to": "roberto.rodriguez@primuslabs.com;yair.roman@azzule.com;karel.apodaca@azzule.com;samuel.rodriguez@azzule.com",
        #"to": "roberto.rodriguez@primuslabs.com;samuel.rodriguez@azzule.com;yair.roman@azzule.com",
        #"to": "roberto.rodriguez@primuslabs.com;samuel.rodriguez@azzule.com",
        "to": "samuel.rodriguez@azzule.com",
        #"to": "roberto.rodriguez@azzule.com",
        "cc": "",
        "bcc": "",
        "body": "",
        "html": objMessage.get('message',''),
        "files": objMessage.get('files',[])
    })

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
    function:          fnSendNotificationTemplate
    param<objCFG>:     objeto de configuracion para el envio del template
    description:       envia un correo con template
'''
def fnSendNotificationTemplate(objCFG):    
    intDuration = time.time() - objCFG.get('inittime')   
    strException = objCFG.get('exception', '')
    objFile = codecs.open("ISR-DEDUPE-NOTIFICATION.html", 'r')
    strHTML = objFile.read()
    if strException == '':
        strException = "There was not an Exception"
    strHTML = strHTML.replace('|Message|',objCFG.get('message')).replace('|Duration|',str(intDuration) + ' seconds').replace('|Exception|', strException)
    #fnSendMail({
    #   'subject': objCFG.get('subject'),
    #   'message': strHTML,
    #   'files':   objCFG.get('files')
    #})  

def fnGetDayName():
    now = datetime.now()
    return now.strftime("%A").lower()          


if __name__ == '__main__':     
    try:
        start_time = time.time()
        objCFG = af.fnLoadCFGJSON('ISR_CFG_DEDUPE.json')         
        if objCFG != None:                                              
            if fnValidateJSONCFG(objCFG):                                  
                fnRemoveFile(objCFG["files"]["outfile"])
                if objCFG["SQL"]["enabled"]:
                    fnRemoveFile(objCFG["files"]["cannonical"])                    
                    boolResult = fnCreateCSVBySQL(objCFG["SQL"]["canonical"]["connectionstr"],objCFG["SQL"]["canonical"]["query"], objCFG["files"]["cannonical"])                    
                    if boolResult == False:
                        raise Exception("Cannonical data is empty")         
                arrD = readData(objCFG["files"]["cannonical"])
                print(arrD)
                       
                arrDataCannonical =  acsv.fnGetData(objCFG["files"]["cannonical"],4)                 
                
                #crea un entrenamiento basado en los datos proporcionados o utiliza uno existente dependiendo la configuracion dada del usuario                                                                 
                objDDP = fnGetSettingAndTraining(arrDataCannonical, objCFG)                
                print("---|||||| Init form arrClusters||||||---")

                arrCluster = fnFormClusterDDP(objDDP, arrDataCannonical, objCFG)                
                #print("---|||||| arrCluster len:" + str(len(arrCluster)) + "||||||---")
                if len(arrCluster) > 0:
                    print("len(arrCluster) > 0")
                    print(arrCluster)
                    #crea el archivo
                    fnCreateCSV(arrCluster, objCFG)  
                    csvsort(objCFG["files"]["outfile"], [0], output_filename=objCFG["files"]["outfile"], has_header=True)
                    fnSendNotificationTemplate({
                        'subject': 'Report By CustomerName',
                        'message': 'Hi, the daily dedupe record linkage is attach',
                        'inittime': start_time,
                        'exception': '',
                        'files': [objCFG["files"]["outfile"]]
                    })
                else:  
                    print("---|||||| No Clusters ||||||---")                  
                    fnSendNotificationTemplate({
                        'subject': 'Report By CustomerName',
                        'message': 'Hi, the daily dedupe record linkage doesn''t have duplicates',
                        'inittime': start_time,
                        'exception': '',
                        'files': [objCFG["files"]["messy"]]
                    })            
                    print("---|||||| Process was successfully ||||||---")
        else:
             print('---|||||| JSON CFG Invalid ||||||---')
    except Exception as e:
        fnSendNotificationTemplate({
            'subject': 'Exception',
            'message': 'There was an exception: ',
            'inittime': start_time,
            'exception': str(e),
            'files': []
        })
        print('---|||||| ERROR: ' + str(e) + ' ||||||---')