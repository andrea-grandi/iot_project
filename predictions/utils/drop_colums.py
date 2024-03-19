import pandas as pd

# Leggi il dataset
df = pd.read_csv("dataset_test.csv")

# Elimina la colonna "label"
df.drop(columns=['Latitudine'], inplace=True)
df.drop(columns=['Longitudine'], inplace=True)

# Salva il dataset modificato
df.to_csv("dataset_finale.csv", index=False)
