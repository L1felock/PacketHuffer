from Tkinter import *
import tkMessageBox
import Tkinter

top = Tk()

m1 = PanedWindow()
m1.pack(fill=BOTH, expand=1)


Lb1 = Listbox(top)
Lb1.insert(1, "Python")
Lb1.insert(2, "Perl")
Lb1.insert(3, "C")
Lb1.insert(4, "PHP")
Lb1.insert(5, "JSP")
Lb1.insert(6, "Ruby")

#Lb1.pack()

m2 = PanedWindow(m1, orient=VERTICAL)
m1.add(m2)

top = Label(m2, text="top pane")
m2.add(top)
m2.add(Lb1)

bottom = Label(m2, text="bottom pane")
m2.add(bottom)
info = Label(m2, text=Lb1.curselection())
m2.add(info)


top.mainloop()