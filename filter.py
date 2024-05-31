# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del filtrador del sistema
# ---------------------------------------------------------------------------------------------------
import cv2
import numpy as np
import os

#Función 1: determinar las coordenadas de una posible lapa, un 5% 
# retorna una lista con las coordenadas de las lapas detectadas
def detect_macaw_coordinates(image, threshold=0.05):
    # Convertir la imagen a HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Definir los rangos de color rojo en HSV
    red_lower1 = np.array([0, 50, 50])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([160, 50, 50])
    red_upper2 = np.array([180, 255, 255])
    
    # Crear máscaras para los rangos de color rojo
    mask1 = cv2.inRange(hsv_image, red_lower1, red_upper1)
    mask2 = cv2.inRange(hsv_image, red_lower2, red_upper2)
    red_mask = cv2.bitwise_or(mask1, mask2)
    
    height, width = red_mask.shape
    
    y_coords = []
    x_coords = []
    
    # escanea el eje y (filas)
    for y in range(height):
        row = red_mask[y, :]
        red_pixels = np.count_nonzero(row)
        if red_pixels >= threshold * width:
            y_coords.append(y)
    
    # escanea el eje x (columnas)
    for x in range(width):
        col = red_mask[:, x]
        red_pixels = np.count_nonzero(col)
        if red_pixels >= threshold * height:
            x_coords.append(x)
    
    # si se detectaron coordenadas, se calculan los límites de la lapa
    if y_coords and x_coords:
        y_min = min(y_coords)
        y_max = max(y_coords)
        x_min = min(x_coords)
        x_max = max(x_coords)
        macaw_coords = [(x_min, y_min, x_max - x_min, y_max - y_min)]
    else:
        macaw_coords = []
    
    return macaw_coords


#Función 2: recortar la imagen con las coordenadas obtenidas de la función 1
def crop_image(image, coordinates):
    x, y, w, h = coordinates
    cropped_image = image[y:y+h, x:x+w]
    return cropped_image

def main():
    input_folder = 'images_preprocess'
    output_folder = 'images_filter'
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterar sobre las imágenes preprocesadas
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg')):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            
            macaw_coords = detect_macaw_coordinates(image)

            for idx, coords in enumerate(macaw_coords):
                cropped_image = crop_image(image, coords)
                output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_crop.jpg")
                cv2.imwrite(output_path, cropped_image)

if __name__ == "__main__":
    main()
