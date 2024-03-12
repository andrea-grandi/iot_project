from my_speech_recognition import SpeechRecognitionSystem
import json
import serial
import speech_recognition as sr


def config_serial_esp():
    try:
        with open('config.json', 'r') as config_file:
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
        with open('config.json', 'r') as config_file:
            return json.load(config_file).get("adafruit_config", {})
    except FileNotFoundError:
        print("Config file not found.")
        return None
    except Exception as e:
        print("Error occurred while configuring Adafruit:", e)
        return None

def init_recognizer():
    return sr.Recognizer()


if __name__ == "__main__":
    recognizer = init_recognizer()
    ser = config_serial_esp()
    if ser is None:
        exit(1)
    
    adafruit = config_adafruit()
    if adafruit is None:
        exit(1)
    
    sr_system = SpeechRecognitionSystem(ser, recognizer, adafruit)
    sr_system.loop()
    
