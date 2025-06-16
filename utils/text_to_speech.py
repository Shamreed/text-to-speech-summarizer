from gtts import gTTS
import os

class TextToSpeech:
    def __init__(self, lang="en", slow=False):
        self.lang = lang
        self.slow = slow

    def convert_to_speech(self, text, output_path="output/summary_audio.mp3"):
        tts = gTTS(text=text, lang=self.lang, slow=self.slow)
        tts.save(output_path)
        print(f"Audio saved as {output_path}")
