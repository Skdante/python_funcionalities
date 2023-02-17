import re

cadena="Vamos a aprender expresiones regulares en Payhton. Payhton es un lenguaje se sintaxis sencilla"
textoBuscar="Payhton"

'''
if re.search(textoBuscar, cadena) is not None:
    print("He encontrado el texto")
else:
    print("No eh encontrado el texto")
'''

textoEncontrado=re.search(textoBuscar, cadena)
print(textoEncontrado.start())
print(textoEncontrado.end())
print(textoEncontrado.span())
print(len(re.findall(textoBuscar, cadena)))