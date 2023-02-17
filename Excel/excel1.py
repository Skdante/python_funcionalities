import pandas as pd
import numpy as np

cols = ['Year', 'Length', 'Title']
df = pd.read_excel('exceltest1.xlsx', usecols=cols)

df['Length h'] = np.round(df['Length']/60., 1)
df.to_excel('exceltest1_result.xlsx')

''' 
    Description: Get a Excel Document and read 3 columns (year, length and title) and make a new document 
    with these columns and new column called Lenth h
'''
''' pip install pandas '''
''' pip install xlrd '''
''' pip install openpyxl '''
