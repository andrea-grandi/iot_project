import paho.mqtt.client as mqtt
import struct
import requests
from geopy.distance import geodesic

# Dizionari per contenere Latitudine e Longitudine associate all'username
usersLat = {} 
usersLong = {}

# Funzione per mandare una richiesta web a IFTTT
def send_request_IFTTT(username):
    url = "https://maker.ifttt.com/trigger/send_danger/with/key/buRicbM1I8d6oIlQBiJbAh"
    payload = {'value1': username}  # Includi l'identificatore del dispositivo come payload
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("Notifica inviata con successo!")

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

# Funzione per calcolare la distanza tra due coordinate
def distance_calc(coordinate1, coordinate2):
    return geodesic(coordinate1, coordinate2).meters

# Funzione che divide la stringa in due, differenziando utenti, latitudine e longitudine (inseriti nelle variabili globali)
def split_coordinates(msg):
    # Divido la stringa usando lo spazio come divisore
    parts = msg.split(' ')

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
    return username

# Funzione di ricezione del messaggio ed estrazione dell'username
def on_message(client, userdata, msg):
    print(msg.payload.decode())
    
    # Inserisco la coordinata associata all'utente corretto nel dizionario
    username = split_coordinates(msg.payload.decode())
    
    # Prendo le coordinate pericolose dal DB
    dangerous_coordinates = get_all_gps_coordinates()

    # Controllo che siano state ricevute sia Latitudine che Longitudine
    if usersLat[username] is not None and usersLong[username] is not None:
        for coordinate in dangerous_coordinates:
            distance = distance_calc((usersLat[username], usersLong[username]), coordinate)
            if distance < 500:
                client.publish(username, 'Pericolo')
                send_request_IFTTT(username)
                usersLat[username] = None
                usersLong[username] = None
                break

# Indirizzo del broker MQTT
mqttBroker = 'mqtt.eclipseprojects.io'
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, 'IdRec')
client.on_message = on_message
client.connect(mqttBroker)
client.subscribe('ToDB') # Topic al quale è connesso il ricevitore

# Ciclo infinito, fino alla disconnessione del dispositivo
client.loop_forever()
