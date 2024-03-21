import pandas as pd

# Leggi il dataset
df = pd.read_csv("bikerides_day.csv")

# Elimina la colonna "label"
df.drop(columns=['Rain'], inplace=True)
df.drop(columns=['Temp'], inplace=True)

# Salva il dataset modificato
df.to_csv("dataset_finale.csv", index=False)
