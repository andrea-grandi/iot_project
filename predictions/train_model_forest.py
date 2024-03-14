import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import RFE

# Carica il dataset
df = pd.read_csv('train/train_positions_dataset_modena.csv')

# Seleziona le colonne per il clustering
X = df[['Latitudine', 'Longitudine']]

# Colonna addestramento modello
y = df['Tipo']

# Inizializza il modello per la feature selection
estimator = RandomForestClassifier()

# Seleziona le migliori 10 features tramite RFE
selector = RFE(estimator, n_features_to_select=10, step=1)
selector.fit(X, y)
X_selected = selector.transform(X)

# Suddividi i dati per addestramento e test
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

# Inizializza il modello Random Forest per la classificazione
model = RandomForestClassifier()

# Allena con i dati di train
model.fit(X_train, y_train)

# Predicta
y_pred = model.predict(X_test)

# Calcola l'accuracy nei predict
accuracy = accuracy_score(y_test, y_pred)

# Stampa l'accuracy
print(f"Accuracy: {accuracy}")

