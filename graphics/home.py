# -*- coding: utf-8 -*-

from tkinter import *

home = Tk()

# Home_configurations:
home.title("UNO-Isn")
home.configure(bg='#ed2600')

# Logo:
uno = PhotoImage(file='../resources/pictures/Logo (2).png')
canvasLogo = Canvas(home, width=515, height=330, highlightthickness=0)
canvasLogo.create_image(0, 0, anchor=NW, image=uno)
canvasLogo.grid(row=0, column=7)

# Buttons:
play = Button(home, text="PLAY", activebackground='#febe2e', activeforeground='#ed2600', bg='#febe2e', fg='#ed2600',
              relief='flat', takefocus=1, font='arial', padx=30, pady=5)
play.grid(row=2, column=7)

helpButton = Button(home, text="HELP", activebackground='#febe2e', activeforeground='#ed2600', bg='#febe2e',
                    fg='#ed2600', relief='flat', takefocus=1, font='arial', padx=30, pady=5)
helpButton.grid(row=4, column=7)

# Dev cards:
dev = PhotoImage(file='../resources/pictures/Dev.png')
canvas = Canvas(home, width=300, height=163, highlightthickness=0)
canvas.create_image(0, 0, anchor=NW, image=dev)
canvas.grid(row=17, column=16)

# "Made by ...":
madeBy = Label(text="Made by \"Med-Studios\"", font='arial', bg='#ed2600', fg='#ffffff')
madeBy.grid(row=10, column=16)

print(home.grid_size())
Button(home, text='L17-C18', borderwidth=1).grid(row=17, column=18)
Button(home, text='L0-C0', borderwidth=1).grid(row=0, column=0)
Button(home, text='L0-C7', borderwidth=1).grid(row=0, column=7)
Button(home, text='L0-C6', borderwidth=1).grid(row=0, column=6)


home.mainloop()