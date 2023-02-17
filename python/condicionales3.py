print("Asignaturas optativas año 2020")
print("Asignaturas optativas: Informatica gráfica - Pruebas de software - Usabilidad y accesibilidad")
asignatura = input("Escriba la asignatura escogida: ").lower()

print("Minusculas", asignatura.lower())
print("Mayusculas", asignatura.upper())
print("Mayuscula inicial", asignatura.capitalize())
print("Mayusculas en las iniciales", asignatura.title())

if asignatura in ("informatica gráfica", "pruebas de software", "usabilidad y accesibilidad"):
    print("Asignatura elegida ", asignatura.title())
else: 
    print("La asignatura escogida no esta contemplada")

