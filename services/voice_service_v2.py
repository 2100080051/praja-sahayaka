import edge_tts
import asyncio
import os
import nest_asyncio

VOICE = "te-IN-MohanNeural"

async def generate_voice_file(text: str, output_file: str = "temp_output.mp3"):
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_file)
        return output_file
    except Exception:
        return None

def get_voice_audio(text: str):
    nest_asyncio.apply()
    
    filename = "response_audio.mp3"
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_voice_file(text, filename))
    
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            data = f.read()
        return data
    return None
