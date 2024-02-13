import pandas as pd # Leer el archivo CSV como un DataFrame
from DataPaths import DATASET_PATH


df = pd.read_csv(DATASET_PATH)

# Convertir columnas numéricas automáticamente
df[['is_forgered_index', 'forgery_type_index']] = df[['is_forgered_index', 'forgery_type_index']].astype(int)

print(df.info())
print(df.iloc[0:3])
print(df.iloc[10000:10003])
print(df.iloc[20000:20003])
