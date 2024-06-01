# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del clasificador del sistema
# ---------------------------------------------------------------------------------------------------
from ultralytics import YOLO 
import os

#Function to detect macaws in an image
def detect_macaws(image_path):
    model = YOLO("Train4.0/runs/detect/train/weights/best.pt", task="detect")  

    results = model(image_path)

    num_macaws = 0
    
    for result in results:
        boxes = result.boxes
        
        num_macaws += len(boxes)
        print(result)
    
    print(f"Number of macaws detected: {num_macaws}")
    
    return num_macaws

#Function to go trough all the images in a folder
def go_through_images(folder_path):
    
    files = os.listdir(folder_path)

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        detect_macaws(file_path)


def main():
    go_through_images("images_filter")

if __name__ == "__main__":
    main()
