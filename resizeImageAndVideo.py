import os
import cv2

    # Dictionnaires #

# Resolution : (Width, Height)
STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160)
}

# Extension de vidéo : codec
VIDEO_TYPE = {
    '.avi': cv2.VideoWriter_fourcc(*'avc1'),
    '.mkv': cv2.VideoWriter_fourcc(*'avc1'),
    '.mp4': cv2.VideoWriter_fourcc(*'mp4v')
}

# Extension de fichier : Type de fichier
FILE_TYPE = {
    '.avi': 'video',
    '.mkv': 'video',
    '.mp4': 'video',
    '.jpg': 'image',
    '.png': 'image'
}

    # Fonctions appelée par les boutons #

# Renvoi le type de fichier en fonction de son extension
def file_type(file_name):
    name, ext = os.path.splitext(file_name)
    if ext in FILE_TYPE:
        return FILE_TYPE[ext]
    else:
        return ''

# Renvoi le codec choisi en fonction de l'extension
def get_video_type(fileName):
    filename, ext = os.path.splitext(fileName)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

# Renvoi la résolution (Width, Height) selon le type de fichier
def get_dims(image_name, res="1080p"):
    if file_type(image_name) == "image":
        return image_get_dims(res)
    elif file_type(image_name) == "video":
        return video_get_dims(res)

# Renvoi la résolution (Width, Height) pour une vidéo
def video_get_dims(res="1080p"):
    global width, height
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        return STD_DIMENSIONS[res]
        #change_resolution(capture, width, height)
    return width, height

# Renvoi la résolution (Height, Width) pour une image cv2
def image_get_dims(res="1080p"):
    global width, height
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width = STD_DIMENSIONS[res][0]
        height = STD_DIMENSIONS[res][1]
        #change_resolution(capture, width, height)
    return height, width

# Renvoi une image cv2 resized si la taille de l'upscaled est supérieur à celle de l'original
def donwsize(original_image, upscaled_image, scale):
    global width, height
    if original_image.shape[1] < upscaled_image.shape[1]:
        width = original_image.shape[1]
        height = original_image.shape[0]
        #dsize = (height, width)
        dsize = (width, height)
        return cv2.resize(upscaled_image, dsize, fx=-scale, fy=-scale, interpolation=cv2.INTER_AREA)
    else:
        print("Failed to downsize : original width > than upsclaled image")


def donwsize_video(cap, upscaled_image, scale):
    global width, height
    width = int(cap.get(3))
    height = int(cap.get(4))
    #dsize = (height, width)
    dsize = (width, height)
    return cv2.resize(upscaled_image, dsize, fx=-scale, fy=-scale, interpolation=cv2.INTER_AREA)


# Resize en fonction des resolutions (du dictionnaire STD_DIMENSIONS) #

def resize_image(image, new_size, scale_percent=100):
    global width, height
    if new_size in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[new_size]
    elif 0 < scale_percent:
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
    dsize = (width, height)
    return cv2.resize(image, dsize)


def resize_video(cap, image, new_size, scale_percent=100):
    global width, height
    if new_size in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[new_size]
    elif 0 < scale_percent:
        width = int(cap.get(3) * scale_percent / 100)
        height = int(cap.get(4) * scale_percent / 100)
    dsize = (width, height)
    return cv2.resize(image, dsize)


    # Renvoi le scale en fonction du rapport entre l'image d'origine et la taille souhaitée #

def scale_choice(image_name, new_size) -> int:
    if file_type(image_name) == "image":
        return image_scale_choice(image_name, new_size)
    elif file_type(image_name) == "video":
        return video_scale_choice(image_name, new_size)

# Si le type de fichier = image
def image_scale_choice(image, new_size_width):
    print("original image height  = "+str(cv2.imread(image).shape[1]))
    print("new_size_width = "+str(new_size_width))
    global size_factor
    if new_size_width > cv2.imread(image).shape[1]:
        size_factor = float(new_size_width/cv2.imread(image).shape[1])
    print("size factor = "+str(size_factor))
    if size_factor <= 2.0:
        return 2
    if 2 < size_factor <= 3.0:
        return 3
    if 3 < size_factor <= 4.0:
        return 4
    if size_factor > 4.0:
        return 8

# Si le type de fichier = video
def video_scale_choice(cap, new_size_height):
    size_factor = int(new_size_height/cv2.VideoCapture(cap).get(4))
    print("size factor = "+str(size_factor))
    if size_factor <= 2:
        return 2
    if 2 < size_factor <= 3:
        return 3
    if 3 < size_factor <= 4:
        return 4
    if size_factor > 4:
        return 8

# Renvoi le chemin du modèle choisi
def construct_model_path(model, scale):
    if model == "lapsrn":
        return "./models/LapSRN_x" + str(scale) + ".pb"
    else:
        return "./models/" + model.upper() + "_x" + str(scale) + ".pb"
