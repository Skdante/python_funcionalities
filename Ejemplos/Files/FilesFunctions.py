import os
import sqlconection as asql
import FilesCSV as fcsv
import string

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
    arrData = asql.fnGetDataTables(objConnCann,strQuery)
    if len(arrData) > 0:
        fcsv.fnCreateCSV(arrData, strFile)
    else: 
       return False
    return True

def fnReturnLetterExcel(num_celda):
    
    if num_celda < 26:
        return string.ascii_uppercase[num_celda]
    else:
        return string.ascii_uppercase[num_celda // 26 - 1] + string.ascii_uppercase[num_celda % 26]