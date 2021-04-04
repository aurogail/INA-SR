from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import tkinter as tk
from PIL import Image, ImageTk

# create window
window = Tk()

# name window
window.title("SR GUI")

#size window
window.geometry("840x600")
window.minsize(640,400)
window.maxsize(840,600)
window.resizable(width = True, height = True)
window.configure(background='white')

# Function for openeing the file explorer
def openFilename():
    filename = filedialog.askopenfilename(title = "Selectionner un Fichier",
                                           filetypes = (("JPEG File","*.jpg"),
                                                        ("PNG File","*.png"),
                                                        ("all files","*.*")))
    return filename

def open_img():
    x = openFilename()
    original_img = ImageTk.PhotoImage(Image.open(x))
    panel = Label(window, image = original_img)
    panel.image=original_img
    panel.grid(row = 4)

#button
open_button = Button(window, text='Ouvrir un fichier', command = open_img).grid(row = 1, columnspan = 4)
exit_button = Button(window, text="exit", command = lambda : exit()).grid(row = 2, columnspan = 4)

#execute window
window.mainloop()