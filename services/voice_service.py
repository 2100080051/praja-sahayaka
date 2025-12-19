import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import time

def speak_telugu(text: str):
    """
    Converts Telugu text to speech and plays it.
    """
    print(f"Agent (Speaking): {text}")
    try:
        tts = gTTS(text=text, lang='te')
        filename = "temp_output.mp3"
        tts.save(filename)
        
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
        os.remove(filename)
    except Exception as e:
        print(f"TTS Error: {e}")

def listen_mic():
    """
    Listens to the microphone and returns text (Telugu).
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (Speak in Telugu)")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Processing audio...")
            text = recognizer.recognize_google(audio, language="te-IN")
            print(f"User (Transcribed): {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"STT Error: {e}")
            return None
        except Exception as e:
            print(f"Mic Error: {e}")
            return None
