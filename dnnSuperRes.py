import cv2
import numpy as np
import matplotlib.pyplot as plt
import recordVideo
import os
import time


class Image(cv2):

    name: str
    resolution: str
    width: int
    height: int
    model_path: str
    model_name: str
    model_scale: int
    output_name: str

    def __init__(self, name, resolution, width, height, model_path,  model_name, model_scale, output_name):
        self.name = name
        self.resolution = resolution
        self.width = width
        self.height = height
        self.model_path = model_path
        self.model_name = model_name
        self.model_scale = model_scale
        self.output_name = output_name

    def read_image(self):
        return self.imread(self.name)

    def upscale_image(self):
        global sr
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        image = self.read_image()
        sr.readModel(self.model_path)
        sr.setModel(self.model_name, self.model_scale)
        print('Shape of Original Image: {}'.format(image.shape))
        return sr.upsample(image)

    def save_upscaled_image(self):
        self.imwrite(self.output_name, self.upscale_image())
        print('Shape of Super Resolution Image: {}'.format(self.upscale_image().shape))


# imageName: str = "./bird2.JPG"
# outputName: str = "./upscaled.png"
# path: str = "models/EDSR_x4.pb"
# model: str = "edsr"
# modelscale: int = 4
# model for video : ESPCN
# def resize_image(image_name, output_size):
# control de la size ?
# scale ?
# matplotlib ?


