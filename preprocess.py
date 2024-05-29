# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo de preprocesamiento del sistema
# ---------------------------------------------------------------------------------------------------
import cv2
import numpy as np
import os

def process_image(path):
    image = cv2.imread(path)
    return image

def noise_removal(image):
    gaussian_blur = cv2.GaussianBlur(image, (3, 3), 0)
    bilateral_blur = cv2.bilateralFilter(image, 9, 40, 40)
    return bilateral_blur

def improve_sharpness(image):
    kernel = np.array([[0, -0.5, 0], 
                   [-0.5, 3, -0.5], 
                   [0, -0.5, 0]])
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened

def improve_lighting(image):
    improved_lighting = cv2.convertScaleAbs(image, alpha=1.2, beta=20)
    return improved_lighting
    
def intensify_color_aux(hsv_image, lower_bound, upper_bound, increase_value):
    # Crear máscara para el rango de color
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    
    # Aplicar la máscara a la imagen HSV
    hsv_intensified = hsv_image.copy()
    hsv_intensified[:, :, 1] = cv2.add(hsv_intensified[:, :, 1], (mask * increase_value // 255).astype(np.uint8))
    
    return hsv_intensified

def intesify_color(image):
    # Convertir la imagen a HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Definir los rangos de color en HSV
    red_lower1 = np.array([0, 50, 50])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([160, 50, 50])
    red_upper2 = np.array([180, 255, 255])
    yellow_lower = np.array([20, 50, 50])
    yellow_upper = np.array([30, 255, 255])
    blue_lower = np.array([110, 50, 50])
    blue_upper = np.array([130, 255, 255])

    # Intensificar los colores específicos
    increase_value = 180 # Ajusta este valor según sea necesario
    hsv_intensified = intensify_color_aux(hsv_image, red_lower1, red_upper1, increase_value)
    hsv_intensified = intensify_color_aux(hsv_intensified, red_lower2, red_upper2, increase_value)
    hsv_intensified = intensify_color_aux(hsv_intensified, yellow_lower, yellow_upper, increase_value)
    hsv_intensified = intensify_color_aux(hsv_intensified, blue_lower, blue_upper, increase_value)

    # Convertir la imagen HSV intensificada de nuevo a BGR
    intensified_image = cv2.cvtColor(hsv_intensified, cv2.COLOR_HSV2BGR)
    
    return intensified_image

def main():
    input_folder = 'images'
    output_folder = 'images_preprocess'
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg')):
            image = process_image(os.path.join(input_folder, filename))
            image = noise_removal(image)
            image = improve_sharpness(image)
            image = improve_lighting(image)
            image = intesify_color(image)
            
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, image)

main()

