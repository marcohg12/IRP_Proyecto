# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del clasificador del sistema
# ---------------------------------------------------------------------------------------------------

from ultralytics import YOLO 
import cv2
from detecto import core
from contants import TEST_FLAG
from PIL import Image

MODEL = None

def clean_up_model():

    global MODEL
    MODEL = None

# Recibe una imagen cargada con openCV y la marca de tiempo de la imagen
# Realiza el conteo de lapas en la imagen con el modelo indicado por el parámetro (YOLO o DETECTO)
# Retorna la cantidad de lapas detectadas en la imagen con una confianza de
# al menos un 0.9
def detect_macaws(image, time_stamp, model_to_use):

    num_macaws = 0
    global MODEL
    global TEST_FLAG

    # Clasificación con YOLO
    if (model_to_use == "YOLO"):
        
        if (not MODEL):
            MODEL = YOLO("training/runs/detect/train5/weights/best.pt", task = "detect") 
        
        results = MODEL(image, conf = 0.90)

        for result in results:
            
            boxes = result.boxes
            num_macaws += len(boxes)
            
        if (TEST_FLAG):
            cv2.imwrite(f"test_data/images_results/{time_stamp}.jpg", image, num_macaws)

    # Clasificación con DETECTO
    elif (model_to_use == "DETECTO"):

        if (not MODEL):
            MODEL = core.Model.load('model_weights.pth', ['Lapa'])

        pil_image = Image.fromarray(image)

        labels, _, scores = MODEL.predict(pil_image)

        print(scores, time_stamp)
        
        for i in range(0, len(labels)):
            
            if (scores[i] > 0.90):
                num_macaws += 1
    
    return num_macaws