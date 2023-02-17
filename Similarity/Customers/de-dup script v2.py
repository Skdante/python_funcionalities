import pandas as pd
import numpy as np
import regex as re
import sys, os
import azzule_dao_sql as asql
import azzule_functions as af


#import complete client catalogue
objCFG = af.fnLoadCFGJSON('ISR_CFG_DEDUPE.json') 
objConnCann = asql.fnConnect(objCFG["SQL"]["canonical"]["connectionstr"])
strQuery = objCFG["SQL"]["canonical"]["query"]

customer_df = pd.read_sql(strQuery, objConnCann)
customer_df.dropna(subset=['CustomerID', 'CustomerName'],inplace=True)
customer_df.drop(customer_df[customer_df["CustomerName"].apply(lambda x: type(x)!=str)].index,inplace=True)

##################################################################
#quitar entradas de prueba
##################################################################

customer_df["length"]=customer_df["CustomerName"].apply(lambda x: len(x))
customer_df["nunique"]=customer_df["CustomerName"].apply(lambda x: len(set(x)))
customer_df["has_number"]=customer_df["CustomerName"].apply(lambda x: len(re.findall("\d",x))>0)
customer_df["numeric_ratio"]=customer_df["CustomerName"].apply(lambda x:len(re.findall("\d",x))/len(x))


#1. prueba
aux_df=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("prueba", x,re.IGNORECASE)!=None)]
id1=aux_df[~aux_df["CustomerName"].apply(lambda x: "Microbio" in x)]["CustomerID"].to_list()

#2. testing
aux_df=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("testing", x,re.IGNORECASE)!=None)]
id2=aux_df[~aux_df["CustomerName"].apply(lambda x: "Sysco" in x)]["CustomerID"].to_list()

#3. test
aux_df=customer_df[customer_df["CustomerName"].apply(lambda x: (re.search("test", x,re.IGNORECASE)!=None) and 
                    (re.search("testing", x,re.IGNORECASE)==None))]
aux_list=['Testa Produce',"Driscollstest","Rhiannon's test grower", "Test Maos 2 (díazz)", "M & R Testa, Inc.",
         'Froome Family - Test','Driscolls Test Plot', 'Soho Test Farm', 'ttest.org',
         'Fresh Express (demo/test)','LIMS TEST 2', 'LA ORGANIZATION TESTE T1',"Rancho The Greatest Berries, S. de P.R. de R.L."]
id3=aux_df[~aux_df["CustomerName"].isin(aux_list)]["CustomerID"].to_list()

#4 T E S T
id4=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("T E S T",x,re.IGNORECASE)!=None)]["CustomerID"].to_list()
#5 supplier not assigned
id5=customer_df[customer_df["CustomerName"]=='* Supplier not assigned']["CustomerID"].to_list()

#6 quitar entradas de longitud 1
id6=customer_df[customer_df["length"]==1]["CustomerID"].to_list()

#7 entradas con poca variedad de caracteres
id7=customer_df[(customer_df["nunique"]<=2)&(customer_df["length"]>=7)]["CustomerID"].to_list()

#8 NEWCUST...
id8=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("(new)(\s)?(cust)", x,re.IGNORECASE)!=None)]["CustomerID"].to_list()

#9 182176510NP
id9=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("(\d{9})(np)", x,re.IGNORECASE)!=None)]["CustomerID"].to_list()

#10 ^\w..$ (H.., 1.., etc.)
aux_df=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("(^)(\w){0,2}(\.)*($)", x,re.IGNORECASE)!=None)]
aux_list=["IO."]
id10=aux_df[~aux_df["CustomerName"].isin(aux_list)]["CustomerID"].to_list()

#11 primus
id11=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("primus", x,re.IGNORECASE)!=None)]["CustomerID"].to_list()

#12 SCP|TGC-123123
id12=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("(SCP|TGC)-(\d)+", x,re.IGNORECASE)!=None)]["CustomerID"].to_list()

#13 P17676/1/02
id13=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("([a-z])(\d)+(/)", x,re.IGNORECASE)!=None)]["CustomerID"].to_list()

#14 client
id14=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("client", x,re.IGNORECASE)!=None)]["CustomerID"].to_list()

#15 28808B
id15=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("^(\d)+(\w)$", x,re.IGNORECASE)!=None)]["CustomerID"].to_list()

#16 niba-
id16=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("^(niba)-", x,re.IGNORECASE)!=None)]["CustomerID"].to_list()

#17 M-03
id17=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("^m-(\d)+$", x,re.IGNORECASE)!=None)]["CustomerID"].to_list()

#18 9829-01
id18=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("^(\d){4}-(\d){2}$", x,re.IGNORECASE)!=None)]["CustomerID"].to_list()

#19 09220OPC13
id19=customer_df[customer_df["CustomerName"].apply(lambda x: re.search("^(\d){5}(\w){3}(\d)", x,re.IGNORECASE)!=None)]["CustomerID"].to_list()

#x extras
aux_list=["asdf","Veracruz","Toluca","Gonzalez","Armando","Bob","Rose",".",
"Various","Lunes","Martes","Armando","36538-36539","morenogirona@gmail.com","SM-EASR-7005-Fronteras"]
idxtra=customer_df[customer_df["CustomerName"].apply(lambda x:x in (aux_list))]["CustomerID"].to_list()

all_removed_ids=id1+id2+id3+id4+id5+id6+id7+id8+id9+id10+id11+id12+id13+id14+id15+id16+id17+id18+id19+idxtra
true_testing_ids=customer_df[customer_df["IsForTesting"]!=0]["CustomerID"].to_list()

customer_df.drop(customer_df[customer_df["CustomerID"].isin(true_testing_ids)].index,inplace=True)
customer_df.drop(customer_df[customer_df["CustomerID"].isin(all_removed_ids)].index,inplace=True)

##################################################################
#limpieza de caracteres especiales
##################################################################

char_replace_dict={'Á': "A", 'Ã':"A",'É':"E", 'Í':"I", 'Ñ':"N", 'Ó':"O", 'Ö':"O",
                   'Ú':"U", 'Ü':"U", 'à':"a", 'á':"a", 'â':"a", 'ã':"a", 'ä':"a", 
                   'è':"e",'é':"e", 'ê':"e", 'ë':"e", 'ì':"i", 'í':"i", 'î':"i", 
                   'ñ':"n", 'ó':"o", 'ô':"o", 'õ':"o", 'ö':"o", 'ú':"u", 'ü':"u",
                   'Ç':'C','ç':'c'}

customer_df["CleanCustomerName"]=customer_df["CustomerName"].replace(char_replace_dict,regex=True)

def clean_special_symbols(df,col="CleanCustomerName"):
    
    #doble , .
    df.loc[:,col]=df[col].apply(lambda x: x.replace(",,",", ").replace("..",".").replace(",",", "))
    #incorporated
    df.loc[:,col]=df[col].apply(lambda x: x.replace("Inc.","inc").replace("inc.","inc"))

    # °,o
    df.loc[:,col]=df[col].apply(lambda x: x.replace("°","o").replace("º","o"))

    # (),[]
    df.loc[:,col]=df[col].apply(lambda x: x.replace("[","(").replace("]",")"))
    #{}
    df.loc[:,col]=df[col].apply(lambda x: x.replace("{","(").replace("}",")")) 
    #hay una entrada que dice "[do not remove]" ??
    #inserta dobles espacios pero los quitaré al final
    df.loc[:,col]=df[col].apply(lambda x: x.replace("("," (").replace(")",") "))
    df.loc[:,col]=df[col].apply(lambda x: x.replace("( ","(").replace(" )",")"))

    # &, cambiar e, y, n', 'n, and, et, por &

    # n', 'n
    df.loc[:,col]=df[col].apply(lambda x: re.sub("\s('n|n')\s",r" & ",x,flags=re.IGNORECASE))
    # and
    df.loc[:,col]=df[col].apply(lambda x: x.replace("S.COOP.AND.","Sociedad Cooperativa Andalucia"))
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(\W+)(and)(\W+|$)", r"\1&\3",x,flags=re.IGNORECASE))
    
    # et (fr), excepto en "et al"
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(\W)([eèéêë]t)(\W|$)(?!al)", r"\1&\3",x,flags=re.IGNORECASE))
    #'CIA EXPORTADORA E IMPOTADORA TAVARE ET . SRL'
    df.loc[:,col]=df[col].apply(lambda x: x.replace("CIA EXPORTADORA E IMPOTADORA TAVARE &","CIA EXPORTADORA E IMPOTADORA TAVARE ET"))

    # y, e (intsertar espacios)
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(Imp\.)(e )",r"\1 \2",x,flags=re.IGNORECASE))
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(\.)(y)",r"\1 \2",x))
    #CIA.DE EXP.Y NEGOCIOS GNRLES.S.A. (insertar espacio)
    df.loc[:,col]=df[col].apply(lambda x: x.replace("CIA.DE EXP.Y NEGOCIOS GNRLES.S.A.", "CIA.DE EXP. Y NEGOCIOS GNRLES.S.A."))

    # cambiar y por & excepto en casos .Y, Y. -y-, y/o, además de los siguientes:
    aux_list=["Mex y Can","Big Y Foods Inc.","M & Y Produce","MEX Y CAN TRADING (1992) INC."]
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(\s)(y)(\s|$)", r"\1&\3",x,flags=re.IGNORECASE) if x not in aux_list else x)

    # '
    #cambiar in' por ing
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(\w)n'\s",r"\1ng ", x,flags=re.IGNORECASE))

    #apostrofé al final de una palabra (no se generaliza ya que hay casos como D' Or)
    df.loc[:,col]=df[col].apply(lambda x: x.replace("SOCIETA'","SOCIETA")) 

    # cambiar ´ (ascento), ` (abrir comilla), ’ (cerrar comilla) por ' (apostrofe)
    df.loc[:,col]=df[col].apply(lambda x: x.replace("´","'").replace("’","'").replace("`","'").replace("INC `","INC"))

    # eliminar dobles comillas “ (abrir), " (cerrar) 
    df.loc[:,col]=df.loc[:,col].apply(lambda x: x.replace('"',"").replace('“',""))

    # eliminar texto entre comillas 'abc'
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(')(\w+)(')",r" \2 ",x))

    # \#
    #change no. \d to #\d
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(\s)(no)(\.?)(\s+)(\d+)", r"\1#\5",x,flags=re.IGNORECASE))
    #change #\s\d to #\d
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(\.?|^)(\w?)(\s?)(#)(\s?)(\d+)",r"\2 #\6",x,flags=re.IGNORECASE).lstrip())

    # _ , –, cambiar (guión bajo y guión largo) por espacio
    df.loc[:,col]=df.loc[:,col].apply(lambda x: x.replace('_'," ").replace("–"," "))
    # cambiar .- por .\s-
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(\.)-(\s?)(\w)", r"\1 - \3",x,flags=re.IGNORECASE))
    # quitar "--"," - "
    df.loc[:,col]=df[col].apply(lambda x: x.replace("--","-").replace(" - "," "))

    # cambiar \w[*]\w por \w-\w
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(\w)[*](\w)", r"\1-\2",x,flags=re.IGNORECASE))
    #quitar los * restantes y cambiar + por \s+\s (se quitan dobles espacios al final)
    df.loc[:,col]=df[col].apply(lambda x: x.replace("*"," ").replace("+"," + "))
    #algunas entradas con + podrían cambiarse a &

    #quitar  %,!
    df.loc[:,col]=df[col].apply(lambda x: x.replace("%","").replace("!",""))

    # ;
    # posesivos mal capturados con ;
    df.loc[:,col]=df[col].apply(lambda x: x.replace(";s","'s"))
    # cambiar ; por ,
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(\W)([ .]?);", r"\1, ",x,flags=re.IGNORECASE))
    df.loc[:,col]=df[col].apply(lambda x: x.replace(";",", "))
        
    #  :
    # eliminar " :" y ".:"
    df.loc[:,col]=df[col].apply(lambda x: re.sub("(\W):", r"\1 ",x,flags=re.IGNORECASE))
    # cambiar : por .
    df.loc[:,col]=df.loc[:,col].apply(lambda x: x.replace(":",". "))
        
    #. , / (demasiados casos, deberían revisarse manualmente uno por uno o no modificarlos)


    #aux_l=df[df[col].apply(lambda x: any(el in ["°","º"] for el in x))]["customerid"].to_list()
    #df[df["customerid"].isin(aux_l)]

    ### espacios (" " vs "\xa0"), basta con codificar el string de manera correcta usando u"..." o r"..."

    ### múltiples espacios contigüos
    df.loc[:,col]=df[col].apply(lambda x: re.sub("\s+"," ",x).lstrip().rstrip())

    return df

customer_df=clean_special_symbols(customer_df,col="CleanCustomerName")
customer_df.loc[:,"CleanCustomerName"]=customer_df["CleanCustomerName"].apply(lambda x: x.lower())

##################################################################
#limpieza y eliminación de abreviaciones
##################################################################

abbreviation_elimination_dict={
#start
"(adm\. & com)(\.)":"", "(\W|^)(a/s)(\.)*(\W|$)":r"\1  \4",
' adm\.':' ', '(^|\s)admora\.':r'\1 ',' agiicola':' ',' ag\. ':' ','(^)agr(\.)':' ',
' agr(\.|$)': ' ','( of ag)(ri)?(\.)?(\W|$)':r" of \4", 'agri\.': ' ', 'agric(\W)':' ','agroind\.':' ',
 '(&) asoc\.': '& ','(^|\W)(asoc)(\.?)(\W)': r'\1 \4', ' assn\.': ' ',' assoc\.': ' ', ' assoc-': ' -',
 ' bro(s?)\.': ' brothers', 'calvi.llo': 'calvillo', ' de cert\.': ' de ', '(&)(\s)*(cia|co)(\.)?(\W|$)':r"\5",
 '(\W|^)cia(\.|\s)': r'\1 ', '(^|\W)(co)(\.)(\w)': r' \4', '(^|\W)(co)(\.)(\W|$)': r'\1 \4', '(\W)(com)(\.)(\w)': r'\1 \4',
 '(\W)(com)(\.)(\W)': r'\1 \4', '& comer\.': '& ','(^|\s)comerc\. &':r'\1 & ', "(^|\W)(co)(-)(op)(\.?)(\W|$)": 
 r"\1 \6", "(^|\W)(soc|sooc|s)(\.?)(\s)(coop)(\.?)(\W|$)": r"\1 \7", "(^|\W)(cal-ore)(\.?)(\W|$)": r"\1 cal-ore \4",
 '(\s)(e)(\s)(com)':r" & \4",'(^|\s)coop\.(\s?)':r'\1 ', 
 '(^|\s)(cor)(\.|\s)*(edu)(\.|\s)*(de la soc)(\.|\s)*(nacio)(\.|\s)*': r'\1coordinacion educativa de la sociedad nacional ',
 '(^|\s)cor\.edu\.': r'\1 cor edu ',
  '(^|\s)corp\.':r'\1 ', '(^|\s)cta\.':r'\1 ', 
 
 # x/y
 '(^|\W)(d)(\.|/|\s)*(b)(\.|/|\s)*(a)(\W)+(\W|\w|$)':r'\1 d/b/a \8', '(\W|^)(prev)(\.?)(\W)':r'\1 previously \4',
 "(\W)c/o(\W|$)":r"\1 \2", "(\W)cc/bk(\W|$)": r"\1 \2", "(\W)o/a(\W|$)":r"\1 operating as \2", 
 "(\W)s/a(\W|$)": r"\1 \2", "(\W)s/n(\W|$)": r"\1 - \2", "(\W)t/a(\W)": r"\1 trading as \2",

#abreviaciones de sociedades
 '(s)(\.|\s)*(a)(\.|\s)*(de|de3)?(\.|\s)*(c)(\.|\s)*(v)(\.|\s)?([/-]|\)|\(|$)': r' \11',
 "(\W)(\.|\s)*(s)(\.|\s)*(de)(\.|\s)*(s)(\.|\s)*(s)(\.)*(\W|$)": r"\1 \11",
 '(s)(\.|\s)*(de)?(\.|\s)*(r)(\.|\s)*(l)(\.|\s)*(de)(\.|\s)*(c)(\.|\s)*(v)(\.)*(\W|d|$)': r" \15", 
 "(\W|^)(s)(\.|\s)*(r)(\.|\s)*(l)(\.|\s)*(\W|$)": r"\1 \8",
 '(s)(\.|\s)*(p)(\.|\s)*(de)(\.|\s)*(r)(\.|\s)*(l)(\.|\s)*(de)(\.|\s)*(c)(\.|\s)*(v)(\.)*(\W|d|$)': r" \17",
 '(s)(\.|\s)*(de)?(\.|\s)*(p)(\.|\s)*(r)(\.|\s)*(de)(\.|\s)*(r)(\.|\s)*(l)(\.)*(\W|d|$)': r" \15",
 "(\W|^)(soc)(\.|\s)*(de)(\.|\s)*(prod|p)(\.|\s)*(rural|r)(\.|\s)*(r)(\.|\s)*(l)(\.)*": r"\1 ",
 "(\W)(\.|\s)*(s)(\.|\s)*(de)(\.|\s)*(p)(\.|\s)*(r)(\.|\s)*(de)(\.|\s)*(r)(\.)*($)": r"\1 ",
 '(s)(\.|\s)*(p)(\.|\s)*(r)(\.)*(l)(\.)*(\W|$)': r" \9", "(^spr|s\.p\.r\.|s, p\.r\.)(\W)": r" \2", "(\W)s\. \. r\.": r"\1 ",
 '(s)(\.|\s)*(de)?(\.|\s)*(p)(\.|\s)*(r)(\.|\s)*(de)(\.|\s)*(r)(\.|\s)*(i)(\.)*(\W|d|$)': r" \15",
 '(s)(\.|\s)*(p)(\.|\s)*(r)(\.|\s)*(de)(\.|\s)*(r)(\.|\s)*(l)(\.|\s)*(de)(\.|\s)*(c)(\.|\s)*(v)(\.)*(\W|$)':r" \19",
"(\W)(s)(\.|\s)*(de)(\.|\s)*(p)(\.|\s)*(r)(\.|\s)*(de)(\.|\s)*(c)": r"\1 ", "(\W)(spr)(\s?)(de|de )?(r|f)([lisf])?(\W|$)": r"\1 \7",
"(\W)(s)(\.|\s)*(de)(\.|\s)*(r)(\.|\s)*(p)(\.|\s)*": r"\1 ",
 "(de)(\.|\s)*(c)(\.|\s)*(v)(\.)*(\W|$)": r" \7", "(^|\W)(s)(\.|\s)*(c)(\.|\s)*(de)(\.|\s)*(r)(\.|\s)*(l)(\.)*(\W|$)": r"\1 \12",
 "s(\.)*p(\.)*r(\.)*$": " ",
 "(\W)(de)(\W)(r)(\.|\s)*(i)(\.|\s)*(\W|$)": r"\1 \8", "(\W)(de)(\W)(r)(\.|\s)*(l)(\.|\s)*(\W||$)": r"\1 \8",
 "(rural|r)(\.|\s)*(de)(\.|\s)*(l)(\.|\s)*(r)(\.)*($|\W)": r"\1 \9",
 "(\W)(s)(\.|\s)*(l)(\.|\s)*(r)(\.)*(\W)": r"\1 \8", "(\W)(r)(\.|\s)*(s)(\.|\s)*(l)(\.)*(\W)": r"\1 \8", 
 "(\s)(s)(\.|\s)+(l)(\.|\s)*(u)(\.|\s)*(\W)": r"\1 \8", "(\s)(s)(\.|\s)+(l)(\.|\s)*(\W|$)": r"\1 \6",
 "(\W)(s)(\.)(p)(\.|\s)*(de)(\W)": r"\1 \7", 
 "(\W)(\.|\s)*(s)(\.|\s)*(c)(\.|\s)*(de)(\.|\s)*(p)(\.)*(\W|$)": r"\1 \11",
 "(\W)(s)(\.|\s)*(a)(\.|\s)*(p)(\.|\s)*(i)(\.)*(\W|$)": r"\1 \10",
 "(\W)(\.|\s)*(s)(\.|\s)*(a)(\.|\s)*(p)(\.|\s)*(l)(\.)*(\W|$)": r"\1 \11",
 "(^|\W)(s)(\.|\s)*(c)(\.|\s)*(l)(\.)*(\W|$)": r"\1 ", 
 "( de c)(\.)($)": "de ", "(\W)(\.|\s)*(s)(\.|\s)*(a)(\.|\s)*(r)(\.|\s)*(l)(\.)*(\W|$)": r"\1  \11",
 "(\W)a\.r\.l(\.|$)": r"\1 ", "(\W|^)s\.c\.p\.p(\.)*(\W|$)": r"\1 \3",
 "(\W)(s)(\.|\s)*(p)(\.|\s)*(p)(\.|\s)*": r"\1 \3", "(\W|^)(\.|\s)*(s)(\.|\s)*(c)(\.|\s)*(a)(\.|\s)*(\W|$)": r"\1 \9",
 "(\W|^)(soc|sooc|s)(\.|\s)*(en)(\.|\s)*(c)(\.|\s)*(\W|$)": r"\1  \8",
 "(\W|^)(soc|sooc|s)(\.|\s)*(en)(\.|\s)*(c)(\.|\s)*(s)(\W|$)": r"\1 \9", 
"(\W|^)(s)(\.|\s)+(p)(\.|\s)*(a)(\.|\s)*(\W|$)": r"\1  \8",
"(\W|^)(sp)(\.|\s)*(a)(\.|\s)*(\W|$)": r"\1 \6",
"(^)(s)(\.|\s)+(c)(\.|\s)*(i)(\.|\s)*(\W|$)":r" \8",

"(\W|^)(soc|sooc|s)(\.|\s)*(e)(\.|\s)*(c)(\.)*(\W|$)": r"\1 \8",
"(\W|^)(\.|\s)*(s)(\.|\s)*(n)(\.|\s)*(c)(\.|\s)*(\W|$)":r"\1  \9",
"(\W|^)(s)(\.|\s)+(r)(\.|\s)*(o)(\.|\s)*(\W|$)": r"\1  \8",
"(\W|^)(s)(,|\.|\s)+(e)(,|\.|\s)*(\W|$)": r"\1  \6",
"(\W)(s)(\.)(s)(\.)(\W)": r"\1 \6",
"(\W)(sp)(\.|\s)*(z)(\.|\s)*(o)(\.|\s)*(o)(\.|\s)*(\W|$)": r"\1  \10",

"(\W|^)(s)(\.|\s)+(c)(\.|\s)*(s)(\.|\s)*($)": r"\1  ",
"(\W)(s)(\s)+(a)(\s)+(c)(\.|\s)*($)": r"\1 ", "(\W)(sr)(\W)":r"\1  \3",
"(\W|^)(\.|\s)*(s)(\.|\s)*(a)(\.)*(c)(\.)*([-()/]|\s|$)": r"\1 \9",
"(\W|^)(\.|\s)*(s)(\.|\s)*(a)(\.)*(s)(\.)*([-()/]|\s|$)": r"\1  \8",
"(\W|farms)(\.|\s)*(s)(\.|\s)*(a)(\.|,|\s)*(\W|$)": r"\1  \7",  
"(\W|^)(uepic sra)(\s)": r"\1 uepic ",
"(\W)(pr)(\.)(\W)": r"\1 \4", 

#continuation
'(^|\s)dept\.': r'\1 ', '(^|\s)dist\.':r'\1 ',
'(^|\s)div\.':r'\1 ','(^|\W)(dr)(\.)': r'\1 ', '(edms)(\.?)': '', 'bpk': '', 'edo\.':'',
'(^|\s)eirl\.': r'\1 ', '(^|\s)elab\.': r'\1 ', 'eng\.': ' ', 'enr\.': ' ',
'ent\.': ' ', "exp\. e imp\. manobal":" manobal", '(^|\s)(exp)(\.)(e|\s)*(imp)(\.?)': r'\1 ',
'( e)?(^|\s)(exp)(\.)(e|\s)*(imp)(\.?)': r'& ', '(imp)(\.?)(\s?)(\w?)(\.?)(\s?)(exp)(\W)': r'  ',
'(\W|^)(imp|importacao|importacion)(\.?)(\s?)(e?)(\.?)(\s?)(exp|exportacao|exportacion)(\W|$)': r' ','(imp)(\.?)(\s?)(&)(\s?)(exp)(\W)':r' ', 
'(\W|^)(prod)(\.|\s)*(&)(\.|\s)*(export)(\.)?(\W)': r'\1 \8',
"(\W|^)(prod)(\.?)(\W)": r"\1 produccion \4", "(\W|^)(prodcue)(\.?)(\W)": r"\1 produce \4",  "(\W|^)(produc)(\.)(\W)": r"\1 \4",
"(\W)(famrs)(\W)": r"\1 farms \3", '(^|\W)fco(\.)': r'\1 francisco ', '(\W)(fdo)(\W)': r'\1 fdo.\3', "(^|\W)for(\.)":r"\1 ",
"(^|\W)(frut)(\.)": r"\1 ", "(^|\W)gan(\.)":r"\1 ", '(^|\W)(gnrles)(\W|$)': r'\1 \3', "farms gp\.": "",
"(^|\W)groc\.": r"\1 ", "(^|\W)hnos(\.|\s)":r"\1 hermanos ", "(\W)(inc)(\.?)(\d|\W|$)":r"\1 \4",
'(^|\W)ind\.': r'\1 ', '(^)(ing)(\.)': ' ', "(\W|^)(int)('|\.|,|\s)*(l)?(\.|,)?(\W|$)": r"\1 \6", "(^|\s)(inv)(\.)":r"\1 ",
"(^|\W)(jr)(\.)": r"\1 junior", "(^|\W)(labr)(\.)": r"\1 ", "(^|\W)(lcc)(\.|$)": r"\1 ", "(^|\W)(lc)(\.|$)": r"\1  ",
"(^|\W)(e)(\.|\s)*(i)(\.|\s)*(r)(\.|\s)*(l)?(\W|$)": r"\1 \9",
"(^|\W)(e)(\.|\s)*(i)(\.|\s)*(r)(\.|\s)*(e)(\.|\s)*(l)(\.|\s)*(i)(\W|$)": r"\1 \13",

#limited liability company, etc.
"(\W|^)(tic)(\.|\s)*(ltd)(\.|\s)*(sti)(\.|\s)*(\W|$)": r"\1 \8",
"(\W)(l)(\.|\s)*(l)(\.|\s)*(c)(\.)*(\d|\W|$)": r"\1 \8",
"(\W)(l)(\.|\s)*(l)(\.|\s)*(p)(\.*)(\W|$)": r"\1 \8",
"(\W)(l)(\.|\s)*(l)(\.|\s)*(l)(\.|\s)*(p)(\.)*(\W|$)": r"\1  \10", 
"(\W)(l)(\.|\s)*(p)(\.)*(\W|$)": r"\1  \6", #ltdtda = ltda
"(agricola)(\W)(l)(\.|\s)*(c)(\.)*(\W|$)": r"\1\2 l,c\7", #agricola lc
"(\W)(l)(\.|\s)*(c)(\.)*(\W|$)": r"\1  \6", 
"(\W|^)(l)(\.|\s)*(t)(\.|\s)*(d)(\.)?(\W|$)": r"\1  \8",
"(\W)(lmtda)(\.?)(\W|$)": r"\1  \4", "(\W)(ltda)(\.?)(\W|$)": r"\1  \4", 
"(\W)(itda)(\.?)(\W|$)": r"\1  \4", 

#continuacion
 "(tech)(\s)*(l)(\.|\s)+(a)(\.|\s)*(s)": r"\1 s",
 "(^|\W)(ma)(\.?)(\W)": r"\1 maria \4", "(^|\W)(manf)(\.?)(\W|$)": r"\1 \4",
 "(\W)(manofact)(\.?)": r"\1 ", "(\W)(mfg)(\.?)(\W|$)": r"\1 \4", "(\W)(mgt)(\.?)(\W|$)": r"\1 \4",
 "(\W)(mkt)(\.?)(\W|$)": r"\1  \4", "(^|\W)(mpio)(\.?)(\W|$)": r"\1 municipio \4", "(^|\W)(mr)(\.?)(\W|$)": r"\1 mr. \4", #mr. & mrs. formating
 "(^|\W)(mrs)(\.)": r"\1 mrs. ", "(^|\W)(mt)(\.?)(\s)(view)(\W|$)": r"\1 mountain view \6" , "(^|\W)(mt)(\.)(\W)": r"\1 mount \4",
 "(^|\W)(mt)(\s)": r"\1 mount ", "(^|\s)(mount|mt)( farms)": r"\1 mt farms", "(mount|mt) s.p.a.": "mt s.p.a.", #works somehow
 "(^|\W)(mtn)(\.?)(\W|$)": r"\1 mountain \4", "(^|\W)(mvz)(\.?)(\W|$)": r"\1 medico veterinario zootecnista \4", 
 "(^|\W)(ntra)(\.?)(\W|$)": r"\1 nuestra \4", "\(org\.\)": " ", "(^|\W)(org)(\.?)(\s)(de cert)(\W|\w)": r"\1 \6", 
 "(sonora, ac)": "sonora", "(^|\W)(pkg)(\.?)(\W|$)": r"\1 \4", "(\W|^)(prov)(\.?)(\W|$)": r"\1 prov \4", "(\W|^)(pty)(\.?)(\W|$)":r" \1 \4",
 "(\W|^)(pvt)(\.?)(\W|$)": r"\1 \4", "(\W|^)(rd)(\.)(\W|$)": r"\1 \4", "(\W|^)(sta)(\.?)(\W|$)":r"\1 \4", "(\W|^)(suc)(\.?)(\W|$)": r"\1 \4",
"(\W|^)(svc)(\.?)(\))": r"\1 \4", "(\W|^)(sys)(\.)(\W)":r"\1 \4", "(\W)(trans)(\.?)(\W|$)": r"\1transports \4", "(\W)(veg)(\.|\s)": r"\1 vegetable",

 "(\W)(st)(\.)(\s)(louis)(\W|$)": r"\1 saint louis \6",
 "(\W)(st)(\.)(\s)(michael)(\W|$)": r"\1 saint michael \6", "(\W)(st)(\.)(\W|$)":r"\1 street \4",

"(\W|^)(s)(,|\.|\s)+(c)(,|\.|\s)*(\W|$)": r"\1 \6",
 '(^|\s)(a)(\.)(\s?)(c)(\.?)(\W|^)': r'\1  \7',
 "(\s|\.|,|^)(s)(,|\.|\s)+(de)(\W)": r'\1  \5',
"(o &)(\s)(c)(\.)(\s)(s)": r'\1 s',
"(\W)(co)(\.)?($)": r"\1",
"(\W)(company)(\.)?(\W|$)": r"\1 \4",
"(\W)(limitada)(\.)?($)": r"\1",

#titulos no-abreviados

"(\W|^)(agricola)(\s|\.)*(&)(\s|\.)*(comercial|comercializadora)(\W|$)": r"\1 \7",
"(\W|^)(maquiladora [&ey] comercializadora)( de)?(\W|$)":r"\1 \4",
#"(\W|^)(grupo industrial [&ey] comercial)( de)?(\W|$)": r"\1 \4",
"(\W|^)(industrial)(\s|\.)*([&ey])?(\s|\.)*(comercial)(\W|$)":r"\1 \7",
"(\W|^)(sociedad comercial [&ey] de inversiones)( de)?(\W|$)":r"\1 \4",
"(\W|^)(comercializadora de productos [&ey] servicios)( de)?(\W|$)":r"\1 \4",

#comercializadora
"(\W|^)(productora [&ey] comercializadora|productora [&ey] comercial)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(comercializadora [&ey] productora|comercial [&ey] productora)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(exportadora [&ey] comercializadora|exportadora [&ey] comercial)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(comercializadora [&ey] exportadora|comercial [&ey] exportadora)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(distribuidora [&ey] comercializadora|distribuidora [&ey] comercial)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(comercializadora [&ey] distribuidora|comercial [&ey] distribuidora)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(procesadora [&ey] comercializadora|procesadora [&ey] comercial)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(comercializadora [&ey] procesadora|comercial [&ey] procesadora)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(cosechadora [&ey] comercializadora|cosechadora [&ey] comercial)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(comercializadora [&ey] cosechadora|comercial [&ey] cosechadora)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(empacadora [&ey] comercializadora|empacadora [&ey] comercial)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(comercializadora [&ey] empacadora|comercial [&ey] empacadora)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(administradora [&ey] comercializadora)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(comercializadora [&ey] administradora)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(agroexportadora [&ey] comercializadora)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(comercializadora [&ey] agroexportadora)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(forestal [&ey] comercial)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(comercial [&ey] forestal)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(inmobiliaria [&ey] comercial)( agricola)?( de)?(\W|$)":r"\1 \5",
"(\W|^)(comercial [&ey] inmobiliaria)( agricola)?( de)?(\W|$)":r"\1 \5",

"(\W|^)(agroindustrial [&ey] comercial|comercial [&ey] agroindustrial)(\W|$)":r"\1 \3",
"(\W|^)(consultoria & asesoria|asesoria & consultoria)(\W|$)":r"\1 \3",
"(\W|^)(corporacion comercial)(\W|$)":r"\1 \3",
"(\W|^)(industrial comercial)(\W|$)":r"\1 \3",
"(\W|^)(comercial [&ey] fruticola)(\W|$)": r"\1 \3",
"(\W|^)(empresa comercializadora)(\W|$)": r"\1 \3",
"(\W|^)(grupo comercial)(\W|$)": r"\1 \3",
"(\W|^)(agricola , ganadera , comercial , industrial , forestal [&ey] transporte)( de)?(\W|$)":r"\1 \4",
"(\W|^)(comercializadora agropecuaria)(,)?(\W|$)":r"\1 \4",
"(\W|^)(comercial|comercializadora)( de)(\W|$)":r"\1 \4",

"(^|\W)(agricola)(,|\s|\.)*(comercial)(,|\s|\.)*(servicios)(,|\s|\.)*([ey&])(,|\s|\.)*(inversiones)(\W|$)":r"",

#sociedades
"(^|\W)(soc|sooc)(\.|\s)*(\W|$)": r"\1 \4",
"(^|\W)(sociedad|s)*(\s|\.)*(de)?(inversiones)(\s|\.)*(agricolas)(\W|$)":r"\1 \8",
"(^|\W)(sociedad|s)*(\s|\.)*(anonima|anonina)(\s|\.)*(cerrada)?(\W|$)":r"\1 \7",
"(^|\W)(sociedad|s)*(\s|\.)*(comercial)(\s|\.)*([&ey])(\s|\.)*(agricola)(,)?(\W|$)":r"\1 \10", 
"(^|\W)(sociedad|s)*(\s|\.)*(cooperativa|coop)(\W|$)":r"\1 \5",
"(^|\W)(sociedad|s)*(\s|\.)*(civil)(\W|$)":r"\1 \5",
"(^|\W)(sociedad|s)*(\s|\.)*(por)?(\s|\.)*(acciones)(\s|\.)*(simplificada|simplificadas)?(\W|$)":r"\1 \9",
"(^|\W)(sociedad|s)*(\s|\.)*(agropecuaria|agropecuarias)(\s|\.)*(&)?(\s|\.)*(ganadera|gan)(\W|$)":r"\1 \9",
"(^|\W)(sociedad|s)*(\s|\.)*(agropecuaria|agropecuarias)(\s|\.)*(&)?(\s|\.)*(forestal|fore)(\W|$)":r"\1 \9",
"(^|\W)(sociedad|s)(\s|\.)*(agricola)(,)?(\W|$)":r"\1 \6", #agricola
"(^|\W)(sociedad)(\W|$)":r"\1 \3",

#prestadoras de servicios
"(\W|^)(prestadora|pres)(\s|\.)*(de)?(\s|\.)*(servicios)(\s|\.)*([ey&])(\s|\.)*(procesadora|procesarora|inversiones)(\W|$)":r"\1 \11",
"(\W|^)(prestadora|pres)(\s|\.)*(de)?(\s|\.)*(servicios)(\W|$)":r"\1 \7",

#exportacao e importacao
"(\W|^)(importadora & exportadora agricola)(\W|^)":r"\1 importadora &: exportadora agricola \3",
"(\W|^)(producao|produccion|productora)(,|\s|\.)*(importadora [&ey] exportadora|importacion [&ey] exportacion|importacao [&ey] exportacao)( comercial)?(\W|$)": r"\1 \6",
"(\W|^)(producao|produccion|productora)(,|\s|\.)*(exportadora [&ey] importadora|exportacion [&ey] importacion|exportacao [&ey] importacao)( comercial)?(\W|$)": r"\1 \6",
"(\W|^)(importadora [&ey] exportadora|importacion [&ey] exportacion|importacao [&ey] exportacao)( comercial)?( de)?(\W|$)": r"\1 \5",
"(\W|^)(exportadora [&ey] importadora|exportacion [&ey] importacion|exportacao [&ey] importacao)( comercial)?( de)?(\W|$)": r"\1 \5",
"(\W|^)(distribuidora [&ey] exportadora|distribucion [&ey] exportacion|distribuicao [&ey] exportacao)( comercial)?( de)?(\W|$)": r"\1 \5",
"(\W|^)(exportadora [&ey] distribuidora|exportacion [&ey] distribucion|exportacao [&ey] distribuicao)( comercial)?( de)?(\W|$)": r"\1 \5",
"(\W|^)(exportadora|exportacion|exportacao)(,|\s|\.)*([&ey])?(,|\s|\.)*(importadora|importacion|importacao)(,|\s|\.)*([&ey])?(\W|$)": r"\1 \9",
"(\W|^)(importadora|importacion|importacao)(,|\s|\.)*([&ey])?(,|\s|\.)*(exportadora|exportacion|exportacao)(,|\s|\.)*([&ey])?(\W|$)": r"\1 \9",


#location abbreviations
' ca\.': ' california', "(\W)gto(\W|$)": r"\1guanajuato\2",
 "(\W|^)(l)(\.|\s)+(a)(\.|\s)*(\W|$)":r"\1 los angeles \6","(\W)(mo)(\.?)($)": r"\1 missouri", 
 "(\W)(ma)(\.?)($)": r"\1 massachusetts \4","(^|\W)(mo)(\.)(\W)": r"\1 missouri \4", "(^|\W)(mt)($)": r"\1 montana", 
 "(\W)(ny)(\.?)(\W|$)":r"\1 new york \4", "(\W|^)(pue)(\.?)(\W|$)": r"\1 puebla \4", "(\W)(s)(\.)(f)(\.)?($)":r"\1 san francisco",
 "(\W)(tn)(\.?)($)": r"\1 tennessee \4", "(\W)(tx)(\.?)(\W|$)": r"\1 texas \4",
 "(^|\s)\.(\s|$)":" ","\((\s|\.)*\)":" " , '(\s)+': ' ', "(<|>)":"/", "(\w)(@)(.)+":r"\1", "(\s)+(,)(\s)":r"\1\3", "(,)(\s)*($)":"", "&($)": "",
 }

customer_df["CleanCustomerName3"]=customer_df["CleanCustomerName"].replace(abbreviation_elimination_dict,regex=True) 
customer_df.loc[:,"CleanCustomerName3"]=customer_df["CleanCustomerName3"].apply(lambda x: x.lstrip().rstrip().replace(" , "," ").replace("( ","(").replace(" )",")").replace("  "," "))


##################################################################
#definicion de funciones de similitud
##################################################################

def jaccard_similarity(s1, s2):
    if type(s1)==str and type(s2)==str:
        intersection = set(s1).intersection(set(s2))
        union = s1 + " " + s2 #concatenated strings
        if "**" in s1 or "**" in s2:
            intersection=set()
    elif type(s1)==set and type(s2)==set:
        intersection = s1.intersection(s2)
        union = s1.union(s2) #unique characters
        if "*" in intersection:
            intersection=set()
    else:
        raise TypeError("both arguments must be of the same type")
    return len(intersection)/len(union)

def overlap_coefficient(s1,s2):
    if type(s1)==str and type(s2)==str:
        intersection = set(s1).intersection(set(s2))
        min_length=min(len(s1),len(s2)) #string length
    elif type(s1)==set and type(s2)==set:
        intersection = s1.intersection(s2) 
        min_length=min(len(s1),len(s2)) #no of unique characters
    else:
        raise TypeError("both aruments must be of the same type")
    return len(intersection)/min_length

def sorensen_dice_coefficient(s1, s2):
    if type(s1)==str and type(s2)==str:
        intersection = set(s1).intersection(set(s2))
        len1=len(s1)
        len2=len(s2)
    elif type(s1)==set and type(s2)==set:
        intersection = s1.intersection(s2)
        len1=len(s1)
        len2=len(s2)
    else:
        raise TypeError("both arguments must be of the same type")
    return 2*len(intersection)/(len1+len2)

def relative_hamming_distance(s1, s2):
    dist_counter = 0
    total_length = len(s1) + len(s2)
    if type(s1)==str and type(s2)==str:
        if len(s1)==len(s2):
	        dist_counter = sum(xi != yi for xi, yi in zip(s1, s2))
            #for n in range(len(s1)):
	        #	if s1[n] != s2[n]:
	        #		dist_counter += 1
        else: #different legnth: fill with spaces
            if len(s1)<len(s2):
                short_string=s1
                long_string=s2
            else:
                short_string=s2
                long_string=s1
            short_string+=" "*(len(long_string)-len(short_string))
            dist_counter = sum(xi != yi for xi, yi in zip(short_string, long_string))
    elif type(s1)==set and type(s2)==set:
        if len(s1)==len(s2):
	        dist_counter = sum(xi != yi for xi, yi in zip(s1, s2))
        else:
            if len(s1)<len(s2):
                short_set=s1
                long_set=s2
            else:
                short_set=s2
                long_set=s1
            dist_counter=(s1.union(s2)-s1.intersection(s2))/2
    else:
        raise TypeError("both arguments must be of the same type")
    return dist_counter/total_length

def relative_hamming_similarity(s1,s2):
    return 1-relative_hamming_distance(s1, s2)


def relative_Levenshtein_distance(s1,s2):
    if type(s1)==set and type(s2)==set:
        s1=''.join(sorted(list(s1))) #sort and conver to string
        s2=''.join(sorted(list(s2)))
    if type(s1)==str and type(s2)==str:
        n,m=len(s1),len(s2)
        d = np.zeros([n+1,m+1],dtype=int) #initialize distance matrix
        d[:,0]=np.arange(0,n+1,1,dtype=int)
        d[0,:]=np.arange(0,m+1,1,dtype=int)
        for j in range(1,m+1):
            for i in range(1,n+1):
                if s1[i-1]==s2[j-1]:
                    substitutionCost = 0
                else:
                    substitutionCost = 1
        
                d[i, j] = min(d[i-1, j] + 1,                   # deletion
                             d[i, j-1] + 1,                   # insertion
                             d[i-1, j-1] + substitutionCost)  # substitution
    else:
        raise TypeError("both arguments must be of the same type")
    return d[n,m]/max(n,m)

def relative_Levenshtein_similarity(s1,s2):
    return 1-relative_Levenshtein_distance(s1, s2)


def relative_Levenshtein_Damerau_dist(s1,s2):
    if type(s1)==set and type(s2)==set:
        s1=''.join(sorted(list(s1))) #sort and convert to string
        s2=''.join(sorted(list(s2)))
    if type(s1)==str and type(s2)==str:
        n,m=len(s1),len(s2)
        d = np.zeros([n+1,m+1],dtype=int) #initialize distance matrix
        d[:,0]=np.arange(0,n+1,1,dtype=int)
        d[0,:]=np.arange(0,m+1,1,dtype=int)
        for j in range(1,m+1):
            for i in range(1,n+1):
                if s1[i-1]==s2[j-1]:
                    substitutionCost = 0
                else:
                    substitutionCost = 1
        
                d[i, j] = min(d[i-1, j] + 1,                   # deletion
                             d[i, j-1] + 1,                   # insertion
                             d[i-1, j-1] + substitutionCost)  # substitution
                if i > 1 and j > 1 and s1[i-1] == s2[j-2] and s1[i-2] == s2[j-1]:
                    d[i, j] == min(d[i, j], d[i-2, j-2] + 1)  # transposition
                    """
                    try:
                        if s1[i-1] == s2[j-2] and s1[i-2] == s2[j-1]: #
                            d[i, j] == min(d[i, j],
                                            d[i-2, j-2] + 1)  # transposition
                    except:
                        print(i,j, s1[i-1], s2[j-2],s2[i-2], s2[j-1])
                    """
    else:
        raise TypeError("both arguments must be of the same type")
    return d[n,m]/max(n,m)

def relative_Levenshtein_Damerau_similarity(s1,s2):
    return 1-relative_Levenshtein_Damerau_dist(s1, s2)


def relative_Levenshtein_similarity2(s1,s2):
    if "**" in s1 or "**" in s2:
        return 0
    else:
        return 1-lev.distance(s1,s2)/max(len(s1),len(s2))


def relative_Levenshtein_Damerau_similarity2(s1,s2):
    if "**" in s1 or "**" in s2:
        return 0
    else:
        return 1-lev_dam.damerau_levenshtein_distance(s1,s2)/max(len(s1),len(s2))


##################################################################
#import new and format client data
##################################################################

# data_file="../data/original data/new customers/"
# new_files_list=os.listdir(data_file)
# new_files_list=[f for f in new_files_list if ("~$" not in f) and ("new" not in f) and ("New" not in f)][-1:] #only latest report

# aux_list=[]
#for f in new_files_list:
    #print(data_file+f)
#    df=pd.read_excel(data_file+f)
    #df=pd.read_excel(data_file+f,sheet_name="Similarity")
    #print(df.shape)
#    aux_list.append(df)
objConnCann = asql.fnConnect(objCFG["SQL"]["messy"]["connectionstr"])
strQuery = objCFG["SQL"]["messy"]["query"]

new_customers_df = pd.read_sql(strQuery, objConnCann)
# new_customers_df=pd.concat(aux_list)
new_customers_df.dropna(subset=["CustomerID"],inplace=True)
new_customers_df=new_customers_df[new_customers_df.columns[:-6]]
new_customers_df.drop_duplicates(inplace=True)
print(new_customers_df.shape)

new_customers_df["CleanCustomerName"]=new_customers_df["CustomerName"].replace(char_replace_dict,regex=True)
new_customers_df.loc[:,"CleanCustomerName"]=clean_special_symbols(new_customers_df,col="CleanCustomerName")
new_customers_df.loc[:,"CleanCustomerName"]=new_customers_df["CleanCustomerName"].apply(lambda x: x.lower())
new_customers_df["CleanCustomerName2"]=new_customers_df["CleanCustomerName"].replace(abbreviation_replacement_dict,
regex=True).apply(lambda x:x.replace(" . "," ").replace("  "," ").lstrip().rstrip())
new_customers_df["CleanCustomerName3"]=new_customers_df["CleanCustomerName"].replace(abbreviation_elimination_dict,
regex=True).apply(lambda x:x.replace(" . "," ").replace("  "," ").lstrip().rstrip())


#split search terms to find more candidates
alias_dict={
    "(doing business as|d/b/a)":"_","formerly":"_","(\W)former(\W)":r"\1_\2","previously":"_", "(\W)aka(\W)":"\1_\2","operating as": "_", "trading as":"_",
    "/":"_", "h_a": 'h/a ', "i_e":' i/e','in_out':'in/out ',"t_a":'t/a ',"y_o":' y/o ',"_a_can":'/a/can', "\(":"_", "\)":"_", "_(.)+_":"_",
    "(\s)+(\.)(\s|$)": "",
    #"(\W)([a-z]){3,20}/([a-z]){3,20}(\W|$)":r"\1\2 _ \3\4",
}
#not splitting parenthesis
aux_list=new_customers_df["CleanCustomerName3"].replace(alias_dict,regex=True).to_list()
aux_list2=new_customers_df["CleanCustomerName3"].to_list()
split_names_list=[]
for i,name in enumerate(aux_list):
    original_name=aux_list2[i]
    new_names=[n for n in name.split("_") if len(n)>2]
    split_no=len(new_names)
    if split_no>1:
        split_names_list.append([original_name]+name.split("_"))
    else:
        split_names_list.append([original_name])

cleanup_dict={"\((\s)*\)":" ","(,|\.|-|/)$":""}

aux_df=pd.DataFrame(split_names_list)
aux_df["CustomerID"]=new_customers_df["CustomerID"].to_list()
value_vars_list=[var for var in aux_df.columns.to_list() if type(var)==int]
aux_df=aux_df.melt(id_vars=["CustomerID"],value_vars=value_vars_list).sort_values(by=["CustomerID","variable"]).dropna()
aux_df.columns=["CustomerID","variable","split_names"]
aux_df.loc[:,"split_names"]=aux_df["split_names"].replace(cleanup_dict,regex=True)
aux_df.drop(aux_df[aux_df["split_names"].apply(lambda x:len(x)<2)].index,inplace=True)
aux_df.loc[:,"split_names"]=aux_df.loc[:,"split_names"].apply(lambda x: x.replace(" . "," ").replace("  "," ").lstrip().rstrip())
aux_df=aux_df[["CustomerID","split_names"]].reset_index(drop=True)
#print(aux_df.shape)
new_customers_df2=new_customers_df.merge(aux_df,how="outer",on="CustomerID")
#print(aux_df.shape,new_customers_df2.shape)

##################################################################
#merge new client data and complete data catalogue
##################################################################

import thefuzz.fuzz as fuzzy

location_vars=['CustomerID','CustomerName','CleanCustomerName','CleanCustomerName2','CleanCustomerName3',
'CountryID','InsideStateID','CityID','Address','Email','PostalCode','PhoneNumber','FaxNumber']

#merged_df=new_customers_df.merge(customer_df[location_vars],how="left",on=["CountryID","InsideStateID","CityID"])
merged_df=new_customers_df2.merge(customer_df[location_vars],how="left",on=["CountryID"],suffixes=["_new","_old"])
new_ids_list=new_customers_df2["CustomerID"].astype(int).to_list()

#remove duplicate new customers and empty name columns
merged_df.drop(merged_df[merged_df["CustomerID_old"].isin(new_ids_list)].index,inplace=True)
merged_df.drop(merged_df[merged_df["CustomerID_new"].isna()].index,inplace=True)

merged_df["CustomerID_pair"]=merged_df["CustomerID_new"].apply(lambda x: str(x).zfill(5)+" ")\
    +merged_df["CustomerID_old"].apply(lambda x: str(x).zfill(5))


#initial fuzzy similarity scores
new_names_list=merged_df["split_names"].to_list()
old_names_list=merged_df["CleanCustomerName3_old"].to_list()
old_names_list=["*******" if type(s)!=str else s for s in old_names_list] #replace nans

res_token_set=[fuzzy.token_set_ratio(s1,s2)/100 for s1,s2 in zip(new_names_list,old_names_list)]
merged_df["fuzzy_set_score"]=res_token_set

##################################################################
#name similarity scoring
##################################################################

import Levenshtein as lev
import pyxdameraulevenshtein as lev_dam
from joblib import Parallel, delayed

res_df=merged_df.drop(merged_df[merged_df["fuzzy_set_score"]<=0.725].index,inplace=False).copy()
new_names_list=res_df["split_names"].to_list()
old_names_list=res_df["CleanCustomerName3_old"].to_list()
old_names_list=["*******" if type(s)!=str else s for s in old_names_list] #replace nans

#regular name scoring
res_jaccard_list=[jaccard_similarity(set(s1),set(s2)) for s1,s2 in zip(new_names_list,old_names_list)]
res_overlap_list=[overlap_coefficient(set(s1),set(s2)) for s1,s2 in zip(new_names_list,old_names_list)]
res_sorensen_list=[sorensen_dice_coefficient(set(s1),set(s2)) for s1,s2 in zip(new_names_list,old_names_list)]

res_hamming_list=[relative_hamming_similarity(s1,s2) for s1,s2 in zip(new_names_list,old_names_list)]

res_levenshtein_list=[1-lev.distance(s1,s2)/max(len(s1),len(s2)) for s1,s2 in zip(new_names_list,old_names_list)]
res_lev_damerau_list=[1-lev_dam.damerau_levenshtein_distance(s1,s2)/max(len(s1),len(s2)) for s1,s2 in zip(new_names_list,old_names_list)]
#res_levenshtein_list=Parallel(n_jobs=-1)(delayed(relative_Levenshtein_similarity)(s1,s2) for s1,s2 in zip(new_names_list,old_names_list))
#res_lev_damerau_list=Parallel(n_jobs=-1)(delayed(relative_Levenshtein_Damerau_similarity)(s1,s2) for s1,s2 in zip(new_names_list,old_names_list))

scores_results=[res_jaccard_list,res_overlap_list,res_sorensen_list,res_hamming_list,res_levenshtein_list,res_lev_damerau_list]
scores_array=np.array(scores_results)

average_score=list(np.mean(scores_array,axis=0))
scores_results.append(average_score)
max_score=list(np.max(scores_array,axis=0))
scores_results.append(max_score)
min_score=list(np.min(scores_array,axis=0))
scores_results.append(min_score)

#ordered set scores
def ordered_set_scoring(string1,string2,function,input_type=set):
    s1=set(string1.replace("(","").replace(")","").split(" "))
    s2=set(string2.replace("(","").replace(")","").split(" "))
    s0=s1&s2

    if input_type==str:
        s1=' '.join(sorted(list(s1)))
        s2=' '.join(sorted(list(s2)))
        s0=' '.join(sorted(list(s0)))
    
    try:
        t0=function(s1,s2)
    except:
        t0=0
    try:
        t1=function(s0,s1)
    except:
        t1=0
    try:
        t2=function(s0,s2)
    except:
        t2=0
    return max(t0,t1,t2)


res_ordered_set_jaccard_list=[ordered_set_scoring(s1,s2,jaccard_similarity,input_type=set) for s1,s2 in zip(new_names_list,old_names_list)]
res_ordered_set_overlap_list=[ordered_set_scoring(s1,s2,overlap_coefficient,input_type=set) for s1,s2 in zip(new_names_list,old_names_list)]
res_ordered_set_sorensen_list=[ordered_set_scoring(s1,s2,sorensen_dice_coefficient,input_type=set) for s1,s2 in zip(new_names_list,old_names_list)]

res_ordered_set_hamming_list=[ordered_set_scoring(s1,s2,relative_hamming_similarity,input_type=str) for s1,s2 in zip(new_names_list,old_names_list)]

res_ordered_set_levenshtein_list=[1-ordered_set_scoring(s1,s2,lev.distance,input_type=str)/max(len(s1),len(s2)) for s1,s2 in zip(new_names_list,old_names_list)]
res_ordered_set_lev_damerau_list=[1-ordered_set_scoring(s1,s2,lev_dam.damerau_levenshtein_distance,input_type=str)/max(len(s1),len(s2)) for s1,s2 in zip(new_names_list,old_names_list)]

ordered_set_scores_results=[res_ordered_set_jaccard_list,res_ordered_set_overlap_list,res_ordered_set_sorensen_list,
res_ordered_set_hamming_list,res_ordered_set_levenshtein_list,res_ordered_set_lev_damerau_list]
ordered_set_scores_array=np.array(ordered_set_scores_results)

average_score=list(np.mean(ordered_set_scores_array,axis=0))
ordered_set_scores_results.append(average_score)
max_score=list(np.max(ordered_set_scores_array,axis=0))
ordered_set_scores_results.append(max_score)
min_score=list(np.min(ordered_set_scores_array,axis=0))
ordered_set_scores_results.append(min_score)


#gather and format scoring results
scoring_results_df=pd.DataFrame(scores_results).T
metrics_used=["Jaccard","Overlap","Sorensen-Dice","Hamming","Levenshtein","Levenshtein-Damerau","average","max","min"]
metric_vars=[s+"_score" for s in metrics_used]
scoring_results_df.columns=metric_vars

ordered_set_scoring_results_df=pd.DataFrame(ordered_set_scores_results).T
ordered_set_metric_vars=[s+"_ordered_set_score" for s in metrics_used]
ordered_set_scoring_results_df.columns=ordered_set_metric_vars

res_df=pd.concat([res_df.reset_index(drop=True),scoring_results_df.reset_index(drop=True),ordered_set_scoring_results_df.reset_index(drop=True)], axis=1)


##################################################################
#contact info similarity
##################################################################

#email, address, location, postal code, phone number
contact_info_vars=[]

def clean_info_to_str(x):
    if (type(x)==str and len(x)<=2) or x in [np.nan,"nan","NA","N/A","n/a","  .","NAN",0,"0"] or pd.isnull(x)==True:
        x="******"
    #if type(x)==float:
    #    x=int(x)
    new_x=str(x).lstrip().rstrip()
    if len(''.join(set(new_x)))<=1:
        new_x="******"
    return new_x

#jaccard address,zipcode similarity
for var in ["Address","PostalCode"]:
    new_var=var+"_new"
    old_var=var+"_old"

    new_var_list=res_df[new_var].apply(clean_info_to_str).to_list()
    old_var_list=res_df[old_var].apply(clean_info_to_str).to_list()

    var_jaccard_similarity=[]
    for a1,a2 in zip(new_var_list,old_var_list):
        try:
            var_jaccard_similarity.append(jaccard_similarity(set(a1),set(a2)))
        except:
            var_jaccard_similarity.append(np.nan)
    res_df[var+"_jaccard_score"]=var_jaccard_similarity
    contact_info_vars.append(var+"_jaccard_score")

    #res_levenshtein_list=[relative_Levenshtein_similarity2(s1,s2) for s1,s2 in zip(new_var_list,old_var_list)]
    res_lev_damerau_list=[relative_Levenshtein_Damerau_similarity2(s1, s2) for s1,s2 in zip(new_var_list,old_var_list)]
    #res_df[var+"_Levenshtein_Sim"]=res_levenshtein_list
    res_df[var+"_Levenshtein-Damerau_Sim"]=res_lev_damerau_list
    #contact_info_vars.extend([var+"_Levenshtein_Sim",var+"_Levenshtein-Damerau_Sim"])
    contact_info_vars.append(var+"_Levenshtein-Damerau_Sim")

#phone number similarity
new_phone_list=res_df["PhoneNumber_new"].replace("-","").apply(clean_info_to_str).to_list()
old_phone_list=res_df["PhoneNumber_old"].replace("-","").apply(clean_info_to_str).to_list()

#res_levenshtein_list=[relative_Levenshtein_similarity2(s1,s2) for s1,s2 in zip(new_phone_list,old_phone_list)]
res_lev_damerau_list=[relative_Levenshtein_Damerau_similarity2(s1, s2) for s1,s2 in zip(new_phone_list,old_phone_list)]

#res_df["PhoneNumber_Levenshtein_Sim"]=res_levenshtein_list
res_df["PhoneNumber_Levenshtein-Damerau_Sim"]=res_lev_damerau_list
#contact_info_vars.extend(["PhoneNumber_Levenshtein_Sim","PhoneNumber_Levenshtein-Damerau_Sim"])
contact_info_vars.append("PhoneNumber_Levenshtein-Damerau_Sim")

#location similarity
res_df["LocationID_new"]=res_df["CountryID"].apply(lambda x: str(int(x)).zfill(3))\
    +res_df["InsideStateID_new"].apply(lambda x: str(int(x)).zfill(4))+res_df["CityID_new"].apply(lambda x: str(int(x)).zfill(6))
res_df["LocationID_old"]=res_df["CountryID"].apply(lambda x: str(int(x)).zfill(3))\
    +res_df["InsideStateID_old"].apply(lambda x: str(int(x)).zfill(4))+res_df["CityID_old"].apply(lambda x: str(int(x)).zfill(6))

res_df["LocationID_match"]=(res_df["LocationID_new"]==res_df["LocationID_old"])
contact_info_vars.append("LocationID_match")

new_loc_id_list=res_df["LocationID_new"].to_list()
old_loc_id_list=res_df["LocationID_old"].to_list()

#res_levenshtein_list=[relative_Levenshtein_similarity2(s1,s2) for s1,s2 in zip(new_loc_id_list,old_loc_id_list)]
res_lev_damerau_list=[relative_Levenshtein_Damerau_similarity2(s1,s2) for s1,s2 in zip(new_loc_id_list,old_loc_id_list)]

#res_df["LocationID_Levenshtein_Sim"]=res_levenshtein_list
res_df["LocationID_Levenshtein-Damerau_Sim"]=res_lev_damerau_list
#contact_info_vars.extend(["LocationID_Levenshtein_Sim","LocationID_Levenshtein-Damerau_Sim"])
contact_info_vars.append("LocationID_Levenshtein-Damerau_Sim")

#email similarity
email_domain_replacement_dict={"desconocido":"**","yahoo.com":"-","ymail.com":"-","hotmail.com":"-","gmail.com":"-"}

new_email_list=res_df["Email_new"].apply(clean_info_to_str).apply(lambda x:x.lower()).replace(email_domain_replacement_dict,regex=True).to_list()
old_email_list=res_df["Email_old"].apply(clean_info_to_str).apply(lambda x:x.lower()).replace(email_domain_replacement_dict,regex=True).to_list()

#res_levenshtein_list=[relative_Levenshtein_similarity2(s1,s2) for s1,s2 in zip(new_email_list,old_email_list)]
res_lev_damerau_list=[relative_Levenshtein_Damerau_similarity2(s1, s2) for s1,s2 in zip(new_email_list,old_email_list)]

#res_df["Email_Levenshtein_Sim"]=res_levenshtein_list
res_df["Email_Levenshtein-Damerau_Sim"]=res_lev_damerau_list
#contact_info_vars.extend(["Email_Levenshtein_Sim","Email_Levenshtein-Damerau_Sim"])
contact_info_vars.append("Email_Levenshtein-Damerau_Sim")


#calculate aggregated location similarity score (boosted score)

from scipy import special


#location id (0.8-1) might work, 1 (location ID match) great
x=res_df["LocationID_Levenshtein-Damerau_Sim"].values
aux_s1=pd.Series(np.piecewise(x, [x < 0.8, (0.8<=x)&(x<0.9), (0.9<=x)&(x<0.99) , x>=0.99], [0,0.5,0.75,1]))

#address: jaccard score .60+ great, (.50-.60) so-so but could help, lev-dam 0.55+ works great, (0.4-0.55) might work
aux_s2=res_df["Address_Levenshtein-Damerau_Sim"].apply(lambda x: 0.5+0.5*special.erf(7.5*(x-0.475)) )

#phone number: lev-dam (0.6-0.8) might work
aux_s3=res_df["PhoneNumber_Levenshtein-Damerau_Sim"].apply(lambda x: 0.5+0.5*special.erf((7.5*(x-0.7))) )

#email similarity: lev-dam 0.9+ great, (0.5-0.9) might work
#other posible similarities: email domain (domain, client name, new-old), email name (contact name new-old)
aux_s4=res_df["Email_Levenshtein-Damerau_Sim"].apply(lambda x: 0.5+0.5*special.erf((5*(x-0.6))) )

#postal code: jaccard score 1 (great), (0.60-1) might not work, lev-dam score 1(great),(0.7-0.8] migth work(converto to int?) (no values between 1&0.8)
aux_s5=res_df["PostalCode_Levenshtein-Damerau_Sim"].apply(lambda x: 0.5+0.5*special.erf((12*(x-0.75))) )

res_df["boosted_score"]=(aux_s1+aux_s2+aux_s3+aux_s4+aux_s5)/5


##################################################################
#define aggregate final scores
##################################################################

#hyperplane params
w=np.array([-2.22682097,41.76643225,27.05350377])
#w=np.array([-2.32266081,-26.03009981,-15.79720877])
norm_w=np.sqrt(np.dot(w,w))
w=w/norm_w
b=-35/norm_w #-42
print("w=",w,"b=",b)

def my_hyperplane_function(x,w0=w,b0=b):
    #f=0 iif x is in the plane
    return np.dot(x,w0)+b0

def distance_to_hyperplane (x,w0=w,b0=b):
    distance=(np.dot(x,w0)+b0)/np.sqrt(np.dot(w0,w0))
    return distance

res_df["distance_to_hyperplane"]=res_df[["fuzzy_set_score","average_score","boosted_score"]].apply(distance_to_hyperplane,axis=1) #0.554151 max
res_df["distance_above_hyperplane"]=res_df["distance_to_hyperplane"].apply(lambda x: max(x,0))/max(0.554151,res_df["distance_to_hyperplane"].max())
res_df["fuzzy_component"]=res_df[["fuzzy_set_score","average_score"]].apply(lambda x: x[0] if (x[0]>=0.99 and x[1]>=0.55) else 0,axis=1)
res_df["average_component"]=res_df["average_score"].apply(lambda x: x if x>=0.97 else 0)

res_df["final_score1"]=res_df[["average_score","fuzzy_set_score","boosted_score"]].mean(axis=1)
res_df["final_score2"]=res_df[["distance_above_hyperplane","fuzzy_component","average_component"]].mean(axis=1)

decision_rule1=(res_df["average_score"]>=0.5)&((res_df[["fuzzy_set_score","average_score","boosted_score"]].apply(my_hyperplane_function,axis=1)>0)|\
    (res_df["average_score"]>=0.95)|(res_df["fuzzy_set_score"]>=0.95))
decision_rule2=(res_df["final_score2"]>0.0)

res_df["classification1"]=decision_rule1.apply(lambda x: "duplicated" if x==True else "not-duplicated")
res_df["classification2"]=decision_rule2.apply(lambda x: "duplicated" if x==True else "not-duplicated")

#past merge comparison
true_merges_df=pd.read_excel("../data/original data/new customers/All_New_Customers.xlsx",sheet_name="Merges")
true_merges_df["CustomerID_pair"]=true_merges_df["CustomerID"].apply(lambda x: str(x).zfill(5)+" ")\
    +true_merges_df["CustomerID2"].apply(lambda x: str(x).zfill(5))

res_df["actual_merge"]=res_df["CustomerID_pair"].isin(true_merges_df["CustomerID_pair"].to_list())


##################################################################
#report generation and formating
##################################################################

from datetime import datetime
now=datetime.now()
date = now.strftime("%d-%m-%Y") #%H-%M-%S

report_vars=['CustomerID_new', 'CustomerName_new', 'LocationID_new',
       'Address_new', 'Email_new',
       'PostalCode_new', 'PhoneNumber_new',
       'CleanCustomerName3_new', 'split_names',  
       'CustomerID_old', 'CustomerName_old',
       'CleanCustomerName3_old', 'LocationID_old',
       'Address_old', 'Email_old', 'PostalCode_old', 'PhoneNumber_old', 'actual_merge',
       'average_score','max_score','average_ordered_set_score','fuzzy_set_score' ,'boosted_score',
       "distance_above_hyperplane","fuzzy_component","average_component",'final_score1','final_score2','CustomerID_pair']


report_df=res_df[res_df["classification2"]=="duplicated"].copy().reset_index(drop=True)
report_df=report_df.sort_values(by="average_score",ascending=False).drop_duplicates(subset=["CustomerID_pair"],keep="first")#.groupby(by="CustomerID_pair").head(3)
report_df=report_df[report_vars[:-1]]
print(report_df.shape)

final_vars=["CustomerID_new","CustomerName_new","split_names","CustomerID_old","CustomerName_old","CleanCustomerName3_old", "fuzzy_set_score",
"boosted_score","average_score","distance_above_hyperplane","fuzzy_component","average_component","final_score1","final_score2","actual_merge"]

report_df=report_df[final_vars]
report_df.columns=["New Customer ID","New Customer Name","New Customer Clean Name","Old Customer ID","Old Customer Name","Old Customer Clean Name",
"Fuzzy Matching Score","Contact Info Sim","Average Name Sim","Distance Component","Fuzzy Component","Average Component",
"Old Final Score","Final Score","Previously Merged"]
report_df.sort_values(by=["Final Score","Average Name Sim"],ascending=False).to_excel("../data/results/daily duplicate report/duplicate_clients_"+date+".xlsx", index=False)
#report_df.sort_values(by="Final Score",ascending=False).to_excel("../data/results/daily duplicate report/all_duplicate_clients_"+date+".xlsx", index=False)