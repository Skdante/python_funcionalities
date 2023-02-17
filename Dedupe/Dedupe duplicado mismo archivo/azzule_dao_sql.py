import pyodbc
import azzule_functions as af

'''
    function:           SQLConnect
    param<strConn>:     String de conexion SQL
    description:        Crea una conexion tipo sql
    return:             Objeto de conexion SQL
'''
def fnConnect(strConn): 
    try:   
        if not strConn:
            return None       
        strConn = 'DRIVER={ODBC Driver 17 for SQL Server};' + strConn            
        objCon = pyodbc.connect(strConn)
    except Exception as e:
        print("---|||||| ERROR: Azzule SQLConnect {0} ||||||---".format(e))
        return None
    return objCon

'''
    function:           SQLGetTablesFromDatabase
    param<objConn>:     Objeto de conexion SQL
    param<strQuery>:    Query a ejecutar
    param<boolOnlyOne>: Un solo renglon
    description:        Obtiene todo el dataset de la consulta
    return:             Array data
'''
def fnGetDataTables(objConn, strQuery, boolOnlyOne = False):
    objCursor = objConn.cursor()
    objCursor.execute(strQuery)
    arrItems = [dict((objCursor.description[i][0], value) for i, value in enumerate(objRow)) for objRow in objCursor.fetchall()]    
    objCursor.connection.close()
    return (arrItems[0] if arrItems else None) if boolOnlyOne else arrItems              