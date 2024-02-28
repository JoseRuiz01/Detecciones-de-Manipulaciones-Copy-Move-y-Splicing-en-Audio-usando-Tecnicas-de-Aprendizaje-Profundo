import pandas as pd

from Constants.DataPaths import LABELS_DATASET_PATH


def csv_to_dataframe(csv_path):
    """
    Reads a csv file and stores it in a dataframe
    
    Args: 
        csv_path: path of the .csv file
        
    Returns:
        A Pandas dataframe with the csv data
    """

    dataframe = pd.read_csv(csv_path)
    dataframe[['is_forgered_index', 'forgery_type_index']] = dataframe[['is_forgered_index', 'forgery_type_index']].astype(int)

    return dataframe

csv_path = LABELS_DATASET_PATH
result_dataframe = csv_to_dataframe(csv_path=csv_path)

# Count the number of labels in the 'original_audio' column
labels_count = result_dataframe['is_forgered_category'].value_counts()

# Print the result
print(labels_count)
print(result_dataframe.info())
print(result_dataframe.iloc[0:3])
print(result_dataframe.iloc[10000:10003])
print(result_dataframe.iloc[20000:20003])