import joblib
import schedule
import time
import requests
from position_predict import Prediction 

# Funzione per connettersi al database e estrarre i dati
def get_all_gps_coordinates_and_train():
    url = ""
    response = requests.get(url)
    data = response.json()
    coordinates = []

    # Ciclo di tutte le righe del database
    for row in data['rows']:
        doc = row['doc']
        # Verifica che il documento abbia delle coordinate
        if 'y' in doc and 'ds' in doc:
            y = doc['y']
            ds = doc['ds']
            coordinates.append({'y': y, 'ds': ds})
    
    model, pred_df = Prediction.make_prediction(coordinates)
    save_model(model,  model_path = "trained_model.pkl")
    return model, pred_df


# Funzione per salvare il modello allenato
def save_model(model, model_path):
    joblib.dump(model, model_path)
    print("Modello salvato con successo.")


# Pianifica l'addestramento del modello una volta al mese
schedule.every().month.do(get_all_gps_coordinates_and_train())

# Loop principale
while True:
    # Esegui il processo di pianificazione
    schedule.run_pending()
    time.sleep(1)
