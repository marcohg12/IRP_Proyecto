# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del clasificador del sistema
# ---------------------------------------------------------------------------------------------------

from ultralytics import YOLO 
import cv2

MODEL = None

def detect_macaws(image, time_stamp):
    

    global MODEL

    if (not MODEL):
        MODEL = YOLO("best.pt", task = "detect")  

    results = MODEL(image, conf = 0.9)

    num_macaws = 0
    
    for result in results:
        boxes = result.boxes
        
        num_macaws += len(boxes)
        result.show()
        cv2.imwrite(f"images_results\{time_stamp}.jpg", image)
    
    return num_macaws