import cv2 as cv
import resizeImageAndVideo as rsiv
import os
#import ffmpeg


file_name = "giveon_320x240.mp4"
filename, ext = os.path.splitext(file_name)
out_res = '1080p'
input_path = "test_media/"
output_path = "./results/"
model_name = 'fsrcnn'
model_scale = 4
type_of_image = 'video'
model_path = rsiv.construct_model_path(model_name, model_scale)
outname = filename + "_to_" + out_res + "_with_" + model_name + ext
in_path = input_path+file_name

cap = cv.VideoCapture(in_path)
fps = cap.get(cv.CAP_PROP_FPS)
print("fps = "+str(fps))

width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
#width = cap.get(3)
#height = cap.get(4)
print("cap : "+str(cap))
print("width = "+str(width))
print("height = "+str(height))

outpath = output_path + outname
#dim = rsiv.get_dims(cap, res=out_res)
video_type_cv2 = rsiv.get_video_type(file_name)
out = cv.VideoWriter(outpath, video_type_cv2, cap.get(cv.CAP_PROP_FPS), (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))
sr = cv.dnn_superres.DnnSuperResImpl_create()
print("Reading…")
while True:
    #start = time.time()
    ret, image = cap.read()
    # si fin video
    if not ret:
        break

    sr.readModel(model_path)
    sr.setModel(model_name, model_scale)

    upscaled = sr.upsample(image)
    upscale_from_resize = rsiv.resize_video(cap, image, "", 200)
    downsized = rsiv.donwsize_video(cap, upscaled, model_scale)
    #upscaled.set(3, cap.get(cv.CAP_PROP_FRAME_WIDTH))
    #upscaled.set(4, cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    out.write(downsized)

    #fps_c = (1.0 / (time.time() - start))
    cv.putText(image, 'FPS: {:.2f}'.format(int(cap.get(cv.CAP_PROP_FPS))), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 20, 55), 1)

    cv.imshow("Original frame", image)
    cv.imshow("resize", upscale_from_resize)
    cv.imshow("Upscaled frame", upscaled)
    cv.imshow("Downsized", downsized)
    #out.write(upscaled)
    #print('Shape of Original Image: {}'.format(image.shape))
    if cv.waitKey(int(1000/fps)) & 0xFF == ord('q'):
        print("Stopping…")
        break

"""self.capture_video(input_path).release()
out.release()
cv.destroyAllWindows()"""

cap.release()
out.release()
cv.destroyAllWindows()
print("Stopped")
