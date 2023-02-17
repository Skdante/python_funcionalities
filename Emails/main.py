import time
import functions as af
import sendemail as email
import sqlconection as asql
import csvcreation as acsv
import excelcreation as excel

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
        acsv.fnCreateCSV(arrData, strFile)
    else: 
       return False
    return True


if __name__ == '__main__':
    try:
        start_time = time.time()
        df = excel.fnReadExcel('EntityProfiles.xlsx', sheetName = 'EntityProfiles')
        # df = excel.fnReadExcel('prueba.xlsx', ['EventID', 'EventTypeID'])
        # df = excel.fnReadExcel('prueba.xlsx', ['EventID', 'EventTypeID'], sheetName = 'prueba',dataType = {'EventID': float, 'EventTypeID': float})
        # af.fnRemoveFile('prueba1.xlsx')

        df['values'] = scriptData
        excel.fnFormatExcel(df, 0)
        # excel.fnFormatExcel(df, 0, True, 'Hola Mundo')
        # pase = excel.fnSaveExcel(df, 'prueba1.xlsx')
        # print(df)
    except Exception as e:
        print('---|||||| ERROR: ' + str(e) + ' ||||||---')

'''
if __name__ == '__main__':
    try:
        start_time = time.time()
        objCFG = af.fnLoadCFGJSON('datas.json')
        if objCFG != None: 
            af.fnRemoveFile('prueba.csv')
            fnCreateCSVBySQL(objCFG["SQL"]["connection"]["connectionstr"],objCFG["SQL"]["connection"]["query"], 'prueba.csv')
            #arrDataCannonical =  acsv.fnGetData('prueba.csv',4) 
            #csvsort('prueba.csv', [0], output_filename='prueba.csv', has_header=True)
            #body = open('body_html.txt', 'r')
            #mylist = body.readlines()

            with open('body_html.txt', 'r') as fp:
                mylist = fp.read()
            
            email.fnSendEmail(
                objCFG['DataEmail']['remitente'],
                objCFG['DataEmail']['destinatarios'],
                'Correo de Pruebas - Asunto',
                mylist,
                ['prueba.xlsx', 'prueba1.xlsx'],
                objCFG['DataEmail']['usuario'],
                objCFG['DataEmail']['password'],
                True
                )
            
        else:
             print('---|||||| JSON Invalid ||||||---')
    except Exception as e:
        print('---|||||| ERROR: ' + str(e) + ' ||||||---')
'''