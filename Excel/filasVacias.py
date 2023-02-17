import pandas as pd
df = pd.read_excel(open('filasVacias.xlsx', 'rb'), sheet_name='Sheet1')
print(df)
df.dropna(how='all', inplace=True)
print(df)

'''Elimina filas vacias'''