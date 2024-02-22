import pandas as pd
import serial
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import subprocess
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import time

# Carica il dataset
dataset_path = 'dataset.csv'
dataset = pd.read_csv(dataset_path)

ser_sensors = serial.Serial('/dev/cu.usbmodem21301', 115200, timeout=1)
#ser_actuators = serial.Serial('/dev/cu.usbmodem21301', 250000)


# Divide il dataset in features (X) e target (y)
X = dataset[['THUMB', 'INDEX', 'MIDDLE', 'G1', 'G2', 'G3']]
y = dataset['LABEL']

# Dividi il dataset in training set e test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crea un modello di Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Addestra il modello
model.fit(X_train, y_train)

# Effettua le previsioni sul test set
predictions = model.predict(X_test)

# Calcola l'accuratezza del modello sul test set
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy}')

# Adesso puoi utilizzare questo modello per prevedere la lettera in base ai dati della seriale
# Sostituisci la seguente parte con la tua logica di lettura dei dati dalla seriale
# e l'adattamento dei dati al formato giusto per il modello.
def convert_to_letter(prediction):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return alphabet[prediction - 1] if 1 <= prediction <= 26 else 'unknown'

while True:
    # Leggi i dati dalla seriale
    arduino_data = ser_sensors.readline().decode('utf-8').strip().split(',')

    #print(arduino_data)
    
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

        #time.sleep(0.5)
