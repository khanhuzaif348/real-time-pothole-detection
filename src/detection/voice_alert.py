import platform


def speak(message):
    if platform.system() != "Windows":
        return False

    try:
        import pyttsx3

        engine = pyttsx3.init("sapi5")
        engine.setProperty("rate", 160)
        engine.setProperty("volume", 1.0)

        engine.say(message)
        engine.runAndWait()
        engine.stop()

        return True

    except Exception as e:
        print(f"Voice alert unavailable: {e}")
        return False