import os
import cv2

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
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]
    change_resolution(capture, width, height)
    return width, height


def resize_image(image, original_size, new_size, scale_percent):
    # for standard size
    # src = cv2.imread('D:/cv2-resize-image-original.png', cv2.IMREAD_UNCHANGED)
    # percent by which the image is resized
    scale_percent = 50
    # calculate the 50 percent of original dimensions
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    # dsize
    dsize = (width, height)
    # resize image
    return cv2.resize(image, dsize)
