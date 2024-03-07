import multiprocessing
from predict_letter import GesturePredictionSystem
from my_speech_recognition import SpeechRecognitionSystem
import json
import serial
import joblib
import speech_recognition as sr

config = 'config.json'

def config_serial_arduino():
    with open(config, 'r') as config_file:
        config_data = json.load(config_file).get("arduino_serial_config", {})
        return serial.Serial(config_data['device'], config_data['baudrate'])

def load_model():
    return joblib.load('model/trained_model.joblib')

def config_serial_esp():
    with open(config, 'r') as config_file:
        config_data = json.load(config_file).get("esp32_serial_config", {})
        return serial.Serial(config_data['device'], config_data['baudrate'])

def config_adafruit():
    with open(config, 'r') as config_file:
        return json.load(config_file).get("adafruit_config", {})

def init_recognizer():
    return sr.Recognizer()

def main_predict():
    model = load_model()
    ser = config_serial_arduino()
    gp = GesturePredictionSystem(ser, model)
    gp.loop()

def main_bridge():
    recognizer = init_recognizer()
    ser = config_serial_esp()
    adafruit = config_adafruit()
    sr = SpeechRecognitionSystem(ser, recognizer, adafruit)
    sr.loop()

if __name__ == "__main__":
    process_predict = multiprocessing.Process(target=main_predict)
    process_bridge = multiprocessing.Process(target=main_bridge)

    process_predict.start()
    process_bridge.start()

    process_predict.join()
    process_bridge.join()