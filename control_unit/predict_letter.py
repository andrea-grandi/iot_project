import pandas as pd
import serial
import joblib
import json
import time

# ARDUINO

class GesturePredictionSystem:
    def __init__(self, ser, model):
        self.ser = ser
        self.model = model

    def convert_to_letter(self, prediction):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        return alphabet[prediction - 1] if 1 <= prediction <= 26 else 'unknown'

    def loop(self):
        while True:
            # Leggi i primi 6 dati dalla seriale
            data = self.ser.readline().decode('utf-8').strip().split(',')[:6]

            # Verifica se il numero di dati è corretto
            if len(data) == 6:  # Assumendo che ci siano 6 dati (THUMB, INDEX, MIDDLE, G1, G2, G3)
                # Converte i dati in interi
                data = [int(value) for value in data]

                # Crea un DataFrame con i dati letti dalla seriale
                df = pd.DataFrame([data], columns=['THUMB', 'INDEX', 'MIDDLE', 'G1', 'G2', 'G3'])

                # Effettua la previsione della lettera con il modello addestrato
                predicted_number = self.model.predict(df)[0]

                # Converte il numero predetto alla lettera corrispondente
                predicted_letter = self.convert_to_letter(predicted_number) 

                self.ser.write(predicted_letter.encode('utf-8'))

                # Flush della seriale per assicurarsi che tutti i dati siano stati inviati
                self.ser.flush()
                
                # Stampa la lettera risultante
                print("Predicted Letter:", predicted_letter)
