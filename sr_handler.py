import speech_recognition as sr
import io

def transcribe_audio(audio_bytes):
    with open("temp_input.wav", "wb") as f:
        f.write(audio_bytes)
        
    r = sr.Recognizer()
    try:
        with sr.AudioFile("temp_input.wav") as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="te-IN")
            return text
    except Exception:
        return None
