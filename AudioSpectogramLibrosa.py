import librosa
import librosa.display
import numpy as np
import random
import os
import matplotlib.pyplot as plt 
from scipy.io import wavfile
from DataPaths import ORIGINAL_DATASET_PATH, COPY_MOVE_DATASET_PATH, SPLICING_DATASET_PATH, SPECTOGRAM_LIBROSA_EXAMPLE_PATH

def select_random_audio(original_path):
    """
    Selecciona un audio aleatorio de la carpeta especificada y devuelve su ruta y nombre.
    """
    archives = os.listdir(original_path)
    
    if not archives:
        return None
    
    random_index = random.randint(0, len(archives)-1)
    random_audio = archives[random_index]
    
    audio_path = os.path.join(original_path, random_audio)
    audio_name = os.path.splitext(random_audio)[0]
    
    return random_audio, audio_name, audio_path


def search_forgered_audio(path, audio_name):
    files_found = []
    files = os.listdir(path)
    
    for file in files:
        if file.startswith(audio_name) and "_" in file:
            files_found.append(os.path.join(path, file))
            
    return files_found


def select_audios(files_found_splicing, files_found_copy_move):
    random_index = random.randint(0, min(len(files_found_splicing)-1, len(files_found_copy_move)-1))
    random_audio_splicing = files_found_splicing[random_index]
    random_audio_cm = files_found_copy_move[random_index]
    
    return random_audio_splicing, random_audio_cm


def generate_spectogram(original_path, copy_move_path, splicing_path, audio_name):
    original_audio, sr = librosa.load(original_path)
    splicing_audio, _ = librosa.load(splicing_path)
    copy_move_audio, _ = librosa.load(copy_move_path)
    
    # Genera la gráfica del espectrograma
    fig, ax = plt.subplots(3, 1, figsize=(10, 6))
    fig.patch.set_facecolor('white')

    # Espectrograma del audio original
    librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(original_audio)), ref=np.max), sr=sr, x_axis='time', y_axis='log', ax=ax[0])
    ax[0].set_title('Espectrograma del audio original')
    ax[0].set_xlabel('Tiempo [s]')
    ax[0].set_ylabel('Amplitud')

    # Espectrograma del audio con copy-move
    librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(copy_move_audio)), ref=np.max), sr=sr, x_axis='time', y_axis='log', ax=ax[1])
    ax[1].set_title('Espectrograma del audio con copy-move')
    ax[1].set_xlabel('Tiempo [s]')
    ax[1].set_ylabel('Amplitud')

    # Espectrograma del audio con splicing
    librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(splicing_audio)), ref=np.max), sr=sr, x_axis='time', y_axis='log', ax=ax[2])
    ax[2].set_title('Espectrograma del audio con splicing')
    ax[2].set_xlabel('Tiempo [s]')
    ax[2].set_ylabel('Amplitud')

    plt.tight_layout()

    # Guarda la gráfica como un archivo PNG
    plt.savefig(f'{SPECTOGRAM_LIBROSA_EXAMPLE_PATH}/{audio_name}.png')


selected_audio_path, audio_name, audio_path = select_random_audio(ORIGINAL_DATASET_PATH)

if selected_audio_path is not None:
    print(f"Audio seleccionado: {audio_path}")
else:
    print("La carpeta está vacía.")

files_found_splicing = search_forgered_audio(SPLICING_DATASET_PATH, audio_name)
files_found_copy_move = search_forgered_audio(COPY_MOVE_DATASET_PATH, audio_name)
audio1, audio2 = select_audios(files_found_splicing, files_found_copy_move)

print(f"Elemento de la lista 1: {audio1}")
print(f"Elemento de la lista 2: {audio2}")

generate_spectogram(audio_path, audio1, audio2, audio_name)
