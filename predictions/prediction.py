import pandas as pd
from prophet import Prophet
import plotly.express as px

# Carica il dataset
data = pd.read_csv("dataset_test.csv")

# Aggiungi una colonna per le date utilizzando la colonna "Data"
data['ds'] = pd.to_datetime(data['Data'])

# Addestra il modello per la predizione della latitudine
model_lat = Prophet()
model_lat.fit(data[["ds", "Latitudine"]].rename(columns={"Latitudine": "y", "ds": "ds"}))

# Addestra il modello per la predizione della longitudine
model_lon = Prophet()
model_lon.fit(data[["ds", "Longitudine"]].rename(columns={"Longitudine": "y", "ds": "ds"}))

# Addestra il modello per la predizione della pericolosità
model_pericolosita = Prophet()
model_pericolosita.fit(data[["ds", "Pericolosita"]].rename(columns={"Pericolosita": "y", "ds": "ds"}))

# Crea un dataframe per le predizioni future fino al 2025
future = pd.DataFrame(columns=["ds"])  # Crea un dataframe vuoto con solo la colonna "ds"
future['ds'] = pd.date_range(start='2024-01-01', end='2025-12-31')  # Aggiungi le date al dataframe "future"

# Effettua le predizioni per latitudine, longitudine e pericolosità
pred_lat = model_lat.predict(future)
pred_lon = model_lon.predict(future)
pred_pericolosita = model_pericolosita.predict(future)

# Creazione dei grafici per le predizioni di latitudine, longitudine e pericolosità
fig_lat = px.line(pred_lat, x='ds', y='yhat', title='Predizioni per latitudine')
fig_lon = px.line(pred_lon, x='ds', y='yhat', title='Predizioni per longitudine')
fig_pericolosita = px.line(pred_pericolosita, x='ds', y='yhat', title='Predizioni per pericolosità')

# Visualizzazione dei grafici
fig_lat.show()
fig_lon.show()
fig_pericolosita.show()
