import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Carica il dataset
dataset_path = 'dataset.csv'
dataset = pd.read_csv(dataset_path)

# Divide il dataset in features (X) e target (y)
X = dataset[['THUMB', 'INDEX', 'MIDDLE', 'G1', 'G2', 'G3']]
y = dataset['LABEL']

# Dividi il dataset in training set e test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crea un modello di Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Addestra il modello
model.fit(X_train, y_train)

# Effettua le previsioni sul test set
predictions = model.predict(X_test)

# Calcola l'accuratezza del modello sul test set
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy}')

# Salva il modello addestrato
import joblib
joblib.dump(model, 'trained_model.joblib')

"""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score

# Carica il dataset
dataset_path = 'dataset.csv'
dataset = pd.read_csv(dataset_path)

# Rimuovi la colonna 'LABEL' dal dataset
X = dataset[['THUMB', 'INDEX', 'MIDDLE', 'G1', 'G2', 'G3']]

# Crea un modello di K-Means con il numero desiderato di cluster e specifica n_init
n_clusters = 5  # Puoi scegliere il numero di cluster in base al tuo dominio
n_init = 10  # Imposta il numero di inizializzazioni desiderato
model = KMeans(n_clusters=n_clusters, n_init=n_init, random_state=42)

# Addestra il modello
model.fit(X)

# Ottieni le previsioni dal modello di clustering
predictions = model.predict(X)

# Nota: Poiché stiamo utilizzando un algoritmo di clustering, non avremo etichette reali.
# Se vuoi valutare la qualità del clustering, dovresti utilizzare metriche specifiche di clustering.

# Salva il modello addestrato
import joblib
joblib.dump(model, 'trained_clustering_model.joblib')
"""

