'''pip install SpeechRecognition'''
'''pip install PyAudio'''
import speech_recognition as sr

listener = sr.Recognizer()

with sr.Microphone() as micro:
    print("Esuchando...")
    sonido = listener.listen(micro)
    texto = listener.recognize_google(sonido, language="es_MX")
    print(texto)