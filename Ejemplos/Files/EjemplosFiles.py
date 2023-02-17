import FilesFunctions as ff
import FilesCSV as fcsv
import FilesExcel as fe

if __name__ == '__main__':
    try:
        #-------------------------  General -------------------------------                       
        ## Remueve un archivo
        ff.fnRemoveFile('prueba.csv')

        #-------------------------  CSV  ----------------------------------
        ## Crea un archivo csv a partir de una consulta en BD
        # ff.fnCreateCSVBySQL("SERVER=10.10.50.30;DATABASE=MasterSystem;UID=ApplicationUser_;PWD=D3$@rr0ll0;",
        # "exec dbo.IS_Relationships_created_Alerts", 
        # 'prueba.csv')
        ## Obtiene la info de un archivo CSV y hace un diccionario
        # arrDataCannonical =  fcsv.fnGetData('prueba.csv',4)
        ## Ordena el archivo CSV indicado
        # fcsv.fnCSVSort('prueba.csv', [0], has_header=True)

        #------------------------- Texto  ----------------------------------
        ## Abrir y leer archivo de texto para obtener un arreglo de strings por linea 
        # body = open('body_html.txt', 'r')
        # mylist = body.readlines()
        ## Abrir y leer archivo de texto para obtener un string por linea  (perfecto para html)
        # with open('body_html.txt', 'r') as fp:
        #        mylist1 = fp.read()

        #-------------------------- Excel  ----------------------------------
        ## Lee un documento excel y devuelve un arreglo de este
        df = fe.fnReadExcel('Documentos Prueba\EntityProfiles.xlsx', sheetName = 'EntityProfiles')
        # df = excel.fnReadExcel('prueba.xlsx', ['EventID', 'EventTypeID'])
        # df = excel.fnReadExcel('prueba.xlsx', ['EventID', 'EventTypeID'], sheetName = 'prueba',dataType = {'EventID': float, 'EventTypeID': float})
        ## Genera el excel la informacion del diccionario y le da un formato
        # fe.fnFormatExcel(df)
        # fe.fnFormatExcel(df, True, 'Archivo de Perfiles') 
        ## Crea un excel a partir de un diccionario en una ruta
        pase = fe.fnSaveExcel(df, 'Documentos Prueba\Datos_prueba.xlsx')
        print(pase)
    except Exception as e:
        print('---|||||| ERROR: ' + str(e) + ' ||||||---')