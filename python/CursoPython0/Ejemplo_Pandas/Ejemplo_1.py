import numpy as np
import pandas as pd

# Creando una serie con panda
s = pd.Series([1, 3, 5, np.nan, 6, 8])
# print(s)

# Creando un DataFrame agregando datos random con numpy
dates = pd.date_range('20200101', periods=6)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
# print(df)
# print(df.head()) # Muestra los primeros 5 renglones
# print(df.tail(2)) # Muestra los ultimos 2 renglones
# print(df.index) # Muestra los indices
# print(df.describe()) #Muestra de manera general el mayor, menor, suma, etc
# print(df.T) # Cambiando de filas a columnas
# print(df.sort_index(axis=1, ascending=False))
# print(df.sort_values(by='B')) # Ordenando la fila B
# print(df['A']) # Solo muestra la columna A
# print(df[0:2]) # Muestra la fila de la 0 a la 2
print(df['20130102':'20130104']) # Muestra del indice del 20130102 al 20130104

df2 = pd.DataFrame({'A': 1.,
                    'B': pd.Timestamp('20130102'),
                    'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                    'D': np.array([3] * 4, dtype='int32'),
                    'E': pd.Categorical(["test", "train", "test", "train"]),
                    'F': 'foo'})
# print(df2)
# print(df2.dtypes)