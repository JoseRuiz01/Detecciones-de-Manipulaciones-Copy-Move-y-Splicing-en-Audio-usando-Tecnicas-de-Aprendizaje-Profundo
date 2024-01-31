import os
import csv

# Dataset folders paths 
original_dataset_path = '/home/jose/src/TFG/DatasetConcatenation/OriginalDataset'
copy_move_dataset_path = '/home/jose/src/TFG/DatasetConcatenation/CopyMoveDataset'
splicing_dataset_path = '/home/jose/src/TFG/DatasetConcatenation/SplicingDataset'

folder_paths = [original_dataset_path, copy_move_dataset_path, splicing_dataset_path]

# Label lists
forgery_category_label = ["Original_Audio", "Copy_Move_Audio", "Splicing_Audio"]
is_forgered_label = ["Original_Audio", "Forgered_Audio"]

# Header columns of the .csv
headers = ["audio", "is_forgered_index", "is_forgered_category", "forgery_type_index", "forgery_type_category"]


# Return the index for the forgeryCategory type and the string associated
def getForgeryType(folder):
    forgery_type_index = folder.index
    forgery_type_category = forgery_category_label[forgery_type_index]
    return forgery_type_index, forgery_type_category

# Return the index for the isForgered type and the string associated
def getIsForgered(forgery_type_index):
    is_forgered_index = (0 if forgery_type_index == 0 else 1)
    is_forgered_category = is_forgered_label[is_forgered_index]
    return is_forgered_index, is_forgered_category

# Write the row to the file labeled_dataset.csv
def write(writer, file_name, is_forgered_index, is_forgered_category, forgery_type_index, forgery_type_category):
    writer.writerow(
        file_name, 
        is_forgered_index, 
        is_forgered_category, 
        forgery_type_index, 
        forgery_type_category
    )
                    
             
# Load paths of the audios from my dataset
with open('labeled_dataset.csv', 'w', newline='') as csvfile:
    # Write headers in the csv file
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(i for i in headers)
    
    # Travel through all folders of the dataset
    for folder in folder_paths:
        for root, dirs, files in os.walk(folder):

            # Travel through all the files in each folder
            for file in files:
                if file.endswith(".WAV"):
                    file_name = os.path.join(root, file)
                    
                    forgery_type_index, forgery_type_category = getForgeryType(folder)
                    
                    is_forgered_index, is_forgered_category = getIsForgered(forgery_type_index)
                    
                    write(writer, file_name, is_forgered_index, is_forgered_category, forgery_type_index, forgery_type_category)
                

                