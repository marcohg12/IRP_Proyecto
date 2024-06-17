# ---------------------------------------------------------------------------------------------------
# Este archivo contiene funciones para probar los porcentajes de error y aceptación
# del sistema
# ---------------------------------------------------------------------------------------------------

import os
import cv2
from capturer import process_image

def calculate_acceptance_error_percentage(expected_file, results_file):

    # Función interna para analizar los números de las líneas
    def parse_numbers(lines):
        return [int(line.strip().split()[-1]) for line in lines]

    # Función interna para leer y analizar el contenido de un archivo
    def read_and_parse_file(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        return parse_numbers(lines)

    # Leer y analizar los números esperados y obtenidos de los archivos
    expected_numbers = read_and_parse_file(expected_file)
    results_numbers = read_and_parse_file(results_file)

    # Lista para almacenar los porcentajes correctos obtenidos por línea
    line_correct_percentages = []

    # Calcular el porcentaje correcto obtenido por línea
    for exp, res in zip(expected_numbers, results_numbers):
        if exp == res:
            line_correct_percentages.append(1)
        else:
            line_correct_percentages.append(0)

    # Calcular el porcentaje de aceptación global y el porcentaje de error global
    total_lines = len(line_correct_percentages)
    total_correct_percentage = sum(line_correct_percentages)
    
    acceptance_percentage = (total_correct_percentage / total_lines) * 100
    error_percentage = 100 - acceptance_percentage

    return acceptance_percentage, error_percentage

def test_system():

    image_files = [f for f in os.listdir('images') if os.path.isfile(os.path.join('images', f))]

    for file_name in image_files:

        file_path = os.path.join('images', file_name)

        image = cv2.imread(file_path)

        if image is not None:

            if image.shape[0] != 0 or image.shape[1] != 0:

                process_image(image, "YOLO", (0, 0))

test_system()
acceptance_percentage, error_percentage = calculate_acceptance_error_percentage('test_data/expected_results2.txt', 'test_data/results2.txt')
print("Acceptance Percentage:", acceptance_percentage)
print("Error Percentage:", error_percentage)