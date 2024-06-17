# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del generador de reporte del sistema
# ---------------------------------------------------------------------------------------------------

import uuid
import shutil
import os

SESSION_FILENAME = None
TIME_STAMP = None
LAST_NUMBER_OF_MACAWS_SEEN = 0
from enum import Enum
from datetime import datetime
from classifier import clean_up_model

class Veredict_Type(Enum):

    INCREMENT = 1
    DECREMENT = 2
    START = 3
    END = 4

# Restaura los valores por defecto de las variables globales
def clean_up():

    global SESSION_FILENAME
    SESSION_FILENAME = None

    global TIME_STAMP
    TIME_STAMP = None

    global LAST_NUMBER_OF_MACAWS_SEEN
    LAST_NUMBER_OF_MACAWS_SEEN = 0

    clean_up_model()

# Descarga el último reporte realizado
def download_report():

    global SESSION_FILENAME

    if (not SESSION_FILENAME):
        return False
    
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    
    source_path = os.path.join("reports", SESSION_FILENAME)
    destination_path = os.path.join(downloads_dir, SESSION_FILENAME)
    
    if os.path.exists(source_path):

        shutil.copy(source_path, destination_path)
        os.remove(source_path)
        return True
    
    return False

# Recibe una marca de tiempo y la guarda en una variable global
def process_time_stamp(time_stamp):
    
    global TIME_STAMP
    TIME_STAMP = time_stamp

# Recibe la cantidad de lapas detectadas
# Genera un veredicto con base en el último procesamiento y guarda el veredicto
# en el archivo de la sesión
def report_director(num_macaws):

    global LAST_NUMBER_OF_MACAWS_SEEN
    global TIME_STAMP
    global SESSION_FILENAME

    minutes = TIME_STAMP[0]
    seconds = TIME_STAMP[1]
    time_str = f"En el minuto {minutes} segundo {seconds}"
    changes = False
    veredict = ""
    details = ""
    veredict_type = None

    # Hay un inicio de avistamiento
    if (LAST_NUMBER_OF_MACAWS_SEEN == 0 and num_macaws > 0):

        veredict = "--------------------------------------- INICIO DE AVISTAMIENTO ---------------------------------------"
        details = f"Cantidad de lapas observadas: {num_macaws}"
        veredict_type = Veredict_Type.START
        changes = True

    # Hay un fin de avistamiento
    elif (LAST_NUMBER_OF_MACAWS_SEEN > 0 and num_macaws == 0):

        veredict = "FIN DE AVISTAMIENTO"
        veredict_type = Veredict_Type.END
        changes = True

    # Hay un decremento en los ejemplares dentro del avistamiento
    elif (LAST_NUMBER_OF_MACAWS_SEEN > 0 and LAST_NUMBER_OF_MACAWS_SEEN > num_macaws):

        veredict = "DECREMENTO EN LA CANTIDAD DE EJEMPLARES OBSERVADOS"
        details = f"Cantidad de lapas actualmente: {num_macaws}. Cantidad anterior: {LAST_NUMBER_OF_MACAWS_SEEN}"
        veredict_type = Veredict_Type.DECREMENT
        changes = True

    # Hay un incremento de los ejemplares dentro del avistamiento
    elif (LAST_NUMBER_OF_MACAWS_SEEN > 0 and LAST_NUMBER_OF_MACAWS_SEEN < num_macaws):

        veredict = "INCREMENTO EN LA CANTIDAD DE EJEMPLARES OBSERVADOS"
        details = f"Cantidad de lapas actualmente: {num_macaws}. Cantidad anterior: {LAST_NUMBER_OF_MACAWS_SEEN}"
        veredict_type = Veredict_Type.INCREMENT
        changes = True
    
    # Si hay un cambio se registra en el archivo
    if (changes):

        write_in_file(veredict, details, time_str, veredict_type)

    LAST_NUMBER_OF_MACAWS_SEEN = num_macaws

# Recibe el veredicto, detalles, marca de tiempo en string y el tipo de veredicto
# Formatea los strings y los escribe en el archivo de la sesión
def write_in_file(veredict, details, time_str, veredict_type):

    global SESSION_FILENAME

    # Si no hay archivo de sesión, genera el archivo y coloca el encabezado
    if (not SESSION_FILENAME):

        SESSION_FILENAME = str(uuid.uuid4()) + ".txt"
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("reports/" + SESSION_FILENAME, 'a') as file:
            
            file.write("--------------------------------------- REPORTE DE AVISTAMIENTO --------------------------------------\n")
            file.write("Fecha: " + str(current_datetime) + "\n\n")
    
    # Genera el reporte
    with open("reports/" + SESSION_FILENAME, 'a') as file:

        if (veredict_type == Veredict_Type.END):
            file.write(veredict + ". " + time_str + "\n")
        else:
            file.write(veredict + "\n")

        if (details != ""):

            file.write(details + ". " + time_str + "\n\n")
        elif (veredict_type != Veredict_Type.END):

            file.write(time_str + "\n")

        if (veredict_type == Veredict_Type.END):
            file.write("------------------------------------------------------------------------------------------------------")
            file.write("\n\n\n")