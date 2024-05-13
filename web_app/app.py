from flask import Flask, render_template, jsonify
import requests
import socket

app = Flask(__name__)

# Funzione per ottenere i dati dal database
def get_all_gps_coordinates():
    url = ""
    response = requests.get(url)
    data = response.json()
    coordinates = []

    # Ciclo di tutte le righe del database
    for row in data['rows']:
        doc = row['doc']
        # Verifica che il documento abbia delle coordinate scritte in esso
        if 'lat' in doc and 'lon' in doc:
            lat = doc['lat']
            lon = doc['lon']
            coordinates.append({'lat': lat, 'lon': lon})
    return coordinates

# Pagina principale
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Endpoint per ottenere i dati GPS dal database
@app.route('/gps_data')
def gps_data():
    data = get_all_gps_coordinates()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
