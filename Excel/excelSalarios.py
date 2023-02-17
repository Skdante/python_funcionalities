import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_excel(open('excelSalarios.xlsx', 'rb'), sheet_name='Sheet1')
horas = []

for i in range(len(df['Nombre'])):
    sal =  datetime.strptime(str(df['Salida'][i]), "%H:%M:%S")
    ent =  datetime.strptime(str(df['Entrada'][i]), "%H:%M:%S")
    diff = (sal - ent)
    horas.append(diff.total_seconds()/3600)

df['horas'] = np.round(horas, 1)
df['salario total'] = df['horas'] * df['Salario']

print(df)
