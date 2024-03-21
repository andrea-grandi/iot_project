import pandas as pd
import numpy as np

# Numero di righe nel dataset
num_rows = 10000

# Genera dati casuali per latitudine e longitudine
latitudes = np.random.uniform(44.6331, 44.7054, num_rows)  # Latitudine di Modena
longitudes = np.random.uniform(10.9135, 10.9848, num_rows)  # Longitudine di Modena

# Inizializzo la pericolosità 
pericolo = [0, 1, 2, 3, 4]

# randomizzo 
pericolosità = np.random.choice(pericolo, num_rows)

# inizializzo il tipo 
tipo = 'Sicura' 

# Crea il DataFrame
data = {'Latitudine': latitudes, 'Longitudine': longitudes, 'Pericolosità' : pericolosità, 'Tipo': tipo}
df = pd.DataFrame(data)

# Assegna 'sicura' alle posizioni non pericolose
df.loc[df['Pericolosità'] == 1, 'Tipo'] = 'Zona rumorosa'
# Assegna 'sicura' alle posizioni non pericolose
df.loc[df['Pericolosità'] == 2, 'Tipo'] = 'Zona molto trafficata'
# Assegna 'sicura' alle posizioni non pericolose
df.loc[df['Pericolosità'] == 3, 'Tipo'] = 'Zona poco luminosa'
# Assegna 'sicura' alle posizioni non pericolose
df.loc[df['Pericolosità'] == 4, 'Tipo'] = 'Pericolo caduta oggetti'


# Salva il DataFrame in un file CSV
df.to_csv('train/train_positions_dataset_modena.csv', index=False)
