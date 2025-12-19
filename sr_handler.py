import speech_recognition as sr
import io

from pydub import AudioSegment
import os

# Robustly Add local ffmpeg to PATH so pydub can find both ffmpeg and ffprobe
# This is better than just setting AudioSegment.converter as it handles ffprobe too
ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
if os.path.exists(os.path.join(ffmpeg_dir, "ffmpeg.exe")):
    # Prepend to PATH
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]
    # Also explicity set for safety
    AudioSegment.converter = os.path.join(ffmpeg_dir, "ffmpeg.exe")
    
import time

def transcribe_audio(audio_bytes, language="te-IN"):
    if not audio_bytes:
        return None

    start_time = time.time()
    print(f"[{start_time}] Starting transcription...")

    # Convert WebM (or whatever browser sends) to WAV using pydub
    # This is crucial because speech_recognition mainly likes WAV/AIFF/FLAC
    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        # Export as WAV to a memory buffer or file
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0) # Reset pointer to start
        
        conversion_time = time.time()
        print(f"[{conversion_time}] Audio conversion took: {conversion_time - start_time:.2f}s")

        r = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            # record the audio data from the file
            audio_data = r.record(source)
            
            rec_start_time = time.time()
            print(f"[{rec_start_time}] Sending to Google API...")
            
            # recognize speech using Google Speech Recognition
            text = r.recognize_google(audio_data, language=language)
            
            end_time = time.time()
            print(f"[{end_time}] Recognition took: {end_time - rec_start_time:.2f}s. Total: {end_time - start_time:.2f}s")
            
            return text
            
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except Exception as e:
        print(f"Error in transcription: {e}")
        return None
