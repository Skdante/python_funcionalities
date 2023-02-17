from tkinter import *
root= Tk()
root.title("Ejemplo")

playa=IntVar()
montana=IntVar()
turismoRral=IntVar()

def OpcionViaje():
    opcionEscogida=""

    if playa.get() == 1:
        opcionEscogida += " playa"
    if montana.get() == 1:
        opcionEscogida += " Montaña"
    if turismoRral.get() == 1:
        opcionEscogida += " Turismo Rural"

    textoFinal.config(text=opcionEscogida)

Label(root, text="Eligue destinos:").pack()

Checkbutton(root, text="Playa", variable=playa, onvalue=1, offvalue=0, command=OpcionViaje).pack()
Checkbutton(root, text="Ciudad", variable=montana, onvalue=1, offvalue=0, command=OpcionViaje).pack()
Checkbutton(root, text="Montañas", variable=turismoRral, onvalue=1, offvalue=0, command=OpcionViaje).pack()

textoFinal=Label(root)
textoFinal.pack()

root.mainloop()