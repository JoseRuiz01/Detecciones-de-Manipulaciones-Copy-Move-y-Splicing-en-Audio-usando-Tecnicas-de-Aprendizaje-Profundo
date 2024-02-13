import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from DataPaths import ORIGINAL_DATASET_PATH, COPY_MOVE_DATASET_PATH, SPLICING_DATASET_PATH, SPECTOGRAM_MATPLOT_EXAMPLE_PATH
from SelectAudios import select_random_audio, search_forgered_audio, select_audios



def generate_spectogram(original_path, copy_move_path, splicing_path, audio_name): 
    fs, original_audio = wavfile.read(original_path)
    fs, splicing_audio = wavfile.read(splicing_path)
    fs, copy_move_audio = wavfile.read(copy_move_path)
    
    # Found the min length of both audios
    min_length = min(len(original_audio), len(splicing_audio), len(copy_move_audio))

    # Cut the audios with the min length
    original_audio_cut = original_audio[:min_length]
    splicing_audio_cut = splicing_audio[:min_length]
    copy_move_audio_cut = copy_move_audio[:min_length]
    
    # Create the time line for the plot
    t = np.arange(0, min_length / fs, 1 / fs)

    # Generate the 3 plots
    fig, ax = plt.subplots(3, 1, figsize=(12, 9))  # Crea 3 subplots
    fig.patch.set_facecolor('white')

    # Original audio spectogram
    ax[0].plot(t, original_audio_cut)
    ax[0].set_title('Audio original en el dominio del tiempo')
    ax[0].set_xlabel('Tiempo [s]')
    ax[0].set_ylabel('Amplitud')
    ax[0].grid(True)

    # Copy-Move audio spectogram
    ax[1].plot(t, copy_move_audio_cut, c='tab:green')  # Color verde
    ax[1].set_title('Audio con copy-move en el dominio del tiempo')
    ax[1].set_xlabel('Tiempo [s]')
    ax[1].set_ylabel('Amplitud')
    ax[1].grid(True)

    # Splicing audio spectogram
    ax[2].plot(t, splicing_audio_cut, c='tab:red')
    ax[2].set_title('Audio con splicing en el dominio del tiempo')
    ax[2].set_xlabel('Tiempo [s]')
    ax[2].set_ylabel('Amplitud')
    ax[2].grid(True)

    plt.tight_layout()

    # Save the image as .png 
    plt.savefig(f'{SPECTOGRAM_MATPLOT_EXAMPLE_PATH}/{audio_name}.png')

    


## MAIN ##
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

generate_spectogram(audio_path, audio1, audio2, audio_name)
