# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del capturador de imágenes y video del sistema
# ---------------------------------------------------------------------------------------------------

import cv2 
from report import process_time_stamp, report_director
from classifier import detect_macaws
from preprocess import noise_removal, improve_lighting, improve_sharpness, intesify_color
from filter import detect_macaw_coordinates, crop_image
import matplotlib.pyplot as plt

def process_video(video_path):

    video_capture = cv2.VideoCapture(video_path)
    frame_count = 0
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps) 
    
    while video_capture.isOpened():

        ret, frame = video_capture.read()
        
        if ret and frame_count % frame_interval == 0:

            time_stamp = video_capture.get(cv2.CAP_PROP_POS_MSEC)
            time_stamp = (int(time_stamp) // 60000, int((time_stamp % 60000) / 1000))

            process_image(frame, time_stamp)
            
        frame_count += 1
        
        if not ret:
            break
    
    video_capture.release()
    cv2.destroyAllWindows()
    
def process_image(image, time_stamp):

    process_time_stamp(time_stamp)

    noise_reduced_img = noise_removal(image)
    color_improved_img = intesify_color(noise_reduced_img)
    lighting_improved_img = improve_lighting(color_improved_img)
    sharpness_improved_img = improve_sharpness(lighting_improved_img)

    interest_area = detect_macaw_coordinates(sharpness_improved_img)

    if (interest_area == []):

        report_director(0)

    else:

        reduced_img = crop_image(sharpness_improved_img, interest_area[0])
        cv2.imwrite(f'images_analize\image_{time_stamp}.jpg', image)
        num_macaws = detect_macaws(reduced_img, time_stamp)
        report_director(num_macaws)
        with open('results2.txt', 'a') as file:
            file.write(f'image_{time_stamp}.jpg ' + str(num_macaws) + '\n')