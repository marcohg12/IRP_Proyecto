# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del generador de reporte del sistema
# ---------------------------------------------------------------------------------------------------

import uuid

SESSION_FILENAME = None
TIME_STAMP = None
LAST_NUMBER_OF_MACAWS_SEEN = 0
from enum import Enum
from datetime import datetime

class Veredict_Type(Enum):

    INCREMENT = 1
    DECREMENT = 2
    START = 3
    END = 4

def clean_up():

    global SESSION_FILENAME
    SESSION_FILENAME = None

    global TIME_STAMP
    TIME_STAMP = None

    global LAST_NUMBER_OF_MACAWS_SEEN
    LAST_NUMBER_OF_MACAWS_SEEN = 0


def process_time_stamp(time_stamp):
    
    global TIME_STAMP
    TIME_STAMP = time_stamp

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

    if (LAST_NUMBER_OF_MACAWS_SEEN == 0 and num_macaws > 0):

        veredict = "--------------------------------------- INICIO DE AVISTAMIENTO ---------------------------------------"
        details = f"Cantidad de lapas observadas: {num_macaws}"
        veredict_type = Veredict_Type.START
        changes = True

    elif (LAST_NUMBER_OF_MACAWS_SEEN > 0 and num_macaws == 0):

        veredict = "FIN DE AVISTAMIENTO"
        veredict_type = Veredict_Type.END
        changes = True

    elif (LAST_NUMBER_OF_MACAWS_SEEN > 0 and LAST_NUMBER_OF_MACAWS_SEEN > num_macaws):

        veredict = "DECREMENTO EN LA CANTIDAD DE EJEMPLARES OBSERVADOS"
        details = f"Cantidad de lapas actualmente: {num_macaws}. Cantidad anterior: {LAST_NUMBER_OF_MACAWS_SEEN}"
        veredict_type = Veredict_Type.DECREMENT
        changes = True

    elif (LAST_NUMBER_OF_MACAWS_SEEN > 0 and LAST_NUMBER_OF_MACAWS_SEEN < num_macaws):

        veredict = "INCREMENTO EN LA CANTIDAD DE EJEMPLARES OBSERVADOS"
        details = f"Cantidad de lapas actualmente: {num_macaws}. Cantidad anterior: {LAST_NUMBER_OF_MACAWS_SEEN}"
        veredict_type = Veredict_Type.INCREMENT
        changes = True
    
    if (changes):

        write_in_file(veredict, details, time_str, veredict_type)

    LAST_NUMBER_OF_MACAWS_SEEN = num_macaws


def write_in_file(veredict, details, time_str, veredict_type):

    global SESSION_FILENAME

    if (not SESSION_FILENAME):

        SESSION_FILENAME = str(uuid.uuid4()) + ".txt"
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("reports/" + SESSION_FILENAME, 'a') as file:
            
            file.write("--------------------------------------- REPORTE DE AVISTAMIENTO --------------------------------------\n")
            file.write("Fecha: " + str(current_datetime) + "\n\n")
    
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