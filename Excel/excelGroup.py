import pandas as pd
cols = ['Year', 'Genero', 'Ventas']
df = pd.read_excel(open('excelVentas.xlsx', 'rb'), sheet_name='Sheet1', usecols=cols)

df = df.groupby(['Year','Genero'])['Ventas'].sum()

print(df)
'''df.to_excel('excelVentas_result.xlsx')'''