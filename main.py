import multiprocessing
from my_speech_recognition import speech_rec
from predict_letter import predict

def main():
    # Creazione dei processi
    process_predict_letters = multiprocessing.Process(target=predict)
    process_speech_recognition = multiprocessing.Process(target=speech_rec)

    try:
        # Avvio dei processi
        process_predict_letters.start()
        process_speech_recognition.start()

        # Attendi che entrambi i processi terminino
        process_predict_letters.join()
        process_speech_recognition.join()

    except KeyboardInterrupt:
        # Interrompi i processi in caso di interruzione da tastiera (CTRL+C)
        process_predict_letters.terminate()
        process_speech_recognition.terminate()

    finally:
        # Assicurati di chiudere i processi in ogni caso
        process_predict_letters.join()
        process_speech_recognition.join()

if __name__ == "__main__":
    main()
        
