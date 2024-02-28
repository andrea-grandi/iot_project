import serial
import csv

# Impostare la porta seriale appropriata e il baud rate
ser = serial.Serial('/dev/cu.usbmodem21201', 115200)  # Sostituire 'COMx' con la porta seriale corretta

# Aprire un file CSV in modalità di scrittura
with open('dataset/test.csv', 'w', newline='') as file:
    # Creare un oggetto scrittore CSV
    writer = csv.writer(file)

    # Scrivere l'intestazione delle colonne nel file CSV
    writer.writerow(["THUMB","INDEX","MIDDLE","G1","G2","G3"])

    # Leggere i dati dalla seriale e scriverli nel file CSV
    while True:  # Numero di dati da leggere
        # Leggere una riga di dati dalla seriale e rimuovere i caratteri di newline
        data = ser.readline().decode().strip()

        # Dividere i dati in una lista di valori
        values = [int(val.strip()) for val in data.split(',')]

        # Scrivere solo i primi sei valori nel file CSV
        writer.writerow(values[:6])

# Chiudere la porta seriale
ser.close()
