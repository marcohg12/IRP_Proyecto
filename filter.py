# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del filtrador del sistema
# ---------------------------------------------------------------------------------------------------

import cv2
import numpy as np

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

    #print(coordinates)
    x, y, w, h = coordinates
    cropped_image = image[y:y+h, x:x+w]
    return cropped_image

# def main():
#     image = cv2.imread('images/zz7.jpg')
#     coordinates = detect_macaw_coordinates(image)
#     cropped_image = crop_image(image, coordinates[0])
#     cv2.imshow('Cropped Image', cropped_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     main()
