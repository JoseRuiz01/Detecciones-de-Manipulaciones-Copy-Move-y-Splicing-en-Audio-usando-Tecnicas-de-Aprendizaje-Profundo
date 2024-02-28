import torchaudio import transforms
import pandas as pd
import matplotlib.pyplot as plt
from Constants.DataPaths import DATASET_PATH

dataframe = pd.read_csv(DATASET_PATH,usecols=['audio_path'])

def process_audio(path):
    
    """
    Loads audio from `path`, converts it to mono if necessary, and creates a regular spectrogram.

    Args:
        path (str): Path to the audio file.

    Returns:
        numpy.ndarray: The regular spectrogram of the audio.
    """
    
    audio, sr = torchaudio.load(path)
    
    #Ensures that the audio is mono
    if audio.shape[1] == 2:
        audio = audio.mean(dim=1) #makes it mono
    

    #Creates a regular Spectogram
    spectogram = torchaudio.transforms.Spectrogram()(audio)
    
    
    spectogram_np= spectogram.numpy()
    
    return spectogram_np


def process_audio_to_mel_spectogram(path):
    
    """
    Loads audio from `path`, converts it to mono if necessary, and creates a mel spectrogram.

    Args:
        path (str): Path to the audio file.

    Returns:
        numpy.ndarray: The mel spectrogram of the audio.
    """
    
    audio, sr = torchaudio.load(path)
    
    #Ensures that the audio is mono for better representation
    if audio.shape[1] == 2:
        audio = audio.mean(dim=1) #makes it mono
    

    
    #Creates the Mel spectogram
    melspec = torchaudio.transforms.MelSpectrogram()(audio)
    #Creates mel spectogram using more params
    #melspec = torchaudio.transforms.MelSpectrogram(sample_rate=sr,n_fft=1024,hop_length=None,n_mels=64)(audio)
    
    #Converts to decibels
    top_db = 80

    #db_spec = transforms.AmplitudeToDB(top_db)(melspec)
    
    #Converts to numpy array
    mel_spectogram_np = melspec.numpy()
    
    #Uncomment to return the decibels
    #return (db_spec)
    return mel_spectogram_np

    


regular_spectograms = []
mel_spectograms = []

#For creating the regular spectograms
for audio in dataframe['audio_path']:
    regular_spectogram_np = process_audio(audio)
    regular_spectograms.append(regular_spectogram_np)
    
#For creating the mel spectograms
for audio in dataframe['audio_path']:
    mel_spectogram_np = process_audio_to_mel_spectogram(audio)
    mel_spectograms.append(mel_spectogram_np)


c = input("Decide if you want to create a regular (r) or a mel (m) spectogram ")

while c.lower() not in ['r','m']:
    print("Invalid input, Enter 'r' for regular spectogram, or 'm' for mel spectogram")
    c = input("Decide if you want to create a regular (r) or a mel (m) spectogram ")

if c == 'r':
    dataframe['spectogram_of_audio'] = regular_spectograms
    original_path = DATASET_PATH
    new_path = original_path.replace("labeled_dataset.csv", "")
    dataframe.to_csv(new_path+"audios_with_regular_spectograms.csv")
    
else:
    dataframe['spectogram_of_audio'] = mel_spectograms
    original_path = DATASET_PATH
    new_path = original_path.replace("labeled_dataset.csv", "")
    dataframe.to_csv(new_path+"audios_with_mel_spectograms.csv")
    


