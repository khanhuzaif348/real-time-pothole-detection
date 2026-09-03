import platform


def speak(message):

    # Streamlit Cloud runs Linux.
    # Voice alerts are only enabled on Windows.
    if platform.system() != "Windows":
        return

    import pyttsx3

    engine = pyttsx3.init("sapi5")

    engine.setProperty("rate", 160)
    engine.setProperty("volume", 1.0)

    engine.say(message)
    engine.runAndWait()
    engine.stop()