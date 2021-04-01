import os
import cv2
from switchcase import switch

# cap = cv2.VideoCapture(0)

STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160)
}


VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID')
}


def change_resolution(capture, width, height):
    capture.set(3, width)
    capture.set(4, height)


def get_video_type(fileName):
    filename, ext = os.path.splitext(fileName)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


def get_dims(capture, res="1080p"):
    global width, height
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]
        change_resolution(capture, width, height)
    return width, height


def resize_image(image, original_size, new_size, scale_percent=100):
    # for standard size
    # src = cv2.imread('D:/cv2-resize-image-original.png', cv2.IMREAD_UNCHANGED)

    global width, height

    # size_factor = int(new_size/image.shape[1])

    if new_size in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[new_size]
    elif 0 < scale_percent < 100:
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)
    # resize image
    return cv2.resize(image, dsize)


def scale_choice(image, new_size_width):
    size_factor = int(new_size_width/image.shape[1])

    with switch(size_factor) as case:
        if case(size_factor) <= 2:
            return 2

        if 2 < case(size_factor) <= 3:
            return 3

        if 3 < case(size_factor) <= 4:
            return 4

        if case(size_factor) > 4:
            return 8


def video_scale_choice(cap, new_size_width):
    size_factor = int(new_size_width/cap.get(3))

    with switch(size_factor) as case:
        if case(size_factor) <= 2:
            return 2

        if 2 < case(size_factor) <= 3:
            return 3

        if 3 < case(size_factor) <= 4:
            return 4

        if case(size_factor) > 4:
            return 8


def model_choice(type_of_image, scale):
    with switch(type_of_image) as case:
        if case("video"):
            if scale <= 4:
                return "espcn"
            else:
                return "lapsrn"
        if case("image"):
            if scale <= 4:
                return "edsr"
            else:
                return "lapsrn"


def construct_model_path(model, scale):
    if model == "lapsrn":
        return os.path.join("./models/LapSRN_x" + scale + ".pb")
    else :
        return os.path.join("./models/", model.upper() + "_x" + scale + ".pb")
