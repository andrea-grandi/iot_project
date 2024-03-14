import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Carica il dataset
df = pd.read_csv('train_positions_dataset_modena.csv')

# Seleziona le colonne per il clustering
X_scaled = df[['Latitudine', 'Longitudine']]

# Colonna addestramento modello
y = df['Tipo']

# Crea una lista vuota per memorizzare i punteggi della silhouette
silhouette_scores = []

# Standardizza i dati
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_scaled)

# Prova un numero di cluster da 2 a 100
for n_clusters in range(2, 101):
    # Crea il modello K-Means
    model = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    
    # Addestra il modello e predici i cluster per ciascun punto
    cluster_labels = model.fit_predict(X_scaled)
    
    # Calcola il punteggio della silhouette per il numero corrente di cluster
    silhouette_avg = silhouette_score(X_scaled, cluster_labels)
    
    # Aggiungi il punteggio alla lista
    silhouette_scores.append(silhouette_avg)

# Trova il numero ottimale di cluster con il punteggio più alto della silhouette
optimal_num_clusters = silhouette_scores.index(max(silhouette_scores)) 

# Inizializza il modello KMeans per il clustering
model = KMeans(n_clusters=optimal_num_clusters)

# Seleziona le colonne per il clustering
X_scaled = df[['Latitudine', 'Longitudine']]

# Colonna addestramento modello
y = df['Tipo']

# Standardizza i dati
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_scaled)

# Suddividi i dati per addestramento e test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Allena con i dati di train
model.fit(X_train, y_train)

# Predicta
y_pred = model.predict(X_test)

# Calcola l'accuraacy nei predict
accuracy = accuracy_score(y_test, y_pred)

# Stampa l'accuracy
print(f"Accuracy: {accuracy}")
