import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Carica il dataset
train_set = pd.read_csv('../../dataset/sample_dataset/train_set.csv')
test_set = pd.read_csv('../../dataset/sample_dataset/test_set.csv')

# Dividi il dataset in feature e target
X_train = train_set.drop(columns=['LABEL'])
y_train = train_set['LABEL']
X_test = test_set.drop(columns=['LABEL'])
y_test = test_set['LABEL']

# Inizializza il modello Naive Bayes
model = GaussianNB()

# Addestramento del modello
start_time = time.time()
model.fit(X_train, y_train)
training_time = time.time() - start_time

# Esegui le previsioni sul set di test
y_pred = model.predict(X_test)

# Calcola le metriche di valutazione
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
conf_matrix = confusion_matrix(y_test, y_pred)

# Calcola l'accuratezza sui dati di addestramento
train_accuracy = accuracy_score(y_train, model.predict(X_train))

# Stampa le metriche di valutazione
print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")
print(f"Training Time: {training_time} seconds")


metrics = {'Accuracy': accuracy}

# Plot della confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')

# Plot dei valori delle metriche
plt.figure(figsize=(2, 6))
plt.bar(metrics.keys(), metrics.values(), color=['blue', 'green', 'red', 'orange'])

plt.show()


