from tkinter import*
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
import os
import copy

import FileType

class VideoPlayer(ttk.Frame):

    def __init__(self, parent: ttk.Frame=None, **prop: dict):

        setup = self.set_setup(prop)

        ttk.Frame.__init__(self, parent)

        # private
        self.__cap = object
        self.__size = (640, 480)
        self.__image_ratio = 480/640
        self.__frames_numbers = 0
        self.__play = False
        self.__algo = False
        self.__frame = np.array
        self.__initialdir = "/"
        self.__initialdir_movie = "/"
        self.filename = ""

        # protected
        self._command = []

        # public
        self.frame = np.array
        # build widget
        self._build_widget(parent, setup)

    @property
    def frame(self)->np.array:
        return self.__frame

    @property
    def command(self):
        return self.__command

    @property
    def algo(self)->bool:
        return self.__algo

    @frame.setter
    def frame(self, frame: np.array):
        self.__frame = frame

        if self.algo and callable(self._command):
            # convert image to numpy image
            matrix_image = np.array(self.frame)
            self._command(matrix_image)

    @command.setter
    def command(self, command):
        # check if the command is lambda expression
        if callable(command):

            self._command = command

    @algo.setter
    def algo(self, algo: bool):
        if isinstance(algo, bool):
            self.__algo = algo

    def set_setup(self, prop: dict)->dict:

        default = {'video':  True, 'pause': True, 'stop': True, 'image': False, 'algo': False}
        setup = default.copy()
        setup.update(prop)
        self.algo = setup['algo']
        return setup

    def _build_widget(self, parent: ttk.Frame=None, setup: dict=dict):

        if parent is None:
            self.master.geometry("1050x7500")
            self.master.minsize(1050,750)
            self.master.maxsize(1920,1080)
            self.main_panel = Frame(self.master, relief=SUNKEN)
            self.main_panel.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
            self.master.title("Super Résolution GUI")

        else:
            self.main_panel = parent

        # main panel
        self.main_panel.config(bg="white")

        icon_width = 45
        icon_height = 50
        canvas_progressbar_height = 2
        #frame_height = int(self.main_panel.cget('height')/10-icon_height-canvas_progressbar_height)

        self.canvas_image = Canvas(self.main_panel, bg="white", relief=RIDGE)

        self.frame_image_original= LabelFrame(self.canvas_image, bg="white", relief=RIDGE,text='Image Original',
                                              font=('century gothic', 16), pady=10, width=100)
        self.frame_image_original.grid(row=0, column=0, sticky="nsew")
        self.frame_image_original.bind("<Configure>", self.resize)

        self.frame_image_SR = LabelFrame(self.canvas_image, bg="white", relief=RIDGE, text='Image SR',
                                         font=('century gothic', 16), pady=10, width=100)
        self.frame_image_SR.grid(row=0, column=1, sticky="nsew")
        self.frame_image_SR.bind("<Configure>", self.resize)

        self.canvas_image.grid_columnconfigure(0, weight=1)
        self.canvas_image.grid_columnconfigure(1, weight=1)
        self.canvas_image.grid_rowconfigure(0, weight=1)

        self.canvas_image.pack(fill=BOTH, expand=True, side=TOP)
        self.canvas_image.bind("<Configure>", self.resize)

        self.board = Label(self.frame_image_original, bg="white")
        self.board.pack( fill=BOTH , expand=True)

        canvas_progressbar = Canvas(self.main_panel, relief=FLAT, height=canvas_progressbar_height,
                                    bg="white", highlightthickness=0)
        canvas_progressbar.pack(fill=BOTH, padx=10, pady=10)

        s = ttk.Style()
        s.theme_use('aqua')
        self.progressbar = ttk.Progressbar(canvas_progressbar, orient='horizontal', length=200, mode="determinate")

        # control panel
        control_frame = Frame(self.main_panel, bg="white")
        control_frame.pack(side=TOP,padx=20, fill=X, pady= 10)

        control_frame_algo= Frame(self.main_panel, bg="white")
        control_frame_pe = LabelFrame(control_frame_algo, bg="white", relief=FLAT, text='Résolution',
                                      font=('century gothic', 16), pady=10)
        control_frame_pe.grid(row=0, column=0, padx=20)

        control_frame_modele = LabelFrame(control_frame_algo, bg="white", relief=FLAT, text='Choix du Modèle',
                                          font=('century gothic', 16), pady=10)
        control_frame_modele.grid(row=0, column=1, padx= 50)
        control_frame_algo.pack(side=BOTTOM, fill=X)

        icons_path = os.path.abspath(os.path.join(os.pardir, 'Icons'))
        if setup['video']:
            # play video button button_live_video
            self.icon_video = PhotoImage(file=os.path.join(icons_path, 'video.png'))
            button_live_video = Button(control_frame, padx=2, pady=2, bd=4, fg="white", font=('arial', 12),
                                       text="> Load Video", bg='white', image=self.icon_video, height=icon_height,
                                       width=icon_width, command=lambda: self.load_movie())
            button_live_video.pack(side='left')

        if setup['image']:
            # load image button button_load_image
            self.icon_image = PhotoImage(file=os.path.join(icons_path, 'image.png'))
            button_load_image = Button(control_frame, padx=2, pady=2, bd=4, fg="white", font=('arial', 12),
                                       text="Load Image", bg="black", image=self.icon_image,
                                       height=icon_height, width=icon_width,
                                       command=lambda: self.load_image())
            button_load_image.pack(side='left', padx=10)

        if setup['pause']:
            # pause video button button_live_video
            self.icon_pause = PhotoImage(file=os.path.join(icons_path, 'pause2.png'))
            self.icon_play = PhotoImage(file=os.path.join(icons_path, 'play2.png'))
            self.button_pause_video = Button(control_frame, padx=2, pady=2, bd=4, fg="white",
                                             font=('arial', 12, 'bold'),
                                             text="Pause", bg='white', image=self.icon_pause,
                                             height=icon_height, width=icon_width,
                                             command=lambda: self.pause_movie())
            self.button_pause_video.pack(side='left')

        if setup['stop']:
            # stop video button button_live_video
            self.icon_stop = PhotoImage(file=os.path.join(icons_path, 'stop.png'))
            button_stop_video = Button(control_frame, padx=2, pady=2, bd=4, fg="white", font=('arial', 12, 'bold'),
                                       text="stop", bg='white', height=icon_height, width=icon_width,
                                       image=self.icon_stop,
                                       command=lambda: self.stop_movie())
            button_stop_video.pack(side='left',padx=10)


        if setup['algo']:
            # load image button button_load_image
            # self.icon_algo = PhotoImage( file=os.path.join( icons_path, 'algo.PNG' ) )

            self.icon_x2 = PhotoImage( file=os.path.join( icons_path, 'x2.png' ) )
            self.button_x2 = Button(control_frame_pe, padx=2, pady=2, bd=4, fg="white", font=('arial',12,'bold'),
                                    text="x2", bg="white", height=icon_height, width=icon_width,
                                    image=self.icon_x2,
                                    command=lambda: self.extract())
            self.button_x2.pack(side='left')

            self.icon_x3 = PhotoImage( file=os.path.join( icons_path, 'x3.png' ) )
            self.button_x3 = Button(control_frame_pe, padx=2, pady=2, bd=4, fg="white", font=('arial',12,'bold'),
                                    text="x3", bg="white", height=icon_height, width=icon_width,
                                    image=self.icon_x3,
                                    command=lambda: self.extract())
            self.button_x3.pack(side='left',padx=10)

            self.icon_x4 = PhotoImage( file=os.path.join( icons_path, 'x4.png' ) )
            self.button_x4 = Button(control_frame_pe, padx=2, pady=2, bd=4, fg="white", font=('arial',12,'bold'),
                                    text="x4", bg="black", height=icon_height, width=icon_width,
                                    image=self.icon_x4,
                                    command=lambda: self.extract())
            self.button_x4.pack(side='left')

            self.icon_x8 = PhotoImage( file=os.path.join( icons_path, 'x8.png' ) )
            self.button_x8 = Button(control_frame_pe, padx=2, pady=2, bd=4, fg="white", font=('arial', 12, 'bold'),
                                    text="x8", bg="black", height=icon_height, width=icon_width,
                                    image=self.icon_x8,
                                    command=lambda: self.extract())
            self.button_x8.pack(side='left', padx=10)

            self.icon_uhd = PhotoImage( file=os.path.join( icons_path, 'uhd.png' ) )
            self.button_uhd = Button(control_frame_pe, padx=2, pady=2, bd=4, fg="white", font=('arial', 12, 'bold'),
                                     text="UHD", bg="black", height=icon_height, width=icon_width,
                                     image=self.icon_uhd,
                                     command=lambda: self.extract())
            self.button_uhd.pack(side='left')

            self.icon_hd = PhotoImage( file=os.path.join( icons_path, 'hd.png' ) )
            self.button_hd = Button(control_frame_pe, padx=2, pady=2, bd=4, fg="white", font=('arial', 12, 'bold'),
                                    text="HD", bg="black", height=icon_height, width=icon_width,
                                    image=self.icon_hd,
                                    command=lambda: self.extract())
            self.button_hd.pack(side='left',padx=10)

            self.icon_best = PhotoImage( file=os.path.join( icons_path, 'best.png' ) )
            self.button_best = Button(control_frame_modele, padx=2, pady=2, bd=4, fg="white", font=('arial', 12, 'bold'),
                                      text="Best", bg="black", height=icon_height, width=icon_width,
                                      image=self.icon_best,
                                      command=lambda: self.extract())
            self.button_best.pack(side='left')

            self.icon_fast = PhotoImage( file=os.path.join( icons_path, 'fast.png' ) )
            self.button_fast = Button(control_frame_modele, padx=2, pady=2, bd=4, fg="white", font=('arial', 12, 'bold'),
                                      text="Fast", bg="black", height=icon_height, width=icon_width,
                                      image=self.icon_fast,
                                      command=lambda: self.extract())
            self.button_fast.pack(side='left',padx=10)

            self.icon_apply = PhotoImage( file=os.path.join( icons_path, 'apply.png' ) )
            self.button_apply = Button(control_frame_modele, padx=2, pady=2, bd=4, fg="white", font=('arial', 12, 'bold'),
                                       text="Apply", bg="black", height=icon_height, width=icon_width,
                                       image=self.icon_apply,
                                       command=lambda: self.extract())
            self.button_apply.pack(side='left',padx=50)

        # edit box
        self.frame_counter = Label(control_frame, height=2, width=15, padx=10, pady=10, bd=4,
                                   bg='white', fg="grey", font=('arial', 10, 'bold'))
        self.frame_counter.pack(side=RIGHT)

    def extract(self):

        if FileType.file_type(self.filename) == "image":
            board2 = Label(self.frame_image_SR,height=-1, bg="white")
            board2.pack(side=RIGHT, expand=True)
            print("File type, ext = ", FileType.file_type_ext(self.filename))
            self.__initialdir = os.path.dirname(os.path.abspath(self.filename))
            if len(self.filename) != 0:
                self.frame = Image.open(self.filename)
                image = self.frame
                self.update_progress(1, 1)
                self.__image_ratio = image.height / image.width
                self.show_image(image, board2)
            self.__cap.release()
            cv2.destroyAllWindows()

        elif FileType.file_type(self.filename) == "video":
            board2 = Label(self.canvas_image, width=80, height=-1, bg="white")
            board2.pack(side=RIGHT, fill=BOTH, expand=True)
            print("File type, ext = ", FileType.file_type_ext(self.filename))
            if len(self.filename) != 0:
                self.__initialdir_movie = os.path.dirname(os.path.abspath(self.filename))
                #self.run_frames(board2)

        else:
            print("No file type, ext = ", FileType.file_type_ext(self.filename))

    def resize(self, event):

        w, h = event.width, event.height

        width = h/self.__image_ratio
        height = h

        if width > w:

            width = w
            height = w*self.__image_ratio

        self.__size = (int(width), int(height))
        if Image.isImageType(self.frame):
            image = copy.deepcopy(self.frame)
            self.show_image(image, self.board, self.board2)

    def open_image_file(self):
        return filedialog.askopenfilename(initialdir=self.__initialdir, title="Ouvrir un fichier",
                                          filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

    def open_video_file(self):
        return filedialog.askopenfilename(initialdir=self.__initialdir_movie,
                                          title="Ouvrir un fichier",
                                          filetypes=(("AVI files", "*.AVI"),
                                                     ("MP4 files", "*.MP4"),
                                                     ("all files", "*.*")))

    def load_image(self):

        filename = self.open_image_file()
        self.__initialdir = os.path.dirname(os.path.abspath(filename))
        if len(filename) != 0:
            self.frame = Image.open(filename)
            image = self.frame

            self.update_progress(1, 1)
            self.__image_ratio = image.height / image.width
            self.filename = filename
            self.show_image(image, self.board)

        return filename

    def show_image(self, image, board):

        # resize image
        image.thumbnail(self.__size)
        #
        self.photo = ImageTk.PhotoImage(image=image)
        # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        board.config(image=self.photo)
        board.image = self.photo
        # refresh image display
        board.update()

    def load_movie(self):

        self.board.destroy()
        self.board = Label(self.frame_image_original, bg="white", width=44, height=14)
        self.board.pack( fill=BOTH , expand=True)
        movie_filename = self.open_video_file()
        if len(movie_filename) != 0:
            self.__initialdir_movie = os.path.dirname(os.path.abspath(movie_filename))
            self.filename = movie_filename
            self.__cap = cv2.VideoCapture(movie_filename)
            self.play_movie(self.__cap, self.board)
        #pass
        return movie_filename

    def play_movie(self, cap, board):

        #self.__cap = cv2.VideoCapture(movie_filename)
        self.__frames_numbers = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.__image_ratio = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / cap.get(cv2.CAP_PROP_FRAME_WIDTH)

        self.progressbar.pack(fill=X, padx=10, pady=10, expand=True)
        self.progressbar["maximum"] = self.__frames_numbers
        self.__play = True

        self.run_frames(cap, board)

    def run_frames(self, cap, board):

        frame_pass = 0

        while cap.isOpened():

            if self.__play:
                # update the frame number
                ret, image_matrix = cap.read()
                # self.frame = image_matrix
                if ret:
                    frame_pass += 1
                    self.update_progress(frame_pass)

                    # convert matrix image to pillow image object
                    self.frame = self.matrix_to_pillow(image_matrix)
                    self.show_image(self.frame, board)

                # refresh image display
            board.update()
            board2.update()

        cap.release()

        cv2.destroyAllWindows()

    @staticmethod
    def matrix_to_pillow(frame: np.array):

        # convert to BGR
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # convert matrix image to pillow image object
        frame_pillow = Image.fromarray(frame_bgr)
        return frame_pillow

    def stop_movie(self):

        self.pause_movie()
        self.__cap.release()

        cv2.destroyAllWindows()
        self.update_progress(0, 0)
        self.board.destroy()
        self.board2.destroy()

    def pause_movie(self):

        if self.__cap.isOpened():
            self.__play = not self.__play

        else:
            self.__play = False

        if self.__play:
            self.button_pause_video.config(image=self.icon_pause)
        elif not self.__play:
            self.button_pause_video.config(image=self.icon_play)

    def update_progress(self, frame_pass: int=0, frames_numbers: int = None):

        if frames_numbers is None:
            frames_numbers = self.__frames_numbers

        self.frame_counter.configure(text=str(frame_pass) + " / " + str(frames_numbers))
        # update the progressbar
        self.progressbar["value"] = frame_pass
        self.progressbar.update()


def ChangeState(Objet_button:Button):
    if (Objet_button['state'] == NORMAL):
        Objet_button['state'] = DISABLED
    else:
        Objet_button['state'] = NORMAL

def main():
    vid = VideoPlayer(image=True, play=True, algo=True)
    #vid.command = lambda frame: extract_image(frame)
    vid.mainloop()

#def extract_image(matrix_image: np.array):
# apply algo
#resize_image = cv2.resize(matrix_image, dsize=(640, 480), interpolation=cv2.INTER_CUBIC)
#cv2.imshow('frame', resize_image)

if __name__ == "__main__":
    main()