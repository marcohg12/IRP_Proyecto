# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del clasificador del sistema
# ---------------------------------------------------------------------------------------------------

from ultralytics import YOLO 
import cv2
from contants import TEST_FLAG

MODEL = None

# Recibe una imagen cargada con openCV y la marca de tiempo de la imagen
# Realiza el conteo de lapas en la imagen con el modelo entrenado con YOLO
# Retorna la cantidad de lapas detectadas en la imagen con una confianza de
# al menos un 0.9
def detect_macaws(image, time_stamp):
    
    global MODEL
    global TEST_FLAG

    # Se carga el modelo si no se ha cargado
    if (not MODEL):
        MODEL = YOLO("training/runs/detect/train/weights/best.pt", task = "detect")  

    # Se realiza la clasificación con el modelo
    results = MODEL(image, conf = 0.9)

    num_macaws = 0
    
    # Se hace el conteo de lapas
    for result in results:

        boxes = result.boxes
        num_macaws += len(boxes)

        if (TEST_FLAG):
            cv2.imwrite(f"test_data/images_results/{time_stamp}.jpg", image)
    
    return num_macaws