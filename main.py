# ---------------------------------------------------------------------------------------------------
# Este archivo contiene un ejemplo del uso del sistema
# ---------------------------------------------------------------------------------------------------

from capturer import process_video, process_image
from report import clean_up
import cv2
import os


def main():

    video_path = "videos/video_1.mp4"

    process_video(video_path)

    clean_up()

main()