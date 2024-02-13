"""Python document that uses Torch for preprocessing"""

import math
import random
import torch
import torchaudio

from torchaudio import transforms
from IPython.display import Audio



def process_audio(file : str) -> tuple:
    
    sig, sr = torchaudio.load(file)
    return(sig,sr)
    

