import cv2
from switch_case import switch
import resizeImageAndVideo as rsiv
# import numpy as np
# import matplotlib.pyplot as plt
# import recordVideo
# import os
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

    # methode read
    def read_image(self):
        return self.imread(self.name)

    def capture_video(self):
        return self.VideoCapture(self.name)

    # methode main de l'upscale
    def upscale_image(self):
        global sr
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        with switch(self.type_of_image) as case:
            if case("image"):
                image = self.read_image()
                sr.readModel(self.model_path)
                sr.setModel(self.model_name, self.model_scale)
                print('Shape of Original Image: {}'.format(image.shape))
                return sr.upsample(image)

            if case("video"):
                dim = rsiv.get_dims(self.capture_video(), res=self.resolution)
                video_type_cv2 = rsiv.get_video_type(self.name)
                out = self.VideoWriter(self.name, video_type_cv2, self.fps, dim)
                while self.capture_video().isOpened():
                    start = time.time()
                    ret, image = self.capture_video().read()
                    # si fin video
                    if not ret:
                        break

                    sr.readModel(self.model_path)
                    sr.setModel(self.model_name, self.model_scale)

                    out.write(image)

                    fps_c = (1.0 / (time.time() - start))
                    self.putText(image, 'FPS: {:.2f}'.format(fps_c), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 20, 55), 1)

                    self.imshow("Upscaled frame", image)
                    print('Shape of Original Image: {}'.format(image.shape))
                    if self.waitKey(20) & 0xFF == ord('q'):
                        break
                    return sr.upsample(image)
                self.capture_video().release()
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

# boutons => creer des instances avec les choix
# var des boutons -> switch case -> attributs des instances
upscaled_image = UpscaleImage(name="", resolution="", output_res="", output_name="", width=0, height=0, fps=0, model_name="", model_path="", model_scale=0, type_of_image="")
upscaled_video = UpscaleImage(name="", resolution="", output_res="", output_name="", width=0, height=0, fps=0, model_name="", model_path="", model_scale=0, type_of_image="")
file_name: str = ""
type_of_image: str = ""
fps: int = 0
out_res: str = ""

# a faire selon type de fichier (image ou video)
# a faire pendant que la page est ouverte ? While x.isOpended() ?
with switch(type_of_image) as case:
    if case("image"):
        upscaled_image.name = file_name
        upscaled_image.type_of_image = type_of_image
        upscaled_image.output_res = out_res
        upscaled_image.model_scale = rsiv.scale_choice(upscaled_image.read_image(), rsiv.get_dims(upscaled_image.read_image(), upscaled_image.output_res)[0])
        upscaled_image.model_name = rsiv.model_choice(type_of_image, upscaled_image.model_scale)
        upscaled_image.model_path = rsiv.construct_model_path(upscaled_image.model_name, upscaled_image.model_scale)

    if case("video"):
        upscaled_video.name = file_name
        upscaled_video.type_of_image = type_of_image
        upscaled_video.fps = fps
        upscaled_video.output_res = out_res
        upscaled_video.model_scale = rsiv.scale_choice(upscaled_video.capture_video(), rsiv.get_dims(upscaled_video.capture_video(), upscaled_video.output_res)[0])
        upscaled_video.model_name = rsiv.model_choice(type_of_image, upscaled_video.model_scale)
        upscaled_video.model_path = rsiv.construct_model_path(upscaled_video.model_name, upscaled_video.model_scale)
