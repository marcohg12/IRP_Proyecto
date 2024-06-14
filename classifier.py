# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del clasificador del sistema
# ---------------------------------------------------------------------------------------------------

# from ultralytics import YOLO 
# import cv2
# from contants import TEST_FLAG
import torch
import torchvision.transforms as T
from torchvision.models.detection import fasterrcnn_resnet50_fpn
import cv2
import numpy as np
from contants import TEST_FLAG

def load_model():
    # Load the pretrained Faster R-CNN model
    model = fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    return model

# Recibe una imagen cargada con openCV y la marca de tiempo de la imagen
# Realiza el conteo de lapas en la imagen con el modelo entrenado con YOLO
# Retorna la cantidad de lapas detectadas en la imagen con una confianza de
# al menos un 0.9

# FUNCION CON YOLO
# def detect_macaws(image, time_stamp):
    
#     global MODEL
#     global TEST_FLAG

#     # Se carga el modelo si no se ha cargado
#     if (not MODEL):
#         MODEL = YOLO("training/runs/detect/train/weights/best.pt", task = "detect")  

#     # Se realiza la clasificación con el modelo
#     results = MODEL(image, conf = 0.9)

#     num_macaws = 0
    
#     # Se hace el conteo de lapas
#     for result in results:

#         boxes = result.boxes
#         num_macaws += len(boxes)

#         if (TEST_FLAG):
#             cv2.imwrite(f"test_data/images_results/{time_stamp}.jpg", image)
    
#     return num_macaws

def detect_macaws(image, time_stamp, model):
    # Transformation to apply to the images
    transform = T.Compose([
        T.ToTensor()
    ])

    # Apply the transformations to the image
    image_tensor = transform(image).unsqueeze(0)

    # Perform inference
    with torch.no_grad():
        outputs = model(image_tensor)

    # Filter out the results
    num_macaws = 0
    for box, score, label in zip(outputs[0]['boxes'], outputs[0]['scores'], outputs[0]['labels']):
        if score >= 0.9 and label == 18:  # Assuming class 18 is for macaws
            num_macaws += 1

    if TEST_FLAG:
        cv2.imwrite(f"test_data/images_results/{time_stamp}.jpg", image)
    
    return num_macaws