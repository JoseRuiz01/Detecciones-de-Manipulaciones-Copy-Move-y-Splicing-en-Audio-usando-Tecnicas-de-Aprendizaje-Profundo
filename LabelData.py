import os
import csv
from DataPaths import ORIGINAL_DATASET_PATH, COPY_MOVE_DATASET_PATH, SPLICING_DATASET_PATH

folder_paths = [ORIGINAL_DATASET_PATH, COPY_MOVE_DATASET_PATH, SPLICING_DATASET_PATH]

# Label lists
forgery_category_label = ["Original_Audio", "Copy_Move_Audio", "Splicing_Audio"]
is_forgered_label = ["Original_Audio", "Forgered_Audio"]

# Header columns of the .csv
headers = ["audio_path", "audio_name", "is_forgered_index", "is_forgered_category", "forgery_type_index", "forgery_type_category"]


# Return the index for the forgeryCategory type and the string associated
def getForgeryType(index):
    forgery_type_index = index
    forgery_type_category = forgery_category_label[forgery_type_index]
    return forgery_type_index, forgery_type_category

# Return the index for the isForgered type and the string associated
def getIsForgered(forgery_type_index):
    is_forgered_index = (0 if forgery_type_index == 0 else 1)
    is_forgered_category = is_forgered_label[is_forgered_index]
    return is_forgered_index, is_forgered_category

# Write the row to the file labeled_dataset.csv
def write(writer, file_path, file_name, is_forgered_index, is_forgered_category, forgery_type_index, forgery_type_category):
    writer.writerow([
        file_path,
        file_name, 
        is_forgered_index, 
        is_forgered_category, 
        forgery_type_index, 
        forgery_type_category
    ])
                    
             
# Load paths of the audios from my dataset
with open('labeled_dataset.csv', 'w', newline='') as csvfile:
    # Write headers in the csv file
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(i for i in headers)
    
    # Travel through all folders of the dataset
    for index, folder in enumerate(folder_paths):        
        for root, dirs, files in os.walk(folder):

            # Travel through all the files in each folder
            for file in files:
                if file.endswith(".WAV"):
                    file_path = os.path.join(root, file)
                    file_name, _ = os.path.splitext(file)
                    
                    forgery_type_index, forgery_type_category = getForgeryType(index)
                    
                    is_forgered_index, is_forgered_category = getIsForgered(forgery_type_index)
                    
                    write(writer, file_path, file_name, is_forgered_index, is_forgered_category, forgery_type_index, forgery_type_category)
                

                