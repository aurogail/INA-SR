from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import tkinter as tk
from PIL import Image, ImageTk

# Function for openeing the file explorer
def browseFiles ():
    filename = filedialog.askopenfilenames(initialdir = "/",
                                          title = "Selectionner un Fichier",
                                          filetypes = (("Image files", ".jpg"),
                                                       ("Image files",".png")))
    img = Image.open(filename)
    photo = ImageTk.PhotoImage(img)
    lbl= Label(imge=photo)
    lbl.image= photo

# create window
window = Tk()

# name window
window.title("SR GUI")

#size window
window.geometry("500x500")
window.minsize(300,300)
window.config(background='white')

#button
open_button = Button(window, text='Ouvrir un fichier', command = browseFiles)
open_button.pack()

#execute window
window.mainloop()
