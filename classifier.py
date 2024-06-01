# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del clasificador del sistema
# ---------------------------------------------------------------------------------------------------

from ultralytics import YOLO 

MODEL = None

def detect_macaws(image):

    global MODEL

    if (not MODEL):
        MODEL = YOLO("best.pt", task = "detect")  

    results = MODEL(image, conf = 0.9)

    num_macaws = 0
    
    for result in results:
        boxes = result.boxes
        
        num_macaws += len(boxes)
    
    return num_macaws