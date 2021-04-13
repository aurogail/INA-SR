from dnnSuperRes import UpscaleImage
import resizeImageAndVideo as rsiv

"""MODELS = {
    "uhd": "",
    "hd": "",
    "fast": "espcn",
    "best": "edsr"
}"""

SCALES = {
    "x2": 2,
    "x3": 3,
    "x4": 4,
    "x8": 8
}


def get_filename(VideoPlayerObject, UpscaleImageObject):
    UpscaleImageObject.name = VideoPlayerObject.filename
    #return VideoPlayerObject.filename


def get_model_name(button, UpscaleImageObject):

    model = {
        "uhd": rsiv.model_choice(rsiv.file_type(UpscaleImageObject.name), rsiv.scale_choice(UpscaleImageObject, "4k")),
        "hd": rsiv.model_choice(rsiv.file_type(UpscaleImageObject.name), rsiv.scale_choice(UpscaleImageObject, "1080p")),
        "fast": "espcn",
        "best": "edsr"
    }
    if button.lower() in model:
        UpscaleImageObject.model_name = model[button]
        return model[button]
    else:
        return ""


def get_model_scale(button, UpscaleImageObject):
    #if int(button.lower())
    if button.lower() in SCALES:
        UpscaleImageObject.model_scale = SCALES[button]
        return SCALES[button]
    else:
        return 0


def verif_scale_pour_model(scale, model):
    if scale == 8:
        return "lapsrn"
    elif scale == 3 & model == "lapsrn":
        return "espcn"
    else:
        return model
