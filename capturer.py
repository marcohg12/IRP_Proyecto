# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del capturador de imágenes y video del sistema
# ---------------------------------------------------------------------------------------------------

import cv2 
from report import process_time_stamp, report_director
from classifier import detect_macaws
from preprocess import noise_removal, improve_lighting, improve_sharpness, intesify_color
from filter import detect_macaw_coordinates, crop_image
from contants import TEST_FLAG

# Recibe la ruta del video a procesar
# Procesa el video frame por frame. Por cada frame, se envía al procesador de imágenes
# junto con la marca de tiempo del frame
def process_video(video_path, model_to_use):

    video_capture = cv2.VideoCapture(video_path)
    frame_count = 0
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps) 
    
    while video_capture.isOpened():

        ret, frame = video_capture.read()
        
        if ret and frame_count % frame_interval == 0:

            time_stamp = video_capture.get(cv2.CAP_PROP_POS_MSEC)
            time_stamp = (int(time_stamp) // 60000, int((time_stamp % 60000) / 1000))

            process_image(frame, model_to_use, time_stamp)
            
        frame_count += 1
        
        if not ret:
            break
    
    video_capture.release()
    cv2.destroyAllWindows()

# Recibe una imagen cargada con openCV y la marca de tiempo de la imagen
# Aplica el preprocesamiento y filtrado de la imagen. Luego, envía la imagen
# para la clasificación con YOLO y luego al director de reporte
def process_image(image, model_to_use, time_stamp = (0, 0)):

    global TEST_FLAG

    # Procesamiento de marca de tiempo
    process_time_stamp(time_stamp)

    # Preprocesamiento de la imagen
    noise_reduced_img = noise_removal(image)
    color_improved_img = intesify_color(noise_reduced_img)
    lighting_improved_img = improve_lighting(color_improved_img)
    sharpness_improved_img = improve_sharpness(lighting_improved_img)

    # Obtención del área de interés
    interest_area = detect_macaw_coordinates(sharpness_improved_img)

    # Se filtra la imagen si no hay área de interes
    if (interest_area == [] or interest_area[0][2] == 0 or interest_area[0][3] == 0):

        report_director(0)

        if (TEST_FLAG):
            with open('test_data/results2.txt', 'a') as file:
                file.write(f'image_{time_stamp}.jpg ' + str(0) + '\n')

    else:

        # Se reduce la imagen al área de interés
        reduced_img = crop_image(sharpness_improved_img, interest_area[0])

        # Se clasifica la imagen y se envía el resultado al director de reporte
        num_macaws = detect_macaws(reduced_img, time_stamp, model_to_use)
        report_director(num_macaws)

        if (TEST_FLAG):

            cv2.imwrite(f'test_data/images_analize/image_{time_stamp}.jpg', image)

            with open('test_data/results2.txt', 'a') as file:
                file.write(f'image_{time_stamp}.jpg ' + str(num_macaws) + '\n')