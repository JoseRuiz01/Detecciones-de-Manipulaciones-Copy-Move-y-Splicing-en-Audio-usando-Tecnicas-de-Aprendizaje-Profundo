import librosa
import librosa.display
import numpy as np
from SpectogramsExamplesGenerator.SelectAudios import select_random_audio, search_forgered_audio, select_audios
import matplotlib.pyplot as plt 
from Constants.DataPaths import ORIGINAL_DATASET_PATH, COPY_MOVE_DATASET_PATH, SPLICING_DATASET_PATH, SPECTOGRAM_LIBROSA_EXAMPLE_PATH


def generate_spectogram(original_path, copy_move_path, splicing_path, audio_name):
    original_audio, sr = librosa.load(original_path)
    splicing_audio, _ = librosa.load(splicing_path)
    copy_move_audio, _ = librosa.load(copy_move_path)
    
    # Change this parameters to improve the quality of the image
    hop_length = 128 # Desplazamiento de la ventana durante la transformación (cuanto menor sea, mayor resolución)
    n_fft = 4096 # antidad de muestras de la señal que se toman para calcular la transformada de Fourier (cuanto mayor sea, mayor resolución)

    # Generate the 3 plots 
    fig, ax = plt.subplots(3, 1, figsize=(8, 6))
    fig.patch.set_facecolor('white')

    # Original audio spectogram
    librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(original_audio, hop_length=hop_length, n_fft=n_fft)), ref=np.max), sr=sr, hop_length=hop_length, x_axis='time', y_axis='log', ax=ax[0])
    ax[0].set_title('Espectrograma del audio original')
    ax[0].set_xlabel('Tiempo [s]')
    ax[0].set_ylabel('Amplitud')

    # Copy-Move audio spectogram
    librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(copy_move_audio, hop_length=hop_length, n_fft=n_fft)), ref=np.max), sr=sr, hop_length=hop_length, x_axis='time', y_axis='log', ax=ax[1])
    ax[1].set_title('Espectrograma del audio con copy-move')
    ax[1].set_xlabel('Tiempo [s]')
    ax[1].set_ylabel('Amplitud')

    # Splicing audio spectogram
    librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(splicing_audio, hop_length=hop_length, n_fft=n_fft)), ref=np.max), sr=sr, hop_length=hop_length, x_axis='time', y_axis='log', ax=ax[2])
    ax[2].set_title('Espectrograma del audio con splicing')
    ax[2].set_xlabel('Tiempo [s]')
    ax[2].set_ylabel('Amplitud')

    plt.tight_layout()

    # Save the image as .png 
    plt.savefig(f'{SPECTOGRAM_LIBROSA_EXAMPLE_PATH}/{audio_name}.png', dpi=2048)




## MAIN ##
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
