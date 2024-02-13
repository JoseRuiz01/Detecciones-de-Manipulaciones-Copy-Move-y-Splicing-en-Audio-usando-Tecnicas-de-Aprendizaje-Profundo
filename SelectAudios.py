import random
import os

# Select a random audio from the original dataset
def select_random_audio(original_path):
    archives = os.listdir(original_path)
    
    if not archives:
        return None
    
    # Select a random audio from the original folder
    random_index = random.randint(0,len(archives)-1)
    random_audio = archives[random_index]
    
    # Build the path to the selected audio
    audio_path = os.path.join(original_path, random_audio)
    
    # Name without the extension
    audio_name = os.path.splitext(random_audio)[0]
    
    return random_audio, audio_name, audio_path


# Search the forgered audios based on the original audio name
def search_forgered_audio(path, audio_name):
    files_found = []
    files = os.listdir(path)
    
    for file in files:
        if file.startswith(audio_name) and "_" in file:
            files_found.append(os.path.join(path, file))
            
    return files_found

    
def select_audios(files_found_splicing, files_found_copy_move):
    # Select random index 
    random_index = random.randint(0,min(len(files_found_splicing)-1,len(files_found_copy_move)-1))
    
    # Take the random audios from the list of forgered audios matching the original audio
    random_audio_splicing = files_found_splicing[random_index]
    random_audio_cm = files_found_copy_move[random_index]
    
    return random_audio_splicing, random_audio_cm
