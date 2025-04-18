"""
Primera versión del generador de audios modificados, realizando cortes y asignaciones aleatorias.
FInalmente no se utiliza en el proyecto
"""

import librosa
import soundfile 
import numpy as np
from audio_forgery import *
from load_save import *

# Path to the TIMIT dataset
timit_path = '/TIMIT/data/lisa/data/timit/raw/TIMIT'

#  umbral percentage
umbral_percentage = 1.0

# Create a new folder for the spliced dataset
spliced_dataset_path = 'Dataset/DatasetGenerated/SplicingDataset'
os.makedirs(spliced_dataset_path, exist_ok=True)

# Create a new folder for the copy move dataset
copy_move_dataset_path = 'Dataset/DatasetGenerated/CopyMoveDataset'
os.makedirs(copy_move_dataset_path, exist_ok=True)


# Load TIMIT audio files
timit_files = load_audio_files(timit_path)


# Outer loop
for iteration in range(5):

    # Inner loop
    for original_audio_path in timit_files:

        # Load Original Audio
        original_audio, sr = librosa.load(original_audio_path, sr=None)

        # Define the minimum umbral to check the difference between two audio segments
        max_amplitude = np.max(np.abs(original_audio))
        umbral = umbral_percentage / 100 * max_amplitude

        # Select segments for splicing and copyMove
        while True:
            splice_audio_path = np.random.choice(timit_files)
            splice_segment, _ = select_random_segment(splice_audio_path)
            if len(splice_segment) < len(original_audio) & checkRMSDifference(splice_segment, original_audio, umbral): break

        copy_move_segment, _ = select_random_segment(original_audio_path)

        # Apply forgery
        spliced_audio = apply_forgery(original_audio, splice_segment)
        copy_move_audio = apply_forgery(original_audio, copy_move_segment)

        # Save the audio
        spliced_audio_path = save_files(original_audio_path, iteration, spliced_dataset_path)
        soundfile.write(spliced_audio_path, spliced_audio, sr)
        
        copy_move_audio_path = save_files(original_audio_path, iteration, copy_move_dataset_path)
        soundfile.write(copy_move_audio_path, copy_move_audio, sr)