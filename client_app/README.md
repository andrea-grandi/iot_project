# Cient App

- Client app creata attraverso MIT App Inventor. Utilizzo di un database specifico per le credenziali degli utenti, attraverso Google Sheets, con possibilità di cambiare password nel caso si fosse dimenticata.
- Connessione MQTT per inviare le coordinate del dispositivo mobile periodicamente. Il Broker MQTT notifica l'utente in caso di ingresso in una zona pericolosa. Oppure, si può inviare la propria posizione autonomamente (attraverso un apposito bottone) indicandola come pericolosa. Le posizioni sono contenute in un database dedicato.
- Utilizzo di IFTTT per inviare le notifiche ai dispositivi connessi al servizio, indicando l'username del dispositivo che sta entrando nella zona pericolosa.
