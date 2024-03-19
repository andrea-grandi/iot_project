import pandas as pd
import random

# Leggi il dataset
df = pd.read_csv("dataset_finale.csv")

# Genera valori casuali compresi tra 0 e 100 per la colonna "Pericolosita"
df['Pericolosita'] = [random.uniform(0, 100) for _ in range(len(df))]

# Salva il dataset modificato
df.to_csv("dataset_finale.csv", index=False)
