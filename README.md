<div align="center">

![Made with Doom Emacs](https://img.shields.io/github/tag/doomemacs/doomemacs.svg?style=flat-square&label=release&color=58839b)
![Latest commit](https://img.shields.io/github/last-commit/doomemacs/doomemacs/master?style=flat-square)

# Sign Gloves

*IoT and 3D Intelligent Systems project 2023/2024*

**Sign Glove** is a sistem that convert sign language in audio for interactions between deaf people and non-deaf people. Through the use of sensors (flex sensors, microphone, GPS, etc.), it is able to translate sign language. Additionally, it can detect potentially hazardous situations in the environment (such as ambulance sounds, loud noises, or signals of distress) and alert others through the gloves.

</div>

## Structure

- Controller: Arduino/Esp32 - C++
- Android App: MIT App Inventor
- Web App: Flask - Python
- Hazard Prediction: 
- Comunications: HTTP/MQTT
- Database: SQLite/CouchDB

## Control Unit 

The control unit manages the sensor and actuator components of the glove. The control unit is also responsible for bridging between Arduino and the cloud.

## Android App

The smartphone client manages the display of hazard messages in the area. Through a registration interface, we can add new gloves.

## Web App

The Web App is the centre of this system. The backend part manages the database and all the requests, while in the frontend is possible to manage ones dispositives.

## Predictions

This system is capable of predicting hazardous situations and then alerting prevention agencies, hospitals, or the police.

## Credits

- Andrea Grandi: [@andrea-grandi](https://github.com/andrea-grandi)
- Luca Montagnani: [@montaoo](https://github.com/montaooo)
- Daniele Vellani: [@franzione1](https://github.com/franzione1)
