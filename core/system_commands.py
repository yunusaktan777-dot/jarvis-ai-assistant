"""
System Commands Module
Handles system operations and commands
"""

import subprocess
import psutil
import webbrowser
import os
from typing import Dict, Any
from platform import system

class SystemCommands:
    """Handle system commands and operations"""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get system information"""
        return {
            "os": system(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent,
            "cpu_count": psutil.cpu_count(),
            "total_memory": f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
        }
    
    @staticmethod
    def open_application(app_name: str) -> str:
        """Open an application"""
        try:
            if system() == "Windows":
                os.startfile(app_name)
            else:
                subprocess.Popen([app_name])
            return f"{app_name} açılıyor..."
        except Exception as e:
            return f"Uygulama açılamadı: {str(e)}"
    
    @staticmethod
    def open_browser(url: str) -> str:
        """Open URL in browser"""
        try:
            webbrowser.open(url)
            return f"Tarayıcı açılıyor: {url}"
        except Exception as e:
            return f"Tarayıcı açılamadı: {str(e)}"
    
    @staticmethod
    def get_running_processes() -> list:
        """Get list of running processes"""
        try:
            return [p.info for p in psutil.process_iter(['pid', 'name'])][:10]
        except Exception as e:
            return []
    
    @staticmethod
    def execute_command(command: str) -> str:
        """Execute system command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            return result.stdout if result.stdout else result.stderr
        except subprocess.TimeoutExpired:
            return "Komut zaman aşımına uğradı."
        except Exception as e:
            return f"Komut hatası: {str(e)}"

# Global instance
system_commands = SystemCommands()
