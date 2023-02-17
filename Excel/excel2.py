import pandas as pd
'''df = pd.read_excel('exceltest2.xlsx', index_col=0)'''
'''df = pd.read_excel(open('exceltest2.xlsx', 'rb'), sheet_name='Sheet2')'''
df = pd.read_excel(open('exceltest2.xlsx', 'rb'), sheet_name='Sheet2', dtype={'Puntuacion': float, 'Peliculas': str})
print(df.Peliculas)

'''
 3 ways o get excel
 1.- Read the first sheet 
 2.- Read the Sheet2 sheet
 3.- Read the Sheet2 sheet and transform the puntacion to type float
'''