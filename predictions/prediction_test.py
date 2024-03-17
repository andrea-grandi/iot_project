import pandas as pd
from prophet import Prophet
import plotly.express as px


data = pd.read_csv("dataset_test.csv")

data['ds'] = pd.to_datetime(data['Data'])

model_lat = Prophet()
model_lat.fit(data[["ds", "Latitudine"]].rename(columns={"Latitudine": "y", "ds": "ds"}))

model_lon = Prophet()
model_lon.fit(data[["ds", "Longitudine"]].rename(columns={"Longitudine": "y", "ds": "ds"}))

model_pericolosita = Prophet()
model_pericolosita.fit(data[["ds", "Latitudine", "Longitudine", "Pericolosita"]].rename(columns={"Pericolosita": "y", "ds": "ds"}))

future = model_lat.make_future_dataframe(periods=365)
#future = future[future['ds'].dt.year <= 2025]

pred_lat = model_lat.predict(future)
pred_lon = model_lon.predict(future)
pred_pericolosita = model_pericolosita.predict(future)

fig_lat = px.line(pred_lat, x='ds', y='trend', title='Linea di tendenza per latitudine')
fig_lon = px.line(pred_lon, x='ds', y='trend', title='Linea di tendenza per longitudine')
fig_pericolosita = px.line(pred_pericolosita, x='ds', y='trend', title='Linea di tendenza per pericolosità')

fig_lat.show()
fig_lon.show()
fig_pericolosita.show()


