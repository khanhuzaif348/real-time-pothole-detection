import pyttsx3

def speak(message):
    engine = pyttsx3.init('sapi5')

    engine.setProperty('rate', 160)
    engine.setProperty('volume', 1.0)

    engine.say(message)
    engine.runAndWait()

    engine.stop()