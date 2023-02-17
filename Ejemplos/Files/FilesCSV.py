import csv
import re
from csvsort import csvsort
from sys import version_info

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
                objCleanRow = dict([(k, fnPreProcess(v)) for (k, v) in objRow.items()])
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
         print("---|||||| ERROR: CSV fnCSVGetData {0} ||||||---".format(e))  
         return None 
    if intRefType == 4:
        return arrList
    return objDictData

'''
    function:               fnCSVSort
    param<input_filename>:  Ruta del archivo
    param<columns>:         Columnas a Ordenar
    param<has_header>:      Tiene Encabezado
    description:            Obtiene los datos de un archivo CSV
    return:                 Array
'''
def fnCSVSort(input_filename, columns, has_header):
    csvsort(input_filename, columns, output_filename=input_filename, has_header=has_header)

def _warn_if_not_unicode(string):
    if version_info[0] < 3 and not isinstance(string, unicode):
        warnings.warn(  "Argument %r is not an unicode object. "
                        "Passing an encoded string will likely have "
                        "unexpected results." % (type(string),),
                        RuntimeWarning, 2)

def unidecode_expect_ascii(string):
    """Transliterate an Unicode object into an ASCII string

    >>> unidecode(u"\u5317\u4EB0")
    "Bei Jing "

    This function first tries to convert the string using ASCII codec.
    If it fails (because of non-ASCII characters), it falls back to
    transliteration using the character tables.

    This is approx. five times faster if the string only contains ASCII
    characters, but slightly slower than using unidecode directly if non-ASCII
    chars are present.
    """

    _warn_if_not_unicode(string)
    try:
        bytestring = string.encode('ASCII')
    except UnicodeEncodeError:
        return _unidecode(string)
    if version_info[0] >= 3:
        return string
    else:
        return bytestring

unidecode = unidecode_expect_ascii

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
        print("---|||||| ERROR: Functions fnPreProcess {0} ||||||---".format(e))  
        return None  
    return column 