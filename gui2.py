from tkinter import*
import numpy as np

import FileType
from stylesheet import VideoPlayer
from PIL import Image, ImageTk
import cv2
import os


def extract_vid(matrix_image: np.array):

    # apply algo small image
    print("Extracting video")

    # convert matrix image to pillow image object
    frame_pillow = Image.fromarray(matrix_image)
    frame_pillow.thumbnail([300, 300])
    # show plat
    photo = ImageTk.PhotoImage(image=frame_pillow)
    # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    board.config(image=photo)
    board.image = photo
    # refresh image display
    board.update()


def extract_image(matrix_image: np.array):

    # apply algo small image
    print("Extracting image")
    # convert matrix image to pillow image object
    frame_pillow = Image.fromarray(matrix_image)
    frame_pillow.thumbnail([300, 300])
    # show plat
    photo = ImageTk.PhotoImage(image=frame_pillow)
    # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    board.config(image=photo)
    board.image = photo
    # refresh image display
    board.update()


root = Tk()
root.geometry("840x600")
root.minsize(640, 480)
root.maxsize(1920, 1080)
root.title("SR GUI")

# main panel
MainPanel = Frame(root, width=500, height=2000, bg="white", relief=SUNKEN)
MainPanel.pack(side=TOP)
MainPanel.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

# control panel
control_frame_top = Canvas(MainPanel, width=350, height=5, bg="white", relief=SUNKEN)
control_frame_top.pack(fill=BOTH, expand=False)

board = Label(control_frame_top, width=80, height=-1, bg="white")
board.pack(fill=BOTH, expand=True)

# control panel
control_frame_main = Canvas(MainPanel, width=300, height=700, bg="blue", relief=SUNKEN)
control_frame_main.pack(fill=BOTH, expand=True)

# video player
vid = VideoPlayer(control_frame_main, image=True, play=True, algo=True)

#vid.command = lambda frame: extract_image(frame)

root.mainloop()
