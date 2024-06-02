# ---------------------------------------------------------------------------------------------------
# Este archivo contiene un ejemplo del uso del sistema
# ---------------------------------------------------------------------------------------------------

from capturer import process_video, process_image
import datetime
import cv2
import os

def test_system():

    #video_path = "videos/video_1.mp4"

    #process_video(video_path)
    image_files = [f for f in os.listdir('images') if os.path.isfile(os.path.join('images', f))]

    for file_name in image_files:
        file_path = os.path.join('images', file_name)
        # Read the image
        image = cv2.imread(file_path)
        if image is not None:
            # Send the image to the processing function along with the timestamp
            process_image(image, (0, 0))

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
        if exp == 0:
            line_correct_percentages.append(100 if res == 0 else 0)  # Manejo de división por cero
        else:
            line_correct_percentages.append((res / exp) * 100)

    # Calcular el porcentaje de aceptación global y el porcentaje de error global
    total_lines = len(line_correct_percentages)
    total_correct_percentage = sum(line_correct_percentages)
    
    acceptance_percentage = total_correct_percentage / total_lines
    error_percentage = 100 - acceptance_percentage

    return acceptance_percentage, error_percentage

#test_system()
acceptance_percentage, error_percentage = calculate_acceptance_error_percentage('expected_results2.txt', 'results2.txt')
print("Acceptance Percentage:", acceptance_percentage)
print("Error Percentage:", error_percentage)

