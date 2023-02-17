from tkinter import *
root = Tk()

miFrame = Frame(root, width=500, height=400)
miFrame.pack()

miImage = PhotoImage(file="maxresdefault.jpg")
Label(miFrame, image=miImage).place(x=100, y=200)
#Label(miFrame, text = "Hola chicos", fg="red", font=("Comic Sans MS",18)).place(x=100, y=200)

root.mainloop() 