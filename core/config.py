"""
Configuration Management for JARVIS
Handles settings, encryption, and storage
"""

import json
import os
from pathlib import Path
from cryptography.fernet import Fernet
from typing import Any, Dict

class Config:
    """Configuration handler with encryption support"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".jarvis"
        self.config_file = self.config_dir / "config.json"
        self.key_file = self.config_dir / "key.key"
        
        self.config_dir.mkdir(exist_ok=True)
        self._init_encryption()
        self.settings = self._load_config()
    
    def _init_encryption(self):
        """Initialize encryption key"""
        if not self.key_file.exists():
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        
        with open(self.key_file, 'rb') as f:
            self.cipher = Fernet(f.read())
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "api_key": "",
            "api_key_encrypted": False,
            "voice_engine": "pyttsx3",
            "speech_lang": "tr-TR",
            "tts_lang": "tr",
            "auto_start": False,
            "theme": "dark",
            "volume": 80,
            "speech_rate": 1.0,
            "model": "gpt-3.5-turbo"
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def encrypt_api_key(self, api_key: str) -> str:
        """Encrypt API key"""
        try:
            encrypted = self.cipher.encrypt(api_key.encode())
            return encrypted.decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return api_key
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """Decrypt API key"""
        try:
            decrypted = self.cipher.decrypt(encrypted_key.encode())
            return decrypted.decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return encrypted_key
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.settings[key] = value
        self.save_config()

# Global config instance
config = Config()
