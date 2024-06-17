# --------------------------------------------------------------------------------------------------------------
# Este archivo contiene la interfaz del programa
# --------------------------------------------------------------------------------------------------------------

from tkinter import *
import customtkinter
from capturer import process_image, process_video
from report import clean_up, download_report
import os
import time
import cv2
import threading

FILE_PATH = None
MODEL = "YOLO"

# --------------------------------------------------------------------------------------------------------------

def check_file_type(file_path):

    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
        return 'image'
    
    elif file_extension.lower() in ['.mp4']:
        return 'video'

def process():

    global FILE_PATH
    global MODEL
    start_time = 0
    end_time = 0

    file_type = check_file_type(FILE_PATH)

    processing_label.configure(text = "Procesando el archivo...")
    root.update()

    if (file_type == "video"):

        start_time = time.time()
        process_video(str(FILE_PATH), MODEL)
        end_time = time.time()

    else:
        
        start_time = time.time()
        img = cv2.imread(str(FILE_PATH))
        process_image(img, MODEL)
        end_time = time.time()

    download_label.place(relx = 0.5, rely = 0.7, anchor = CENTER)

    if(download_report()):
        download_label.configure(text = "El reporte generado se encuentra en la carpeta de descargas")
    else:
        download_label.configure(text = "No se reconoció ninguna lapa en el archivo, no se generó un reporte")

    clean_up()

    progress_bar.stop()
    progress_bar.place_forget()
    
    execution_time = round(end_time - start_time, 2)
    processing_label.configure(text = f"El archivo fue procesado exitosamente en {execution_time} segundos")

# --------------------------------------------------------------------------------------------------------------

def process_callback():

    thread = threading.Thread(target = process)
    thread.daemon = True
    thread.start()

    download_label.place_forget()
    progress_bar.place(relx = 0.5, rely = 0.7, anchor = CENTER)
    progress_bar.start()
    process_button.configure(state = "disabled")

def select_file_callback():

    global FILE_PATH

    file_path = customtkinter.filedialog.askopenfilename(initialdir = "/", title = "Seleccione el archivo", filetypes = (("Imagen", "*.png;*.jpg;*.jpeg"), ("Video", "*.mp4")))
    
    if file_path:
        FILE_PATH = file_path
        process_button.configure(state = "normal")

def select_model_callback(choice):

    global MODEL
    MODEL = choice

# --------------------------------------------------------------------------------------------------------------

root = customtkinter.CTk()
root.geometry("500x500")
root.title("RL")
root.resizable(False, False)

title = customtkinter.CTkLabel(master = root, text = "Reconocedor de Lapas", fg_color = "transparent", font = ("Helvetica", 36, "bold"))
title.place(relx = 0.5, rely = 0.1, anchor = CENTER)

select_model_label = customtkinter.CTkLabel(master = root, text = "Seleccione el modelo", fg_color = "transparent")
select_model_label.place(relx = 0.35, rely = 0.3, anchor = CENTER)

select_model = customtkinter.CTkComboBox(master = root, values = ["YOLO", "DETECTO"], state = 'readonly', command = select_model_callback)
select_model.place(relx = 0.65, rely = 0.3, anchor = CENTER)
select_model.set("YOLO")

select_file_callback_label = customtkinter.CTkLabel(master = root, text = "Seleccione el archivo", fg_color = "transparent")
select_file_callback_label.place(relx = 0.35, rely = 0.4, anchor = CENTER)

select_file_callback_button = customtkinter.CTkButton(master = root, text = "Seleccionar", command = select_file_callback)
select_file_callback_button.place(relx = 0.65, rely = 0.4, anchor = CENTER)

processing_label = customtkinter.CTkLabel(master = root, text = "", fg_color = "transparent")
processing_label.place(relx = 0.5, rely = 0.6, anchor = CENTER)

download_label = customtkinter.CTkLabel(master = root, text = "", fg_color = "transparent")
download_label.place(relx = 0.5, rely = 0.7, anchor = CENTER)

progress_bar = customtkinter.CTkProgressBar(master = root, mode = "indeterminate", orientation = "horizontal")

process_button = customtkinter.CTkButton(master = root, text = "Procesar", command = process_callback)
process_button.place(relx = 0.5, rely = 0.9, anchor = CENTER)
process_button.configure(state = "disabled")

root.mainloop()
