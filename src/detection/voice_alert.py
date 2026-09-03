import platform


def speak(message):
    # Voice alerts are supported locally on Windows.
    # Streamlit Cloud runs on Linux.
    if platform.system() != "Windows":
        return

    import pyttsx3

    engine = pyttsx3.init("sapi5")
    engine.setProperty("rate", 160)
    engine.setProperty("volume", 1.0)

    engine.say(message)
    engine.runAndWait()
    engine.stop()