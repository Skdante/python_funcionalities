import pandas as pd
import xlsxwriter as xw
import string
import functions as af

'''
    Instalacion inicial:
    pip install pandas
    pip install xlrd
    pip install openpyxl
'''

'''
    function:           fnReadExcel
    param<pathExcel>:   Ruta del excel a leer
    param<cols>:        Columnas a mostrar, por defecto muestra todas
    description:        Obtiene las columnas de un archivo XLSX
    return:             Diccionario de excel
'''
def fnReadExcel(pathExcel, cols = [], sheetName = '', dataType = {}):
    try:
        if sheetName != '' and len(cols) > 0 and dataType != {}:
            df = pd.read_excel(open(pathExcel, 'rb'), usecols=cols, sheet_name=sheetName, dtype=dataType)
        elif len(cols) > 0 and dataType != {}:
            df = pd.read_excel(open(pathExcel, 'rb'), usecols=cols, dtype=dataType)
        elif sheetName != '' and dataType != {}:
            df = pd.read_excel(open(pathExcel, 'rb'), sheet_name=sheetName, dtype=dataType)
        elif sheetName != '' and len(cols) > 0:
            df = pd.read_excel(open(pathExcel, 'rb'), usecols=cols, sheet_name=sheetName)
        elif sheetName != '':
            df = pd.read_excel(open(pathExcel, 'rb'), sheet_name=sheetName)
        elif len(cols) > 0:    
            df = pd.read_excel(pathExcel, usecols=cols)
        else: 
            df = pd.read_excel(pathExcel)
    except Exception as e:
         print("---|||||| ERROR: Excel fnReadExcel {0} ||||||---".format(e))  
         return None  
    return df 

'''
    function:           fnSaveExcel
    param<dictionario>: Diccionario con los datos a guardar
    param<pathExcel>:   Ruta del excel a guardar
    description:        Guarda a un archivo XLSX
    return:             Diccionario de excel
'''
def fnSaveExcel(dictionario, pathExcel):
    try:
        dictionario.to_excel(pathExcel)
    except Exception as e:
         print("---|||||| ERROR: Excel fnSaveExcel {0} ||||||---".format(e))  
         return False  
    return True

'''
    function:           fnFormatExcel
    param<dictionario>: Diccionario con los datos a guardar
    param<type>:        El tipo de formato que le vamos a agregar
    description:        Crea distintos formatos para el excel
    return:             Diccionario de excel
'''
def fnFormatExcel(dictionario, type, has_title = False, title = ''):
    try:

        with xw.Workbook('fichas_metadatos.xlsx') as workbook:
            objCFG = af.fnLoadCFGJSON('datas.json')
            worksheet = workbook.add_worksheet(objCFG['FormatsExcel']['Name_sheet'])
            
            # Formato de titulo
            formato_titulo = workbook.add_format(objCFG['FormatsExcel']['Format_design'][type]['Format_title'])
            
            # Formato de encabezados
            formato_variables = workbook.add_format(objCFG['FormatsExcel']['Format_design'][type]['Format_heads'])

            # Formato del texto normal
            formato_normal = workbook.add_format(objCFG['FormatsExcel']['Format_design'][type]['Format_datas'])

            # Formatos
            date_format = workbook.add_format(objCFG['FormatsExcel']['Format_design'][type]['Format_datas'])
            date_format.set_num_format('mm/dd/yy')

            # Escribimos título
            if has_title:
                worksheet.merge_range('B1:' + string.ascii_uppercase[len(dictionario.columns)] + '1', title, formato_titulo)
                worksheet.set_row(0, 30)
                row = 2
            else:
                row = 1
            
            id = 1

            # fila 2 o encabezados
            worksheet.set_row(row - 1, 20)
            for head in dictionario.columns:
                letter = af.fnReturnLetterExcel(id)
                worksheet.set_column(letter + ':' + letter, 30)
                try:
                    worksheet.write(letter + str(row), head, formato_variables)
                except:
                    pass
                id += 1

            for row_data in dictionario.values:
                col = 1
                for data in row_data:
                    #if col == 10:
                    #    worksheet.write(row, col, data, date_format)
                    #else:
                    try:
                        worksheet.write(row, col, data, formato_normal)
                    except:
                        pass
                    col += 1
                row += 1
                
            #workbook.close()

    except Exception as e:
         print("---|||||| ERROR: Excel fnSaveExcel {0} ||||||---".format(e))  
         return False  
    return True

'''
    function:           fnSaveEfnDeleteEmptyRowsxcel
    param<dictionario>: Diccionario con los datos a guardar
    description:        Elimina las filas vacias
    return:             Diccionario de excel
'''
def fnDeleteEmptyRows(dictionario):
    try:
        dictionario.dropna(how='all', inplace=True)
    except Exception as e:
         print("---|||||| ERROR: Excel fnSaveEfnDeleteEmptyRowsxcel {0} ||||||---".format(e))  
         return False  
    return True