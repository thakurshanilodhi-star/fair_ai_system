import os
from gtts import gTTS
import tempfile

def speak(text):
    try:
        tts = gTTS(text=text, lang='en')

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)

        os.system(f"start {temp_file.name}")

    except Exception as e:
        print("Voice Error:", e)