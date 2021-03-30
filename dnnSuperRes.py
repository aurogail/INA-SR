import cv2
from switch_case import switch
import resizeImageAndVideo as rsiv
import numpy as np
import matplotlib.pyplot as plt
import recordVideo
import os
import time


class UpscaleImage(cv2):

    name: str
    resolution: str
    output_res: str
    width: int
    height: int
    model_path: str
    model_name: str
    model_scale: int
    output_name: str
    type_of_image: str
    fps: int

    def __init__(self, name, resolution, output_res, width, height, model_path,  model_name, model_scale, output_name, type_of_image, fps):
        self.name = name
        self.resolution = resolution
        self.output_res = output_res
        self.width = width
        self.height = height
        self.model_path = model_path
        self.model_name = model_name
        self.model_scale = model_scale
        self.output_name = output_name
        self.type_of_image = type_of_image
        self.fps = fps

    def upscale_image(self):
        global sr
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        with switch(self.type_of_image) as case:
            if case("image"):
                image = self.self.imread(self.name)
                sr.readModel(self.model_path)
                sr.setModel(self.model_name, self.model_scale)
                print('Shape of Original Image: {}'.format(image.shape))
                return sr.upsample(image)

            if case("video"):
                cap = self.VideoCapture(self.name)
                dim = rsiv.get_dims(cap, res=self.resolution)
                video_type_cv2 = rsiv.get_video_type(self.name)
                out = self.VideoWriter(self.name, video_type_cv2, self.fps, dim)
                while cap.isOpened():
                    start = time.time()
                    ret, image = cap.read()
                    # si fin video
                    if not ret:
                        break

                    sr.readModel(self.model_path)
                    sr.setModel(self.model_name, self.model_scale)

                    out.write(image)

                    fps = (1.0 / (time.time() - start))
                    self.putText(image, 'FPS: {:.2f}'.format(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,0.8, (255, 20, 55), 1)

                    self.imshow("Upscaled frame", image)
                    print('Shape of Original Image: {}'.format(image.shape))
                    if self.waitKey(20) & 0xFF == ord('q'):
                        break
                    return sr.upsample(image)
                cap.release()
                out.release()
                self.destroyAllWindow()

    def save_upscaled_image(self):
        self.imwrite(self.output_name, self.upscale_image())
        print('Shape of Super Resolution Image: {}'.format(self.upscale_image().shape))

    # def save_upscaled_video(self, cap):
        # self.VideoWriter(self.name, videoTypeCV2, fps, dim)


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

