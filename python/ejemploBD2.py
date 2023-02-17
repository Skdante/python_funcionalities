import sqlite3

miConexion=sqlite3.connect("GestionProductos")
miCursor=miConexion.cursor()
"""
miCursor.execute('''
    CREATE TABLE PRODUCTOS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOMBRE_ARTICULO VARCHAR(50) UNIQUE,
    PRECIO INTEGER,
    SECCION VARCHAR(20))  
''')

productos=[
    ("pelota", 20, "jugeteria"),
    ("pantalón", 15, "confección"),
    ("destornillador", 25, "ferretería"),
    ("jarrón", 45, "cerámica")
]

miCursor.executemany("INSERT INTO PRODUCTOS VALUES(NULL, ?, ?, ?)", productos)
miConexion.commit()
"""
#miCursor.execute("SELECT * FROM PRODUCTOS WHERE SECCION = 'confección'")
#productos = miCursor.fetchall()
#print(productos)

#miCursor.execute("UPDATE PRODUCTOS SET PRECIO = 100 WHERE NOMBRE_ARTICULO = 'pelota'")
miCursor.execute("DELETE FROM PRODUCTOS WHERE ID = 1")
miConexion.commit()

miConexion.close()