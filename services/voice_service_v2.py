import edge_tts
import asyncio
import os
import nest_asyncio
import tempfile

VOICE = "te-IN-MohanNeural"

async def generate_voice_file(text: str, output_file: str):
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_file)
        return output_file
    except Exception:
        return None

def get_voice_audio(text: str):
    nest_asyncio.apply()
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_filename = tmp_file.name
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(generate_voice_file(text, tmp_filename))
        
        if os.path.exists(tmp_filename):
            with open(tmp_filename, "rb") as f:
                data = f.read()
            return data
        return None
    finally:
        # Cleanup
        if os.path.exists(tmp_filename):
            try:
                os.remove(tmp_filename)
            except:
                pass
