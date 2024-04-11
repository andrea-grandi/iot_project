from flask import Flask, render_template, jsonify
import requests
import socket

app = Flask(__name__)

#def get_latest_gps_coordinates():
#    url = ""
#    response = requests.get(url)
#    data = response.json()
#    latest_doc_id = data['rows'][0]['id']
#    latest_doc_url = f""
#    response_latest_doc = requests.get(latest_doc_url)
#    latest_doc_data = response_latest_doc.json()
#    lat = latest_doc_data.get('lat')
#    lon = latest_doc_data.get('lon')
#    return {'lat': lat, 'lon': lon}

# Funzione per ottenere i dati dal database
def get_all_gps_coordinates():
    url = "http://admin:cacdga1302@89.168.18.2/iot_project/_all_docs?limit=1&descending=true"
    response = requests.get(url)
    data = response.json()
    coordinates = []

    # Ciclo di tutte le righe del database
    for row in data['rows']:
        doc = row['doc']
        # Verifica che il documento abbia delle coordinate
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
    print(str(data))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
