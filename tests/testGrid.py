# -*- coding: utf-8 -*-

from tkinter import *

testGrid = Tk()

# Home_configurations:
testGrid.title("UNO-Isn (testGrid)")
testGrid.configure(bg='#ed2600')

# Grid:
for l in range(33):
    for c in range(31):
        Button(testGrid, text='L%s-C%s' % (l, c), borderwidth=1).grid(row=l, column=c)

# Logo:
uno = PhotoImage(file='../resources/pictures/Logo (2).png')
canvas = Canvas(testGrid, width=515, height=330, highlightthickness=0)
canvas.create_image(0, 0, anchor=NW, image=uno)
canvas.grid(row=0, column=11)

# Buttons:
play = Button(testGrid, text="PLAY", activebackground='#febe2e', activeforeground='#ed2600', bg='#febe2e', fg='#ed2600',
              relief='flat', takefocus=1, font='arial', padx=30, pady=5)
play.grid(row=2, column=11)


rulesButton = Button(testGrid, text="RULES", activebackground='#febe2e', activeforeground='#ed2600', bg='#febe2e',
                    fg='#ed2600', relief='flat', takefocus=1, font='arial', padx=30, pady=5)
rulesButton.grid(row=4, column=11)

# Dev cards:
dev = PhotoImage(file='../resources/pictures/Dev.png')
canvas = Canvas(testGrid, width=300, height=163, highlightthickness=0)
canvas.create_image(0, 0, anchor=NW, image=dev)
canvas.grid(row=12, column=16)

# "Made by ...":
madeBy = Label(text="Made by \"Med-Studios\"", font='arial', bg='#ed2600', fg='#ffffff')
madeBy.grid(row=11, column=16)

print(testGrid.grid_size())

testGrid.mainloop()