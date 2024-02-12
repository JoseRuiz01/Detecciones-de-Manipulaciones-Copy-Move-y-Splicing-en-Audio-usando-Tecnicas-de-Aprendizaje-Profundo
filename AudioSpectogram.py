import matplotlib.pyplot as plt
import numpy as np
import random
import os
from scipy.io import wavfile
from DataPaths import ORIGINAL_DATASET_PATH, COPY_MOVE_DATASET_PATH, SPLICING_DATASET_PATH, SPECTOGRAM_EXAMPLE_PATH


'''
We are going to visualize the spectogram of an audio.
First, we are going to select a .wav file from the OriginalDataset folder, 
and then we are going to take the same .wav from the other two folders and visualize how it changes, 
depending on the forgery method applied. 

'''

#seleccionamos un audio aleatorio dentro de la carpeta original
def select_random_audio(path_original):
    """
    Selecciona un audio aleatorio de la carpeta especificada y devuelve su ruta y nombre.

    Args:
        path_original (str): Ruta a la carpeta que contiene los archivos de audio.

    Returns:
        tuple: Una tupla con dos elementos:
            - ruta_audio (str): La ruta completa al archivo de audio seleccionado.
            - nombre_audio (str): El nombre del archivo de audio sin la extensión.

    None: Si la carpeta está vacía.
    """
    archives = os.listdir(path_original)
    
    if not archives:
        return None
    #Selecciono un indice aleatorio, y lo cojo de la lista
    random_index = random.randint(0,len(archives)-1)
    random_audio = archives[random_index]
    
    # Construye la ruta completa al archivo de audio
    ruta_audio = os.path.join(path_original, random_audio)
    
    #nombre sin la extension
    audio_name = os.path.splitext(random_audio)[0]
    
    return random_audio, audio_name, ruta_audio


#busca el audio modificado en las dos carpetas, recibiendo el audio de la carpeta original
def buscar_audio_modificado(path, nombre_audio):
    archivos_encontrados = []
    
    archivos = os.listdir(path)
    
    for archivo in archivos:
        if archivo.startswith(nombre_audio) and "_" in archivo:
            archivos_encontrados.append(os.path.join(path,archivo))
            
    return archivos_encontrados

    
def selecciona_audios(archivos_encontrados_splicing,archivos_encontrados_copy_move):
    #Selecciono un indice aleatorio, y lo cojo de la lista
    
    random_index = random.randint(0,min(len(archivos_encontrados_splicing)-1,len(archivos_encontrados_copy_move)-1))
    random_audio_splicing = archivos_encontrados_splicing[random_index]
    random_audio_cm = archivos_encontrados_copy_move[random_index]
    
    return random_audio_splicing, random_audio_cm


def generate_spectogram(ruta_original,ruta_copy_move,ruta_splicing): 
    fs,audio_original = wavfile.read(ruta_original)
    fs,audio_con_splicing = wavfile.read(ruta_splicing)
    fs,audio_con_cm = wavfile.read(ruta_copy_move)
    
    
    # Encuentra la longitud mínima de los audios
    longitud_minima = min(len(audio_original), len(audio_con_splicing), len(audio_con_cm))

    # Recorta los audios a la longitud mínima
    audio_original_recortado = audio_original[:longitud_minima]
    audio_con_splicing_recortado = audio_con_splicing[:longitud_minima]
    audio_con_cm_recortado = audio_con_cm[:longitud_minima]
    
    # Crea el tiempo para la gráfica
    t = np.arange(0, longitud_minima / fs, 1 / fs)

    # Genera la gráfica del espectrograma
    fig, ax = plt.subplots(3, 1, figsize=(12, 9))  # Crea 3 subplots
    fig.patch.set_facecolor('white')

    # Espectrograma del audio original
    ax[0].plot(t, audio_original_recortado)
    ax[0].set_title('Audio original en el dominio del tiempo')
    ax[0].set_xlabel('Tiempo [s]')
    ax[0].set_ylabel('Amplitud')
    ax[0].grid(True)

    # Espectrograma del audio con copy-move
    ax[1].plot(t, audio_con_cm_recortado, c='tab:green')  # Color verde
    ax[1].set_title('Audio con copy-move en el dominio del tiempo')
    ax[1].set_xlabel('Tiempo [s]')
    ax[1].set_ylabel('Amplitud')
    ax[1].grid(True)

    # Espectrograma del audio con splicing
    ax[2].plot(t, audio_con_splicing_recortado, c='tab:red')
    ax[2].set_title('Audio con splicing en el dominio del tiempo')
    ax[2].set_xlabel('Tiempo [s]')
    ax[2].set_ylabel('Amplitud')
    ax[2].grid(True)

    plt.tight_layout()

    # Guarda la gráfica como un archivo PNG
    plt.savefig(f'{SPECTOGRAM_EXAMPLE_PATH}/{nombre_audio}.png')

    

ruta_audio_seleccionado, nombre_audio, ruta_audio = select_random_audio(ORIGINAL_DATASET_PATH)

if ruta_audio_seleccionado is not None:
    print(f"Audio seleccionado: {ruta_audio}")
else:
    print("La carpeta está vacía.")
    


archivos_encontrados_splicing = buscar_audio_modificado(SPLICING_DATASET_PATH, nombre_audio)

archivos_encontrados_copy_move = buscar_audio_modificado(COPY_MOVE_DATASET_PATH, nombre_audio)

audio1, audio2 = selecciona_audios(archivos_encontrados_splicing,archivos_encontrados_copy_move)

print(f"Elemento de la lista 1: {audio1}")
print(f"Elemento de la lista 2: {audio2}")


generate_spectogram(ruta_audio,audio1,audio2)
