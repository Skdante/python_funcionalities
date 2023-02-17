import pandas as pd
import azzule_dao_sql as asql
import azzule_functions as af

#import complete client catalogue
objCFG = af.fnLoadCFGJSON('ISR_CFG_DEDUPE.json') 
objConnCann = asql.fnConnect(objCFG["SQL"]["canonical"]["connectionstr"])
strQuery = objCFG["SQL"]["canonical"]["query"]

customer_df = pd.read_sql(strQuery, objConnCann)
customer_df.dropna(subset=['CustomerID', 'CustomerName'],inplace=True)
customer_df.drop(customer_df[customer_df["CustomerName"].apply(lambda x: type(x)!=str)].index,inplace=True)
print(customer_df)