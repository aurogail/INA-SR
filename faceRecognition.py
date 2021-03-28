#import numpy as np
import os
import cv2

fileName = 'video.avi'
fps = 25.0
resolution = '720p'


def change_resolution(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


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
"""def searchExt(fileName):
    for i in len(fileName):
        arrayFileName = fileName[i]
    if '.' in fileName:
        for i in [4, 3, 2]:
            ext =+ fileName[i]
        return  ext
    return 'ext'"""


def get_video_type(fileName):
    filename, ext = os.path.splitext(fileName)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


def get_dims(cap, res="1080p"):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]
    change_resolution(cap, width, height)
    return width, height


"""creer un objet capturant l'appareil webcam par defaut"""

"""cascade classifier, !! frontalface a utiliser sur une image en niveau de gris !!"""
faceCascade = cv2.CascadeClassifier('haarCascades/haarcascade_frontalface_alt2.xml')
"""'Desktop/haarCascades/haarcascade_frontalface_alt2.xml'"""

cap = cv2.VideoCapture(0)
dim = get_dims(cap, res=resolution)
videoTypeCV2 = get_video_type(fileName)

out = cv2.VideoWriter(fileName, videoTypeCV2, fps, dim)

"""dans cv2, set -> 3 = width et 4 = height"""
"""Loop permettant l'utilisation continue"""

while True:
    """lire frame par frame"""
    ret, frame = cap.read()

    """convertir en niveau de gris"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    """detecter les visages via le classifier"""
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        print(x, y, w, h)

    out.write(frame)

    """afficher cette image sur l'ordi"""
    cv2.imshow('frame', gray)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

"""release"""
cap.release()
out.release()
cv2.destroyAllWindows()