from my_speech_recognition import SpeechRecognitionSystem
import json
import serial
import speech_recognition as sr


def config_serial_esp():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file).get("esp32_serial_config", {})
        return serial.Serial(config_data['device'], config_data['baudrate'])

def config_adafruit():
    with open('config.json', 'r') as config_file:
        return json.load(config_file).get("adafruit_config", {})

def init_recognizer():
    return sr.Recognizer()


if __name__ == "__main__":
    recognizer = init_recognizer()
    ser = config_serial_esp()
    adafruit = config_adafruit()
    sr = SpeechRecognitionSystem(ser, recognizer, adafruit)
    sr.loop()
    