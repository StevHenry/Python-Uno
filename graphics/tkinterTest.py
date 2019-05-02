# -*- coding: utf-8 -*-
from tkinter import *
uno_frame = Tk()

# "Hello world":
label = Label(uno_frame, text="Hello world", bg="blue")
label.pack()

# Exit_button:
exit = Button(uno_frame, text="Quit", command=uno_frame.quit)
exit.pack()

# Entries:
value = StringVar()
value.set("String variable's test")
text = Entry(uno_frame, textvariable=value, width=30)
text.pack()

# Checkbutton:
new = Checkbutton(uno_frame, text="New?")
new.pack()

# List:
list = Listbox(uno_frame)
list.insert(1, "Python")
list.insert(2, "PHP")
list.insert(3, "java")
list.insert(4, "CSS")
list.insert(5, "Javascript")
list.pack()

# Canvas:
canvas = Canvas(uno_frame, width=150, height=120, background='blue')
ligneOne = canvas.create_line(75, 0, 75, 120)
ligneTwo = canvas.create_line(0, 60, 150, 60)
txt = canvas.create_text(75, 60, text="TARGET", font="Arial 16 italic", fill="white")
canvas.pack()

card = PhotoImage(file="pictures\Logo.png")
plusQuatres =Canvas(uno_frame, width=700, height=700)
plusQuatres.create_image(0, 0, anchor=NW, image=card)
canvas.coords(card, 100, 50, 10, 100)
plusQuatres.pack()

# Scale:
step = DoubleVar()
scale = Scale(uno_frame, variable=step, )
scale.pack()

# Frame:
frameOne = Frame(uno_frame, borderwidth=2, relief=GROOVE)
frameOne.pack(side=LEFT, padx=10, pady=10)

frameTwo = Frame(uno_frame, borderwidth=2, relief=GROOVE)
frameTwo.pack(side=LEFT, padx=5, pady=5)

uno_frame.mainloop()