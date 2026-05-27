"""
Speech Recognition Module
Handles voice input and audio processing
"""

import speech_recognition as sr
import threading
from typing import Callable, Optional

class SpeechRecognizer:
    """Handles speech recognition with threading"""
    
    def __init__(self, language: str = "tr-TR"):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.language = language
        self.is_listening = False
        self.recognition_thread: Optional[threading.Thread] = None
    
    def start_listening(self, callback: Callable[[str], None], error_callback: Callable[[str], None] = None):
        """Start listening in a separate thread"""
        if self.is_listening:
            return
        
        self.is_listening = True
        self.recognition_thread = threading.Thread(
            target=self._listen,
            args=(callback, error_callback),
            daemon=True
        )
        self.recognition_thread.start()
    
    def _listen(self, callback: Callable[[str], None], error_callback: Optional[Callable[[str], None]]):
        """Listen for audio input"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            try:
                text = self.recognizer.recognize_google(audio, language=self.language)
                callback(text)
            except sr.UnknownValueError:
                if error_callback:
                    error_callback("Ses tanınamadı. Lütfen tekrar deneyin.")
            except sr.RequestError as e:
                if error_callback:
                    error_callback(f"API hatası: {str(e)}")
        except sr.RequestError as e:
            if error_callback:
                error_callback(f"Mikrofon hatası: {str(e)}")
        finally:
            self.is_listening = False
    
    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False

# Global recognizer instance
recognizer = SpeechRecognizer()
