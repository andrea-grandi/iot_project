import multiprocessing
from predict_letter import GesturePredictionSystem
from my_speech_recognition import SpeechRecognitionSystem
import json
import serial
import joblib
import speech_recognition as sr

config_file = 'config.json'

def config_serial_arduino():
    try:
        with open(config_file, 'r') as config_file:
            config_data = json.load(config_file).get("arduino_serial_config", {})
            return serial.Serial(config_data['device'], config_data['baudrate'])
    except FileNotFoundError:
        print("Config file not found.")
        return None
    except Exception as e:
        print("Error occurred while configuring Arduino serial connection:", e)
        return None

def load_model():
    try:
        return joblib.load('model/trained_model.joblib')
    except FileNotFoundError:
        print("Model file not found.")
        return None
    except Exception as e:
        print("Error occurred while loading the model:", e)
        return None

def config_serial_esp():
    try:
        with open(config_file, 'r') as config_file:
            config_data = json.load(config_file).get("esp32_serial_config", {})
            return serial.Serial(config_data['device'], config_data['baudrate'])
    except FileNotFoundError:
        print("Config file not found.")
        return None
    except Exception as e:
        print("Error occurred while configuring ESP32 serial connection:", e)
        return None

def config_adafruit():
    try:
        with open(config_file, 'r') as config_file:
            return json.load(config_file).get("adafruit_config", {})
    except FileNotFoundError:
        print("Config file not found.")
        return None
    except Exception as e:
        print("Error occurred while configuring Adafruit:", e)
        return None

def init_recognizer():
    return sr.Recognizer()

def main_predict():
    model = load_model()
    ser = config_serial_arduino()
    if model is None or ser is None:
        exit(1)
    gp = GesturePredictionSystem(ser, model)
    gp.loop()

def main_bridge():
    recognizer = init_recognizer()
    ser = config_serial_esp()
    adafruit = config_adafruit()
    if recognizer is None or ser is None or adafruit is None:
        exit(1)
    sr_system = SpeechRecognitionSystem(ser, recognizer, adafruit)
    sr_system.loop()

if __name__ == "__main__":
    process_predict = multiprocessing.Process(target=main_predict)
    process_bridge = multiprocessing.Process(target=main_bridge)

    process_predict.start()
    process_bridge.start()

    process_predict.join()
    process_bridge.join()
