import cv2
import numpy as np
import matplotlib.pyplot as plt
import recordVideo
import os
import time

imageName: str = "./bird2.JPG"
outputName: str = "./upscaled.jpg"
path: str = "models/EDSR_x4.pb"
model: str = "edsr"
model_scale: int = 4

# upscale single image func
def upscale_image(image_name, model_path, model_name, scale, output_name):
    # Create an SR object - only function that differs from c++ code
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    # Read image
    image = cv2.imread(image_name)
    # Read the desired model
    sr.readModel(model_path)
    # Set the desired model and scale to get correct pre- and post-processing
    sr.setModel(model_name, scale)
    # Upscale the image
    result = sr.upsample(image)
    # Save the image
    cv2.imwrite(output_name, result)


# control de la size ?
# scale ?
# matplotlib ?


