import torch
import torchaudio
import pandas as pd
from torch.utils.data import Dataset, DataLoader, random_split
from Constants.DataPaths import LABELS_DATASET_PATH
import numpy as np

class AudiosDataset(Dataset):
    def __init__(self, labels_df, dataset_df):
        """
        Initialize the Audios Dataset class.

        Args:
            labels_df (pandas.DataFrame): DataFrame containing audio labels.
            dataset_df (pandas.DataFrame): DataFrame containing audio files and their corresponding Mel spectrograms.
        """
        self.labels_df = labels_df
        self.dataset_df = dataset_df

    def __len__(self):
        """
        Returns:
            int: Length of the dataset.
        """
        return len(self.labels_df)

    def __getitem__(self, idx):
        """
        Args:
            idx (int): Index of the item.

        Returns:
            tuple: Tuple containing the Mel spectrogram and its corresponding label.
        """
        # Get the audio path and label from the labels DataFrame
        audio_path = self.labels_df.loc[idx, 'audio_path']
        label = self.labels_df.loc[idx, 'forgery_type_index']
        
        # Find the corresponding row in the dataset DataFrame
        dataset_row = self.dataset_df[self.dataset_df['audio_path'] == audio_path].iloc[0]
        
        # Extract the Mel spectrogram
        mel_spectrogram_str = dataset_row['spectogram_of_audio']
        mel_spectrogram = np.array(eval(mel_spectrogram_str))  # Convertir la cadena a un array NumPy
        mel_spectrogram_tensor = torch.tensor(mel_spectrogram)  # Convertir el array NumPy a un tensor de PyTorch
        
        # Apply data augmentation
        aug_mel_spectrogram = self.spectro_augment(mel_spectrogram_tensor)
        
        return aug_mel_spectrogram, label

    @staticmethod
    def spectro_augment(spec, max_mask_pct=0.1, n_freq_masks=1, n_time_masks=1):
        """
        SpecAugment: data augmentation technique for spectrograms. 
        It applies frequency and time masks to the spectrogram to avoid overfitting and help the model generalize better. 
        the model to generalize better. This data augmentation process helps to improve the performance and generalizability of the spectrogram. 
        performance and generalization capability of convolutional neural network models trained on audio data. 
        trained on audio data.

        Args:
            spec (torch.Tensor): Input spectrogram.
            max_mask_pct (float, optional): Maximum percentage of the spectrogram to mask.
            n_freq_masks (int, optional): Number of frequency masks to apply.
            n_time_masks (int, optional): Number of time masks to apply.

        Returns:
            torch.Tensor: Augmented spectrogram.
        """
        aug_spec = spec

        # Apply frequency masking
        freq_mask_param = int(max_mask_pct * aug_spec.size(1))
        for _ in range(n_freq_masks):
            aug_spec = torchaudio.transforms.FrequencyMasking(freq_mask_param)(aug_spec)

        # Apply time masking
        time_mask_param = int(max_mask_pct * aug_spec.size(2))
        for _ in range(n_time_masks):
            aug_spec = torchaudio.transforms.TimeMasking(time_mask_param)(aug_spec)

        return aug_spec


# Obtain the path to the CSV file containing the audio data
DATASET_CSV_PATH = LABELS_DATASET_PATH.replace("labeled_dataset.csv", "audios_with_spectograms.csv")

# Load the labels and audios DataFrame
labels_df = pd.read_csv(LABELS_DATASET_PATH)
dataset_df = pd.read_csv(DATASET_CSV_PATH)

# Create the Sound Dataset instance
sound_dataset = AudiosDataset(labels_df, dataset_df)

# Split the dataset into train and test
train_size = int(0.8 * len(sound_dataset))
test_size = len(sound_dataset) - train_size
train_dataset, test_dataset = random_split(sound_dataset, [train_size, test_size])

# Dataloaders
train_loader = DataLoader(dataset=train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=16, shuffle=False)