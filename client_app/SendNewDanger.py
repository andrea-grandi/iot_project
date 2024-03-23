import paho.mqtt.client as mqtt
import struct
import requests
import couchdb
from geopy.distance import geodesic
import datetime

usersLat = {} 
usersLong = {}

# Funzione per ottenere tutte le coordinate del DB
def get_all_gps_coordinates():
    url = "http://admin:cacdga1302@89.168.18.2/iot_project/_all_docs?include_docs=true"
    response = requests.get(url)
    data = response.json()
    coordinates = []

    # Ciclo di tutte le righe del database
    for row in data['rows']:
        doc = row['doc']
        # Verifica che il documento abbia delle coordinate
        if 'lat' in doc and 'lon' in doc:
            lat = float(doc['lat'])
            lon = float(doc['lon'])
            coordinates.append((lat,lon))
    return coordinates

# Funzione per inserire le coordinate nel DB
def insert_coordinates_to_db(lat,lon):
    # Connessione al DB
    couch = couchdb.Server('http://admin:cacdga1302@89.168.18.2/')
    db = couch['iot_project']
    current_date = datetime.date.today().isoformat() # Calcolo della data attuale

    doc = {
        'lat' : lat,
        'lon' : lon,
        'ds' : current_date,
        'y' : 1
    }

    # Salvataggio doc nel DB
    try:
        db.save(doc)
        print("Coordinate inserite nel database")
    except Exception as e:
        print("Errore nell'inserimento delle coordinate nel db")

# Funzione per calcolare la distanza tra due coordinate
def distance_calc(coordinate1, coordinate2):
    return geodesic(coordinate1, coordinate2).meters

# Ricezione del messaggio
def on_message(client, userdata, msg):
    print(msg.payload.decode())

    # Divido la stringa usando lo spazio come divisore
    parts = msg.payload.decode().split(' ')

    # Controllo che la struttura del messaggio sia corretta
    if len(parts) == 2:
        username = parts[0]
        payload = parts[1]

        if username not in usersLat or username not in usersLong:
            usersLat[username] = None
            usersLong[username] = None
        
        if payload.startswith("Lat:"):
            usersLat[username] = float(payload.split(':')[1])
        else:
            usersLong[username] = float(payload.split(':')[1])         
    
    # Prendo le coordinate pericolose dal DB
    dangerous_coordinates = get_all_gps_coordinates()

    check = False

    # Controllo che siano state ricevute sia Latitudine che Longitudine
    if usersLat[username] is not None and usersLong[username] is not None:
        insert_coordinates_to_db(usersLat[username], usersLong[username])
        usersLat[username] = None
        usersLong[username] = None

mqttBroker = 'mqtt.eclipseprojects.io'
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, 'IdNew')
client.on_message = on_message
client.connect(mqttBroker)
client.subscribe('NewDanger') # Topic al quale è connesso il ricevitore

# Ciclo infinito, fino alla disconnessione del dispositivo
client.loop_forever()
