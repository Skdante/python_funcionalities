import pandas as pd
df = pd.read_excel(open('excelEmails.xlsx', 'rb'), sheet_name='Sheet1')

names = []
surnames = []

for i in df.Email:
    fname = i.split('@')[0]
    name, surname = fname.split('.')
    names.append(name)
    surnames.append(surname)

df['name'] = names
df['surnames'] = surnames

df.to_excel('excelEmails_result.xlsx')