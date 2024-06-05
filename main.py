# ---------------------------------------------------------------------------------------------------
# Este archivo contiene un ejemplo del uso del sistema
# ---------------------------------------------------------------------------------------------------

from capturer import process_video, process_image
from report import clean_up
import cv2
import time

def main():

    video_path = "videos/video_1.mp4"

    process_video(video_path)

    clean_up()

    # ---------------------------------------------

    img_path = "images/149.jpg"

    img = cv2.imread(img_path)

    start_time = time.time()
    process_image(img)
    end_time = time.time()

    execution_time = end_time - start_time
    print("Tiempo de ejecución de una imagen:", execution_time, "segundos")

    clean_up()

main()