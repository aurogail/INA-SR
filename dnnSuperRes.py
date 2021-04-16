import cv2 as cv
import FileType
import shutil

#Classe regroupant les fonctions applicables à une image cv2 -> instances de "presque" type cv2
class UpscaleImage:
    #attributs des Objets UpscaleImage
    name: str
    resolution: str
    output_res: str
    model_path: str
    model_name: str
    model_scale: int
    output_name: str
    type_of_image: str
    fps: int

    #initialisation des attributs (publiques)
    def __init__(self, name, resolution, output_res, model_path,  model_name, model_scale, output_name, type_of_image, fps):
        self.name = name
        self.resolution = resolution
        self.output_res = output_res
        self.model_path = model_path
        self.model_name = model_name
        self.model_scale = model_scale
        self.output_name = output_name
        self.type_of_image = type_of_image
        self.fps = fps

        # """ Methodes """
    # Renvoi une image cv2 à partir du nom du fichier (lecture du fichier)
    def read_image(self, path):
        self.name = path
        return cv.imread(self.name)

    # Renvoi le type de fichier (image ou vidéo en fonction de l'extension)
    def get_file_type(self):
        return FileType.file_type(self.name)

    # Renvoi une frame cv2
    def capture_video(self, path):
        self.name = path
        return cv.VideoCapture(self.name)

    # Renvoi l'image upscaled si le type de fichier == image
    def upscale_image(self, input_path):
        global sr
        sr = cv.dnn_superres.DnnSuperResImpl_create()
        if self.type_of_image == 'image':
            image = self.read_image(input_path)
            sr.readModel(self.model_path)
            sr.setModel(self.model_name, self.model_scale)
            print('Shape of Original Image: {}'.format(image.shape))
            return sr.upsample(image)

    # Renvoi une frame upscaled si le type de fichier == video
    def upscale_video_frame(self, image):
        global sr
        sr = cv.dnn_superres.DnnSuperResImpl_create()
        if self.type_of_image == 'video':
            """dim = rsiv.get_dims(self.capture_video(), res=self.resolution)
            video_type_cv2 = rsiv.get_video_type(self.name)
            out = cv.VideoWriter(self.output_name, video_type_cv2, self.fps, dim)"""

            #start = time.time()
            #image = cap.read()
            # si fin video

            sr.readModel(self.model_path)
            sr.setModel(self.model_name, self.model_scale)
            return sr.upsample(image)

    # Sauvegarde l'image upscaled et la renvoi
    def save_upscaled_image(self, in_path, out_path):
        upscaled = self.upscale_image(in_path)
        print("Saving Upscale -> in_path : "+in_path)
        print("upscaled :" + str(upscaled))
        print("out_path : "+out_path)
        cv.imwrite(out_path, upscaled)
        #copy_to_folder_media(out_path, "./results/")
        print('Shape of Super Resolution Image: {}'.format(upscaled.shape))
        return upscaled

    # Sauvegarde la vidéo upscale (pas encore utilisée)
    def save_upscaled_video(self, cap: cv.VideoCapture, ret, out_path):
        outpath = out_path + self.output_name
        dim = FileType.get_dims(cap, res=self.resolution)
        video_type_cv2 = FileType.get_video_type(self.name)
        out = cv.VideoWriter(outpath, video_type_cv2, self.fps, dim)
        while cap.isOpened():
            if not ret:
                break
            out.write(self.upscale_video_frame(cap))
        self.capture_video(self.name).release()
        out.release()
        cv.destroyAllWindows()


# Fonction qui copie un fichier vers une destination
def copy_to_folder_media(filename, destination):
    shutil.move(filename, destination)

