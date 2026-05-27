"""
ChatGPT AI Module
Handles communication with OpenAI API
"""

import openai
from typing import Optional, List, Dict
from core.config import config

class ChatGPT:
    """ChatGPT interface for conversations"""
    
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self._setup_api()
    
    def _setup_api(self):
        """Setup OpenAI API"""
        api_key = config.get("api_key")
        if api_key:
            if config.get("api_key_encrypted"):
                api_key = config.decrypt_api_key(api_key)
            openai.api_key = api_key
    
    def set_api_key(self, api_key: str, encrypt: bool = True):
        """Set API key"""
        if encrypt:
            encrypted_key = config.encrypt_api_key(api_key)
            config.set("api_key", encrypted_key)
            config.set("api_key_encrypted", True)
        else:
            config.set("api_key", api_key)
            config.set("api_key_encrypted", False)
        
        openai.api_key = api_key
    
    def send_message(self, user_message: str) -> Optional[str]:
        """Send message to ChatGPT"""
        try:
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            response = openai.ChatCompletion.create(
                model=config.get("model", "gpt-3.5-turbo"),
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        
        except openai.error.AuthenticationError:
            return "API Key hatası: Geçersiz API anahtarı."
        except openai.error.RateLimitError:
            return "Hız sınırı aşıldı. Lütfen sonra tekrar deneyin."
        except Exception as e:
            return f"Hata: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history

# Global ChatGPT instance
chatgpt = ChatGPT()
