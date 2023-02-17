import csv
import azzule_functions as af
import operator

'''
    function:           fnCSVGetData
    param<strFileCSV>:  Ruta del archivo
    description:        Obtiene los datos de un archivo CSV
    return:             Array
'''
def fnGetData(strFileCSV, intRefType, strColIntRef = ''):       
    try:
        objDictData = {}
        arrList = []
        with open(strFileCSV) as f:
            objReader = csv.DictReader(f)
            for intIndex, objRow in enumerate(objReader):
                objCleanRow = dict([(k, af.fnPreProcess(v)) for (k, v) in objRow.items()])                
                #by int column reference
                if intRefType == 1:
                   intRowID = int(objRow[strColIntRef])                    
                   objDictData[intRowID] = dict(objCleanRow)       
                #by fileName
                if intRefType == 2:
                    objDictData[strFileCSV + str(intIndex)] = dict(objCleanRow)
                #by index
                if intRefType == 3:
                    objDictData[intIndex] = dict(objCleanRow)
                #only dictionaries
                if intRefType == 4:
                    arrList.append(objCleanRow)
    except Exception as e:
         print("---|||||| ERROR: Azzule CSV fnCSVGetData {0} ||||||---".format(e))  
         return None 
    if intRefType == 4:
        return arrList
    return objDictData

'''
    function:           fnFormClusterGzttr
    param<strFilename>: Ruta del archivo
    description:        Obtiene las columnas de un archivo CSV
    return:             Array strings
'''
def fnGetColumnNames(strFilename):
    try:
        arrList = []
        if strFilename != '':
            with open(strFilename) as f_input:
                reader = csv.DictReader(f_input)
                arrList = reader.fieldnames  
    except Exception as e:
         print("---|||||| ERROR: Azzule CSV fnCSVGetColumnNames {0} ||||||---".format(e))  
         return None  
    return arrList   

'''
    function:           fnCreateCSV
    param<strFilename>: Ruta del archivo
    description:        Obtiene las columnas de un archivo CSV
    return:             Array strings
'''
def fnCreateCSV(arrDict, strCSVFileout):
    try:    
        with open(strCSVFileout, 'w', newline = '') as f_output:
            keys = arrDict[0].keys()
            objWriter = csv.DictWriter(f_output, fieldnames=keys)
            objWriter.writeheader()
            for objItem in arrDict:                                    
                objWriter.writerow(objItem) 
    except Exception as e:
         print("---|||||| ERROR: Azzule CSV fnCreateCSV {0} ||||||---".format(e))  
         return False  
    return True    

def fnSortCSV(data, col=0):
     return sorted(data, key=operator.itemgetter(col))
