import os
import cv2
# from switchcase import switch

# cap = cv2.VideoCapture(0)

STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160)
}


VIDEO_TYPE = {
    '.avi': cv2.VideoWriter_fourcc(*'H264'),
    '.mp4': cv2.VideoWriter_fourcc(*'XVID')
}


FILE_TYPE = {
    '.avi': 'video',
    '.mp4': 'video',
    '.jpg': 'image',
    '.png': 'image'
}


def file_type(file_name):
    name, ext = os.path.splitext(file_name)
    if ext in FILE_TYPE:
        return FILE_TYPE[ext]
    else:
        return ''


"""def change_resolution(capture, width, height):
    capture.set(3, width)
    capture.set(4, height)"""


def get_video_type(fileName):
    filename, ext = os.path.splitext(fileName)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


def video_get_dims(capture, res="1080p"):
    global width, height
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        return STD_DIMENSIONS[res]
        #change_resolution(capture, width, height)
    return width, height


def get_dims(capture, res="1080p"):
    global width, height
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width = STD_DIMENSIONS[res][0]
        height = STD_DIMENSIONS[res][1]
        #change_resolution(capture, width, height)
    return height, width


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


def resize_image(image, new_size, scale_percent=100):
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
    #dsize = (height, width)
    dsize = (width, height)
    # resize image
    return cv2.resize(image, dsize)


def resize_video(cap, new_size, scale_percent=100):
    global width, height

    if new_size in STD_DIMENSIONS:
        width = STD_DIMENSIONS[new_size][0]
    elif 0 < scale_percent < 100:
        width = int(cap.get(3) * scale_percent / 100)
        height = int(cap.get(4) * scale_percent / 100)
    cap.set(3, width)
    cap.set(4, height)


def scale_choice(image, new_size_width):
    print("original image height  = "+str(image.shape[1]))
    print("new_size_width = "+str(new_size_width))
    global size_factor
    if new_size_width > image.shape[1]:
        size_factor = float(new_size_width/image.shape[1])
    print("size factor = "+str(size_factor))

    #with switch(size_factor) as case:
    if size_factor <= 2.0:
        return 2

    if 2 < size_factor <= 3.0:
        return 3

    if 3 < size_factor <= 4.0:
        return 4

    if size_factor > 4.0:
        return 8


def video_scale_choice(cap, new_size_height):
    size_factor = int(new_size_height/cap.get(4))
    print("size factor = "+str(size_factor))

    #with switch(size_factor) as case:
    if size_factor <= 2:
        return 2

    if 2 < size_factor <= 3:
        return 3

    if 3 < size_factor <= 4:
        return 4

    if size_factor > 4:
        return 8


def model_choice(type_of_image, scale):
    if type_of_image == 'video':
        if scale <= 4:
            return "espcn"
        else:
            return "lapsrn"
    if type_of_image == 'image':
        if scale <= 4:
            return "edsr"
        else:
            return "lapsrn"


def construct_model_path(model, scale):
    if model == "lapsrn":
        return "./models/LapSRN_x" + str(scale) + ".pb"
    else:
        return "./models/" + model.upper() + "_x" + str(scale) + ".pb"
