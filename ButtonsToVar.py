import FileType
import resizeImageAndVideo as rsiv
from dnnSuperRes import UpscaleImage

    # Dictionnaires #

# Bouton : modèle
model = {
    "fast": "espcn",
    "best": "edsr"
}

# Bouton : échelle de upscale
SCALES = {
    "x2": 2,
    "x3": 3,
    "x4": 4,
    "x8": 8
}

    # Fonctions appelée par les boutons #

# Assigne le nom du fichier
def get_filename(VideoPlayerObject, UpscaleImageObject):
    UpscaleImageObject.name = VideoPlayerObject.filename
    #return VideoPlayerObject.filename

# Assigne le nom du modele à l'attribut name de l'objet en question
def get_model_name(button: str, UpscaleImageObject: UpscaleImage):

    if button.lower() in model:
        UpscaleImageObject.model_name = model[button]
        print(UpscaleImageObject.model_name)
        #return model[button]

# Assigne le scale (échelle) du modele à l'attribut name de l'objet en question
def get_model_scale(button: str, UpscaleImageObject: UpscaleImage):
    print("Upscale : " + str(UpscaleImageObject))
    if button == 'uhd':
        UpscaleImageObject.model_scale = int(rsiv.scale_choice(UpscaleImageObject.name, rsiv.get_dims(UpscaleImageObject.name, "4k")[1]))
    elif button == 'hd':
        UpscaleImageObject.model_scale = int(rsiv.scale_choice(UpscaleImageObject.name, rsiv.get_dims(UpscaleImageObject.name, "1080p")[1]))
    else:
        if button.lower() in SCALES:
            UpscaleImageObject.model_scale = SCALES[button]
            print("model scale : " + str(UpscaleImageObject.model_scale))

# Vérifie si le upscale est possible avec ces deux paramètres
def verif_scale_pour_model(scale, Upscale: UpscaleImage):
    if scale == 8:
        Upscale.model_name = "lapsrn"
        return Upscale.model_name
    elif scale < 8:
        if scale == 3:
            if Upscale.model_name == "lapsrn":
                return "espcn"
            else:
                if Upscale.model_name == "edsr":
                    if FileType.file_type(Upscale.name) == "video":
                        Upscale.model_name = "fsrcnn"
                        print("Modèle choisi par verif : " + Upscale.model_name)
                        return Upscale.model_name
                    else:
                        print("Modèle choisi par verif : " + Upscale.model_name)
                        return Upscale.model_name
        else:
            if Upscale.model_name == "edsr":
                if FileType.file_type(Upscale.name) == "video":
                    Upscale.model_name = "lapsrn"
                    print("Modèle choisi par verif : " + Upscale.model_name)
                    return Upscale.model_name
                else:
                    print("Modèle choisi par verif : " + Upscale.model_name)
                    return Upscale.model_name
    return Upscale.model_name
