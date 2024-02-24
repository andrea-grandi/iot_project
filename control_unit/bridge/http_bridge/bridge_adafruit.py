import json
import serial
import requests
import time
import subprocess

def leggi_configurazione(file_config):
    with open(file_config, 'r') as f:
        configurazione = json.load(f)
    return configurazione

def leggi_dati_seriale(ser):
    dato_seriale = ser.readline().decode().strip()
    print(f"Dato dalla seriale: {dato_seriale}")

    # Estrai i valori dalla stringa seriale
    values = dato_seriale.split(',')
    
    # Verifica la presenza dei valori attesi
    if len(values) == 5:
        # Creazione del dizionario con i valori letti
        if values[0] == "INVALID" or values[1] == "INVALID":
            data_dict = {'value': 0, 'lat': 0, 'lon': 0}
        else:
            data_dict = {'value': 1, 'lat': float(values[0]), 'lon': values[1]}
        return data_dict
    else:
        print("Errore: La stringa seriale non contiene i valori attesi.")
        return None

def invia_data_ad_adafruit(device, baudrate, url, key):
    try:
        ser = serial.Serial(device, baudrate)
        print(f"Connessione alla seriale {device} avvenuta con successo.")
        
        while True:
            # Leggi i dati dalla seriale e crea il dizionario
            data_dict = leggi_dati_seriale(ser)

            if data_dict:
                # Costruisci il comando curl_command
                curl_command = f'curl -H "Content-Type: application/json" -d \'{{"value": {data_dict["value"]}, "lat": {data_dict["lat"]}, "lon": "{data_dict["lon"]}"}}\' -H "X-AIO-Key: {key}" {url}'

                # Esegui il comando curl
                subprocess.run(curl_command, shell=True)

            time.sleep(10)  # Attendiamo 10 secondi prima di leggere il prossimo dato

    except Exception as e:
        print(f"Errore: {e}")
    finally:
        if ser.is_open:
            ser.close()
            print("Connessione alla seriale chiusa.")

def http_bridge():
    config_file = "config.json"
    configurazione = leggi_configurazione(config_file)

    esp32_config = configurazione.get("esp32_serial_config", {})
    device = esp32_config.get("device")
    baudrate = esp32_config.get("baudrate")

    adafruit_config = configurazione.get("adafruit_config", {})
    url = adafruit_config.get("url")
    key = adafruit_config.get("key")

    if device and baudrate and url and key:
        invia_data_ad_adafruit(device, baudrate, url, key)
    else:
        print("Configurazione incompleta. Assicurati di fornire tutti i parametri necessari nel file config.json.")
