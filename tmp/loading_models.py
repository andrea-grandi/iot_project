from pandas import DataFrame, read_csv
import pandas as pd 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import serial
import pyttsx3
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn import tree
import joblib
import warnings
from sklearn.exceptions import DataConversionWarning
import time

# Assuming you've trained the model with these features
feature_columns = ['THUMB', 'INDEX', 'MIDDLE', 'RING', 'LITTLE', 'G1', 'G2', 'G3']
ser = serial.Serial('/dev/cu.usbmodem21301', baudrate=9600, timeout=1)
# Imposta il ritardo desiderato tra le letture in millisecondi
delay_between_readings = 200  # 500 millisecondi

for i in range(3):
    # Leggi la seriale in blocchi di 100 byte alla volta
    arduinodata = b""
    while b"\n" not in arduinodata:
        arduinodata += ser.read(size=100)
        time.sleep(delay_between_readings / 1000.0)  # Converti il ritardo in secondi

        # Dividi le righe basate su '\r\n' (CRLF)
        lines = arduinodata.decode('ascii').strip().split('\r\n')

        for line in lines:
            values = line.split(',')

            # Controlla se ci sono esattamente 8 valori
            if len(values) == 8:
                print("Received values:", values)
                # Aggiungi qui la tua logica per l'elaborazione dei dati
            else:
                print("Error: Insufficient or invalid values received from serial.")
  # Check if values has enough elements
    if values and len(values) == 8:
        try:
        # Attempt to convert values to integers
            a, b, c, d, e, f, g, h = [int(s) for s in values]

            example = np.array([a, b, c, d, e, f, g, h])

            # Reshape the example array
            example = example.reshape(1, -1)

            # Load the pre-trained KNN model
            mj7 = joblib.load('KNN')

            # Imposta i nomi delle colonne nel modello KNN
            mj7.feature_names_in_ = ['THUMB', 'INDEX', 'MIDDLE', 'RING', 'LITTLE', 'G1', 'G2', 'G3']

            # Make predictions
            predicted_label = mj7.predict(example)
            print(predicted_label)
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print("Error: Insufficient values received from serial.")

'''

#df = pd.read_csv('dataset.csv')
#X=df[['THUMB','INDEX','MIDDLE','RING','LITTLE','G1','G2','G3']]
#Y=df[['LABEL']]
feature_columns = ['THUMB', 'INDEX', 'MIDDLE', 'RING', 'LITTLE', 'G1', 'G2', 'G3']

ser = serial.Serial('/dev/cu.usbmodem21301', baudrate=9600, timeout=1)
for i in range(3):
    arduinodata = ser.readline().strip()
    values = arduinodata.decode('ascii').split(',')
    a, b, c, d, e, f, g, h = [int(s) for s in values]
    example = np.array([a, b, c, d, e, f, g, h])

example = example.reshape(1, -1)
        # K Nearest Neighbor

#x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state = 60)
#model = KNeighborsClassifier()
#model.fit(x_train,y_train)
#joblib.dump(rf,'randomforest')
mj7 = joblib.load('KNN')
# Make predictions
predicted_label = mj7.predict(example)
print(predicted_label)
#predicted=model.predict(x_test)
#accuracy = accuracy_score(y_test,predicted)
#print("Accuracy for KNN is ",accuracy)


        # Random Forest

#x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state = 60)
#rf = RandomForestRegressor(n_estimators = 1000)
#rf.fit(x_train,y_train)
#predictions = rf.predict(x_test)
#accuracy = r2_score(y_test,predictions)
#print('\nAccuracy for random forest:\n', round(accuracy, 2)*100, '%.')
#joblib.dump(rf,'randomforest')
  #mj = joblib.load('randomforest')
  #print(mj.predict(example))
#accuracy1 = r2_score(x_train,y_train)
#print('\nAccuracy for training random forest:\n', round(accuracy1, 2)*100, '%.')


        # Naive Bayes    
#
#x_train2, x_test2, y_train2, y_test2 = train_test_split(X, Y, test_size=0.3, random_state = 60)
#GNB = GaussianNB()
#GNB.fit(x_train,y_train)
#joblib.dump(GNB,'NaiveBayes')
  #mj1 = joblib.load('NaiveBayes')
  #print(mj1.predict(example))
#predicted2 = GNB.predict(x_test2)
#accuracy2 = accuracy_score(y_test2,predicted2)
#print("Accuracy for KNN is ",accuracy2)


        # SVM 
#x_train3, x_test3, y_train3, y_test3 = train_test_split(X, Y, test_size=0.3, random_state = 60)        
#svc = svm.SVC(kernel='linear').fit(x_train,y_train)
#joblib.dump(svc,'SVM')
#mj2 = joblib.load('SVM')
#print(mj2.predict(example))
#predicted3 = svc.predict(x_test)
#accuracy3 = accuracy_score(y_test,predicted3)
#print("Accuracy for SVM is ",accuracy3)        


        # Logistic Regression
#x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state = 60)        
#clf = LogisticRegression().fit(x_train,y_train)
#joblib.dump(clf,'logistic')
  #mj3 = joblib.load('logistic')
  #print(mj3.predict(example))
#predicted4 = clf.predict(x_test)
#accuracy4 = r2_score(y_test,predicted4)
#print("Accuracy for Logistic Regression is ",accuracy4)        



        # Decision Tree

#Dtree = tree.DecisionTreeClassifier().fit(x_train,y_train)
#joblib.dump(Dtree,'DecisionTree')
  #mj4 = joblib.load('DecisionTree')
  #print(mj4.predict(example))
#print(a)
#predicted5 = Dtree.predict(x_test)
#accuracy5 = accuracy_score(y_test,predicted5)
#print("Accuracy for Logistic Regression is ",accuracy5)   
#if  a <= 1:
#if a > 0 and a <=1 :
#    abc = "victory"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 1 and a <=2 :
#    abc = "Comehere"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 2 and a <=3 :
#    abc = "Okay"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 3 and a <=4 :
#    abc = "Stop"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 4 and a <=5 :
#    abc = "You"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 5 and a <=6 :
#    abc = "Hope"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 6 and a <=7 :
#    abc = "Failure"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 7 and a <=8 :
#    abc = "Really"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 8 and a <=9 :
#    abc = "Quote"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 9 and a <=10 :
#    abc = "No"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 10 and a <=11 :
#    abc = "I Love you"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()    
#elif a > 11 and a <=12 :
#    abc = "Livelong"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 12 and a <=13 :
#    abc = "Thats it"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 13 and a <=14 :
#    abc = "Solidarity"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 14 and a <=15 :
#    abc = "Rock On"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 15 and a <=16 :
#    abc = "Good Bye"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 16 and a <=17 :
#    abc = "What is wrong"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 17 and a <=18 :
#    abc = "Why"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()
#elif a > 18 and a <= 19 :
#    abc = "Rest room"
#    engine = pyttsx3.init()
#    engine.say('Predicted Output')
#    engine.say(abc)
#    engine.runAndWait()




'''