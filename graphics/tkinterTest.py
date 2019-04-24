# -*- coding: utf-8 -*-
from tkinter import *
window = Tk()

# "Hello world":
label = Label(window, text="Hello world", bg="blue")
label.pack()

# Exit_button:
exit = Button(window, text="Quit", command=window.quit)
exit.pack()

# Entries:
value = StringVar()
value.set("String variable's test")
text = Entry(window, textvariable=value, width=30)
text.pack()

# Checkbutton:
new = Checkbutton(window, text="New?")
new.pack()

# List:
list = Listbox(window)
list.insert(1, "Python")
list.insert(2, "PHP")
list.insert(3, "java")
list.insert(4, "CSS")
list.insert(5, "Javascript")
list.pack()

# Canvas:
canvas = Canvas(window, width=150, height=120,  background='blue')
ligneOne = canvas.create_line(75, 0, 75, 120)
ligneTwo = canvas.create_line(0, 60, 150, 60)
txt = canvas.create_text(75, 60, text="TARGET", font="Arial 16 italic", fill="white")
canvas.pack()

card = PhotoImage(file="pictures\Logo.png")
plusQuatres =Canvas(window, width=700, height=700)
plusQuatres.create_image(0, 0, anchor=NW, image=card)
canvas.coords(card, 100, 50, 10, 100)
plusQuatres.pack()

# Scale:
step = DoubleVar()
scale = Scale(window, variable=step, )
scale.pack()

# Frame:
frameOne = Frame(window, borderwidth=2, relief=GROOVE)
frameOne.pack(side=LEFT, padx=10, pady=10)

frameTwo = Frame(window, borderwidth=2, relief=GROOVE)
frameTwo.pack(side=LEFT, padx=5, pady=5)

window.mainloop()