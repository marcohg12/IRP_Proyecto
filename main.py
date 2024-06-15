# ---------------------------------------------------------------------------------------------------
# Este archivo contiene un ejemplo del uso del sistema
# ---------------------------------------------------------------------------------------------------

from capturer import process_video, process_image
from report import clean_up
import cv2
import time

def main():

    video_path = "videos/video_1.mp4"

    start_time = time.time()
    process_video(video_path, "YOLO")
    end_time = time.time()

    clean_up()

    execution_time = end_time - start_time
    print("Tiempo de ejecución del video con YOLO:", execution_time, "segundos")

    # # ---------------------------------------------

    start_time = time.time()
    process_video(video_path, "DETECTO")
    end_time = time.time()

    clean_up()

    execution_time = end_time - start_time
    print("Tiempo de ejecución del video con DETECTO:", execution_time, "segundos")

    # # ---------------------------------------------

    img_path = "images/149.jpg"

    img = cv2.imread(img_path)

    start_time = time.time()
    process_image(img, "DETECTO")
    end_time = time.time()

    execution_time = end_time - start_time
    print("Tiempo de ejecución de una imagen:", execution_time, "segundos")

    clean_up()

main()