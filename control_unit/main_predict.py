from predict_letter import GesturePredictionSystem
import json
import serial
import joblib


def config_serial_arduino():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file).get("arduino_serial_config", {})
        return serial.Serial(config_data['device'], config_data['baudrate'])

def load_model():
    return joblib.load('model/trained_model.joblib')


if __name__ == "__main__":
    model = load_model()
    ser = config_serial_arduino()
    gp = GesturePredictionSystem(ser, model)
    gp.loop()
