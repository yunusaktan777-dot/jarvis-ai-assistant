"""
Text-to-Speech Module
Handles voice output and audio synthesis
"""

import pyttsx3
import threading
from typing import Optional

class TextToSpeech:
    """Handles text-to-speech conversion"""
    
    def __init__(self, language: str = "tr", rate: float = 1.0, volume: int = 80):
        self.engine = pyttsx3.init()
        self.language = language
        self.rate = rate
        self.volume = volume
        self.is_speaking = False
        self.speech_thread: Optional[threading.Thread] = None
        
        self._configure_engine()
    
    def _configure_engine(self):
        """Configure TTS engine"""
        self.engine.setProperty('rate', 150 * self.rate)
        self.engine.setProperty('volume', self.volume / 100)
    
    def speak(self, text: str, wait: bool = False):
        """Speak text"""
        if self.is_speaking and not wait:
            return
        
        if wait:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            self.speech_thread = threading.Thread(
                target=self._speak_async,
                args=(text,),
                daemon=True
            )
            self.speech_thread.start()
    
    def _speak_async(self, text: str):
        """Speak text asynchronously"""
        try:
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
        finally:
            self.is_speaking = False
    
    def set_rate(self, rate: float):
        """Set speech rate"""
        self.rate = rate
        self.engine.setProperty('rate', 150 * rate)
    
    def set_volume(self, volume: int):
        """Set volume (0-100)"""
        self.volume = max(0, min(100, volume))
        self.engine.setProperty('volume', self.volume / 100)
    
    def stop(self):
        """Stop speaking"""
        self.engine.stop()
        self.is_speaking = False

# Global TTS instance
tts = TextToSpeech()
