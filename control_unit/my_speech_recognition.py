import speech_recognition as sr
import serial
import json
import time

def load_serial_config():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        return config_data.get("arduino_serial_config", {}), config_data.get("esp32_serial_config", {})

def config_sensor_esp32():
    config_data_esp32 = load_serial_config()[1]
    return serial.Serial(config_data_esp32['device'], config_data_esp32['baudrate'])

def get_serial_data_esp32(ser_esp32):
    # Leggi i dati dalla seriale ESP32 (GPS)
    return ser_esp32.readline().decode('utf-8').strip()

def init_recognizer():
    # Inizializza il recognizer
    return sr.Recognizer()

def config_sensor_arduino():
    config_data = load_serial_config()
    return serial.Serial(config_data[0]['device'], config_data[0]['baudrate'])

def speech_rec():
    ser_arduino, ser_esp32 = config_sensor_arduino(), config_sensor_esp32()
    recognizer = init_recognizer()
    
    while True:
        with sr.Microphone() as source:
            print("Ascolto...")
            audio = recognizer.listen(source)

            try:
                # Utilizza il riconoscimento vocale di Google
                text = recognizer.recognize_google(audio, language='it-IT')
                print("Testo riconosciuto:", text)

                if "aiuto" in text.lower():
                    # Leggi e stampa i dati dalla seriale ESP32 (GPS)
                    serial_data_esp32 = get_serial_data_esp32(ser_esp32)
                    print("Dati dalla seriale ESP32 (GPS):\n", serial_data_esp32)

                # Invia il testo riconosciuto ad Arduino attraverso la connessione seriale
                #ser.write(text.encode('utf-8'))

            except sr.UnknownValueError:
                print("Impossibile riconoscere l'audio")
            except sr.RequestError as e:
                print(f"Errore durante la richiesta al servizio di riconoscimento vocale; {e}")
