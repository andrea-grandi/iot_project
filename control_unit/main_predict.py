from predict_letter import GesturePredictionSystem
import json
import serial
import joblib


def config_serial_arduino():
    try:
        with open('config.json', 'r') as config_file:
            config_data = json.load(config_file).get("arduino_serial_config", {})
            return serial.Serial(config_data['device'], config_data['baudrate'])
    except FileNotFoundError:
        print("Config file not found.")
        return None
    except Exception as e:
        print("Error occurred while configuring serial connection:", e)
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


if __name__ == "__main__":
    model = load_model()
    if model is None:
        exit(1)

    ser = config_serial_arduino()
    if ser is None:
        exit(1)

    gp = GesturePredictionSystem(ser, model)
    gp.loop()
