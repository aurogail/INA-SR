import cv2 as cv
# from switch_case import switch
import resizeImageAndVideo as rsiv
# import numpy
# import matplotlib.pyplot as plt
# import recordVideo
import os, shutil
import time


class UpscaleImage:

    name: str
    resolution: str
    output_res: str
    #width: int
    #height: int
    model_path: str
    model_name: str
    model_scale: int
    output_name: str
    type_of_image: str
    fps: int

    def __init__(self, name, resolution, output_res, model_path,  model_name, model_scale, output_name, type_of_image, fps):
        self.name = name
        self.resolution = resolution
        self.output_res = output_res
        #self.width = width
        #self.height = height
        self.model_path = model_path
        self.model_name = model_name
        self.model_scale = model_scale
        self.output_name = output_name
        self.type_of_image = type_of_image
        self.fps = fps

    # methode read
    def read_image(self, path):
        inpath = path + self.name
        return cv.imread(inpath)

    def get_file_type(self):
        return rsiv.file_type(self.name)

    def capture_video(self, path):
        inpath = path + self.name
        return cv.VideoCapture(inpath)

    # methode main de l'upscale
    def upscale_image(self, input_path):
        global sr
        sr = cv.dnn_superres.DnnSuperResImpl_create()
        #with switch(self.type_of_image) as case:
        if self.type_of_image == 'image':
            image = self.read_image(input_path)
            sr.readModel(self.model_path)
            sr.setModel(self.model_name, self.model_scale)
            print('Shape of Original Image: {}'.format(image.shape))
            return sr.upsample(image)

        if self.type_of_image == 'video':
            """dim = rsiv.get_dims(self.capture_video(), res=self.resolution)
            video_type_cv2 = rsiv.get_video_type(self.name)
            out = cv.VideoWriter(self.output_name, video_type_cv2, self.fps, dim)"""
            while True:
                start = time.time()
                ret, image = self.capture_video(input_path).read()
                # si fin video
                if not ret:
                    break

                sr.readModel(self.model_path)
                sr.setModel(self.model_name, self.model_scale)

                #out.write(image)

                #fps_c = (1.0 / (time.time() - start))
                cv.putText(image, 'FPS: {:.2f}'.format(self.fps), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 20, 55), 1)

                cv.imshow("Upscaled frame", image)
                print('Shape of Original Image: {}'.format(image.shape))
                if cv.waitKey(20) & 0xFF == ord('q'):
                    break

            """self.capture_video(input_path).release()
            out.release()
            cv.destroyAllWindows()"""
            return sr.upsample(image)

    def save_upscaled_image(self, in_path, out_path):
        upscaled = self.upscale_image(in_path)
        downsized_image = rsiv.donwsize(self.read_image(in_path), upscaled, self.model_scale)
        resize = rsiv.resize_image(self.read_image(in_path), "", 200)
        outpath = out_path + self.output_name
        cv.imshow("origin", self.read_image(in_path))
        print("showing origin")
        cv.imshow("resize", resize)
        print("showing resize")
        cv.imshow("upscaled", upscaled)
        print("showing upscaled")
        cv.imshow("downsized", downsized_image)
        print("showing downsized")
        cv.imwrite(outpath, downsized_image)
        cv.waitKey(0)
        cv.destroyAllWindows()

        print('Shape of Super Resolution Image: {}'.format(upscaled.shape))

    def save_upscaled_video(self, in_path, out_path):
        outpath = out_path + self.output_name
        dim = rsiv.get_dims(self.capture_video(in_path), res=self.resolution)
        video_type_cv2 = rsiv.get_video_type(self.name)
        out = cv.VideoWriter(outpath, video_type_cv2, self.fps, dim)
        out.write(self.upscale_image(in_path))
        self.capture_video(input_path).release()
        out.release()
        cv.destroyAllWindows()

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
#name: str
##resolution: str
#output_res: str
##width: int
##height: int
#model_path: str
#model_name: str
#model_scale: int
#output_name: str
#type_of_image: str
#fps: int


file_name = "bird2.jpg"
filename, ext = os.path.splitext(file_name)
#fps = 0
out_res = '1080p'
input_path = "test_media/"
output_path = "./results/"
destination_de_copie = "./test_media/"
#upscaled_image = UpscaleImage(name='', resolution='', output_name='', output_res='', model_name='', model_path='', model_scale='', type_of_image='', fps=0)
#upscaled_video = UpscaleImage(name='', resolution='', output_name='', output_res='', model_name='', model_path='', model_scale='', type_of_image='', fps=0)

"""inputpath = input_path + file_name
modelpath = "./models/EDSR_x4.pb"
modelname = "edsr"
modelscale = 4
out_name = filename + "_to_" + out_res + "_with_" + modelname + ext
outpath = output_path + out_name
sr = cv.dnn_superres.DnnSuperResImpl_create()
image = cv.imread(inputpath)
sr.readModel(modelpath)
sr.setModel(modelname, modelscale)
#print('Shape of Original Image: {}'.format(image.shape))
out = sr.upsample(image)
cv.imwrite(outpath, out)"""


def copy_to_folder_media(filename, destination):
    shutil.move(filename, destination)


# a faire selon type de fichier (image ou video)
# a faire pendant que la page est ouverte ? While x.isOpended() ?
def upscale_main(file_name):
    if rsiv.file_type(file_name) == 'image':
        print("Type of file = "+rsiv.file_type(file_name))
        upscaled_image = UpscaleImage(name=file_name, resolution='', output_name='', output_res='', model_name='edsr', model_path='', model_scale=4, type_of_image='image', fps=0)
        #upscaled_image.name = file_name
        #upscaled_image.output_name = out_name
        #upscaled_image.type_of_image = 'image'
        upscaled_image.output_res = out_res
        #upscaled_image.model_scale = rsiv.scale_choice(upscaled_image.read_image(input_path), rsiv.get_dims(upscaled_image.read_image(input_path), upscaled_image.output_res)[1])
        print("scale choice = "+str(upscaled_image.model_scale))
        #upscaled_image.model_name = rsiv.model_choice('image', upscaled_image.model_scale)
        print("Model choice : "+str(upscaled_image.model_name))
        upscaled_image.model_path = rsiv.construct_model_path(upscaled_image.model_name, upscaled_image.model_scale)
        upscaled_image.output_name = filename + "_to_" + out_res + "_with_" + upscaled_image.model_name + ext
        #upscaled_image.upscale_image(input_path)
        #rsiv.resize_image(upscaled_image.save_upscaled_image(), upscaled_image.output_res)
        upscaled_image.save_upscaled_image(input_path, output_path)

    if rsiv.file_type(file_name) == 'video':
        upscaled_video = UpscaleImage(name=file_name, resolution='', output_name='', output_res='', model_name='espcn', model_path='', model_scale=4, type_of_image='video', fps=0)
        #upscaled_video.name = file_name
        #upscaled_video.output_name = out_name
        #upscaled_video.type_of_image = 'video'
        upscaled_video.fps = upscaled_video.capture_video(input_path).get(cv.CAP_PROP_FPS)

        #upscaled_video.output_res = out_res
        #upscaled_video.model_scale = rsiv.video_scale_choice(upscaled_video.capture_video(input_path), rsiv.get_dims(upscaled_video.capture_video(input_path), upscaled_video.output_res)[1])
        #upscaled_video.model_name = rsiv.model_choice('video', upscaled_video.model_scale)
        upscaled_video.model_path = rsiv.construct_model_path(upscaled_video.model_name, upscaled_video.model_scale)
        upscaled_video.output_name = filename + "_to_" + out_res + "_with_" + upscaled_video.model_name + ext
        #upscaled_video.upscale_image(output_path)
        #rsiv.resize_video()
        upscaled_video.save_upscaled_video(input_path, output_path)


# resize si bouton d'une res standard, sinon, ne pas resize ? mettre x2 x4 x8 ?
