import pandas as pd
import serial
import joblib
import json

def load_serial_config():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        return config_data.get("arduino_serial_config", {}), config_data.get("esp32_serial_config", {})

def convert_to_letter(prediction):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return alphabet[prediction - 1] if 1 <= prediction <= 26 else 'unknown'

def load_model():
    # Carica il modello addestrato
    return joblib.load('trained_model.joblib')

def config_sensor():
    config_data = load_serial_config()
    return serial.Serial(config_data[0]['device'], config_data[0]['baudrate'])

def predict():
    model = load_model()
    ser_sensors = config_sensor()
    while True:
        # Leggi i primi 6 dati dalla seriale
        arduino_data = ser_sensors.readline().decode('utf-8').strip().split(',')[:6]

        # Verifica se il numero di dati è corretto
        if len(arduino_data) == 6:  # Assumendo che ci siano 6 dati (THUMB, INDEX, MIDDLE, G1, G2, G3)
            # Converte i dati in interi
            arduino_data = [int(value) for value in arduino_data]

            # Crea un DataFrame con i dati letti dalla seriale
            df = pd.DataFrame([arduino_data], columns=['THUMB', 'INDEX', 'MIDDLE', 'G1', 'G2', 'G3'])

            # Effettua la previsione della lettera con il modello addestrato
            predicted_number = model.predict(df)[0]

            # Converte il numero predetto alla lettera corrispondente
            predicted_letter = convert_to_letter(predicted_number) 

            ser_sensors.write(predicted_letter.encode('utf-8'))

            # Flush della seriale per assicurarsi che tutti i dati siano stati inviati
            ser_sensors.flush()
            
            # Stampa la lettera risultante
            print("Predicted Letter:", predicted_letter)
