import speech_recognition as sr

def interpretar_microphone():
    recognizer = sr.Recognizer()

    with sr.Microphone() as fonte_audio:
        recognizer.adjust_for_ambient_noise(fonte_audio)

        print("say something...")
        fala = recognizer.listen(fonte_audio, timeout=3)

        try:
            texto = recognizer.recognize_google(fala, language="pt-BR")
            print("você disse:", texto)
        except sr.UnknownValueError:
            print("não entendi o que você disse!")

if __name__ == "__main__":
    interpretar_microphone()