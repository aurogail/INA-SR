import os
import cv2

    # Dictionnaires #

# Extension : Type de fichier
FILE_TYPE = {
    '.avi': 'video',
    '.mkv': 'video',
    '.mp4': 'video',
    '.jpg': 'image',
    '.png': 'image'
}

# Résolution : (Width, Height)
STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160)
}

# Extension de vidéo : Codec
VIDEO_TYPE = {
    '.avi': cv2.VideoWriter_fourcc(*'avc1'),
    '.mkv': cv2.VideoWriter_fourcc(*'avc1'),
    '.mp4': cv2.VideoWriter_fourcc(*'mp4v')
}

    # Certaines fonctions apparaissent dans plusieurs fichiers pour éviter les redondances d'import #

def construct_model_path(model, scale):
    if model == "lapsrn":
        return "./models/LapSRN_x" + str(scale) + ".pb"
    else:
        return "./models/" + model.upper() + "_x" + str(scale) + ".pb"

# Affiche l'extension dans la console
def file_type_ext(file_name):
    name, ext = os.path.splitext(file_name)
    print("ext : ", ext)

# Renvoie le type de fichier (image ou video)
def file_type(file_name):
    name, ext = os.path.splitext(file_name)
    if ext.lower() in FILE_TYPE:
        print("filetype : " + FILE_TYPE[ext])
        return FILE_TYPE[ext]
    else:
        return ''

# Renvoi le codec en fonction de l'extention
def get_video_type(fileName):
    filename, ext = os.path.splitext(fileName)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

# Renvoi (Width, Height) en fonction de la resolution (et type de fichier)
def get_dims(image, res="1080p"):
    if file_type(image) == "image":
        image_get_dims(res)
    elif file_type(image) == "video":
        video_get_dims(res)


def video_get_dims(res="1080p"):
    global width, height
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        return STD_DIMENSIONS[res]

    return width, height


def image_get_dims(res="1080p"):
    global width, height
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width = STD_DIMENSIONS[res][0]
        height = STD_DIMENSIONS[res][1]

    return height, width
