from tkinter import *
from ttkbootstrap.constants import *
from ttkbootstrap import *

# root = Window(themename = "cyborg")
root = Tk(screenName = None, baseName = None, className = "Tk", useTk = 1)
root.title("Tkinter experiment")
root.geometry("500x350")

lbl = Label(text = "Hello world!", font = ("Helvetica", 28), bootstyle = "danger, inverse")
lbl.pack(pady = 50)

btn = Button(text = "Click Me!", bootstyle = "success, outline")
btn.pack(pady = 20)

mainloop()