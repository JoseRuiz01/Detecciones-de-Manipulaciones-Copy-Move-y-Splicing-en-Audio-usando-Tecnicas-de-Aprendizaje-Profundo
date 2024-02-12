import matplotlib.pyplot as plt
import numpy as np
import random
import os
from scipy.io import wavfile
from DataPaths import ORIGINAL_DATASET_PATH, COPY_MOVE_DATASET_PATH, SPLICING_DATASET_PATH, SPECTOGRAM_MATPLOT_EXAMPLE_PATH


'''
We are going to visualize the spectogram of an audio.
First, we are going to select a .wav file from the OriginalDataset folder, 
and then we are going to take the same .wav from the other two folders and visualize how it changes, 
depending on the forgery method applied. 

'''

#seleccionamos un audio aleatorio dentro de la carpeta original
def select_random_audio(original_path):
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
    archives = os.listdir(original_path)
    
    if not archives:
        return None
    
    #Selecciono un indice aleatorio, y lo cojo de la lista
    random_index = random.randint(0,len(archives)-1)
    random_audio = archives[random_index]
    
    # Construye la ruta completa al archivo de audio
    audio_path = os.path.join(original_path, random_audio)
    
    #nombre sin la extension
    audio_name = os.path.splitext(random_audio)[0]
    
    return random_audio, audio_name, audio_path


#busca el audio modificado en las dos carpetas, recibiendo el audio de la carpeta original
def search_forgered_audio(path, audio_name):
    files_found = []
    
    files = os.listdir(path)
    
    for file in files:
        if file.startswith(audio_name) and "_" in file:
            files_found.append(os.path.join(path, file))
            
    return files_found

    
def select_audios(files_found_splicing, files_found_copy_move):
    #Selecciono un indice aleatorio, y lo cojo de la lista
    
    random_index = random.randint(0,min(len(files_found_splicing)-1,len(files_found_copy_move)-1))
    random_audio_splicing = files_found_splicing[random_index]
    random_audio_cm = files_found_copy_move[random_index]
    
    return random_audio_splicing, random_audio_cm


def generate_spectogram(original_path, copy_move_path, splicing_path): 
    fs, original_audio = wavfile.read(original_path)
    fs, splicing_audio = wavfile.read(splicing_path)
    fs, copy_move_audio = wavfile.read(copy_move_path)
    
    # Encuentra la longitud mínima de los audios
    min_length = min(len(original_audio), len(splicing_audio), len(copy_move_audio))

    # Recorta los audios a la longitud mínima
    original_audio_cut = original_audio[:min_length]
    splicing_audio_cut = splicing_audio[:min_length]
    copy_move_audio_cut = copy_move_audio[:min_length]
    
    # Crea el tiempo para la gráfica
    t = np.arange(0, min_length / fs, 1 / fs)

    # Genera la gráfica del espectrograma
    fig, ax = plt.subplots(3, 1, figsize=(12, 9))  # Crea 3 subplots
    fig.patch.set_facecolor('white')

    # Espectrograma del audio original
    ax[0].plot(t, original_audio_cut)
    ax[0].set_title('Audio original en el dominio del tiempo')
    ax[0].set_xlabel('Tiempo [s]')
    ax[0].set_ylabel('Amplitud')
    ax[0].grid(True)

    # Espectrograma del audio con copy-move
    ax[1].plot(t, copy_move_audio_cut, c='tab:green')  # Color verde
    ax[1].set_title('Audio con copy-move en el dominio del tiempo')
    ax[1].set_xlabel('Tiempo [s]')
    ax[1].set_ylabel('Amplitud')
    ax[1].grid(True)

    # Espectrograma del audio con splicing
    ax[2].plot(t, splicing_audio_cut, c='tab:red')
    ax[2].set_title('Audio con splicing en el dominio del tiempo')
    ax[2].set_xlabel('Tiempo [s]')
    ax[2].set_ylabel('Amplitud')
    ax[2].grid(True)

    plt.tight_layout()

    # Guarda la gráfica como un archivo PNG
    plt.savefig(f'{SPECTOGRAM_MATPLOT_EXAMPLE_PATH}/{audio_name}.png')

    


selected_audio_path, audio_name, audio_path = select_random_audio(ORIGINAL_DATASET_PATH)

if selected_audio_path is not None:
    print(f"Audio seleccionado: {audio_path}")
else:
    print("La carpeta está vacía.")
    


archivos_encontrados_splicing = search_forgered_audio(SPLICING_DATASET_PATH, audio_name)
files_found_copy_move = search_forgered_audio(COPY_MOVE_DATASET_PATH, audio_name)
audio1, audio2 = select_audios(archivos_encontrados_splicing,files_found_copy_move)

print(f"Elemento de la lista 1: {audio1}")
print(f"Elemento de la lista 2: {audio2}")


generate_spectogram(audio_path,audio1,audio2)
