import speech_recognition as sr
import serial
import json
import time
import subprocess
import requests

# ESP

server_ip = "http://admin:cacdga1302@89.168.18.2/iot_project"

class SpeechRecognitionSystem:
    
    def __init__(self, ser, recognizer, adafruit):
        self.ser = ser
        self.recognizer = recognizer
        self.adafruit = adafruit
    
    def get_send(self):
        return self.send	

    def set_send(self, send):
        self.send = send

    def get_serial_data(self):
        return self.serial_data

    def serial_data(self):
        data = self.ser.readline().decode('utf-8').strip().split(',')

        if len(data) == 5:
            if data[0] == "INVALID" or data[1] == "INVALID":
                data_dict = {'value': 0, 'lat': 0, 'lon': 0}
            else:
                data_dict = {'value': 1, 'lat': float(data[0]), 'lon': data[1]}
            return data_dict
        else:
            print("Errore: La stringa seriale non contiene i valori attesi.")
            return None

    def loop(self):
        while (True):
            with sr.Microphone() as source:
                print("\nAscolto...")
                audio = self.recognizer.listen(source)

                try:
                    # Utilizza il riconoscimento vocale di Google
                    text = self.recognizer.recognize_google(audio, language='it-IT')
                    print("Testo riconosciuto:", text)

                    # Esempio di WARNING con la parola "AIUTO"
                    if text == "aiuto":
                        data_dict = self.serial_data()
                
                        if data_dict:
                            # Invio i dati ad Adafruit
                            curl_command = f'curl -H "Content-Type: application/json" -d \'{{"value": {data_dict["value"]}, "lat": {data_dict["lat"]}, "lon": "{data_dict["lon"]}"}}\' -H "X-AIO-Key: {self.adafruit.get("key")}" {self.adafruit.get("url")}'
                            subprocess.run(curl_command, shell=True)

                            # Invio i dati al Database
                            myinfo = {'value': data_dict["value"], 'lat': data_dict["lat"], 'lon': data_dict["lon"]}
                            value_sent = requests.post(server_ip, json=myinfo)

                except sr.UnknownValueError:
                    print("Impossibile riconoscere l'audio")
                except sr.RequestError as e:
                    print(f"Errore durante la richiesta al servizio di riconoscimento vocale; {e}")

