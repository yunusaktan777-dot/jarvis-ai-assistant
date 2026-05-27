"""
Main GUI Window
Professional UI for JARVIS AI Assistant
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QPushButton, QLabel,
    QLineEdit, QSpinBox, QSlider, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import sys

from core.chatgpt import chatgpt
from core.speech_recognition import recognizer
from core.text_to_speech import tts
from core.system_commands import system_commands
from core.config import config

class ChatThread(QThread):
    """Thread for ChatGPT communication"""
    response_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, message: str):
        super().__init__()
        self.message = message
    
    def run(self):
        try:
            response = chatgpt.send_message(self.message)
            self.response_signal.emit(response)
            tts.speak(response)
        except Exception as e:
            self.error_signal.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.chat_thread = None
        self.init_ui()
        self.apply_theme()
        
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("J.A.R.V.I.S - AI Assistant")
        self.setGeometry(100, 100, 1200, 700)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Tab Widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Chat Tab
        self.chat_tab = self.create_chat_tab()
        tabs.addTab(self.chat_tab, "💬 Chat")
        
        # Settings Tab
        self.settings_tab = self.create_settings_tab()
        tabs.addTab(self.settings_tab, "⚙️ Settings")
        
        # System Tab
        self.system_tab = self.create_system_tab()
        tabs.addTab(self.system_tab, "🖥️ System")
    
    def create_chat_tab(self) -> QWidget:
        """Create chat interface"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Chat history
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: Consolas, Courier;
                font-size: 12px;
                border: 1px solid #333333;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(QLabel("📝 Conversation History:"))
        layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Write your message here or use voice command...")
        self.chat_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.chat_input)
        
        # Send Button
        send_btn = QPushButton("📤 Send")
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)
        
        # Voice Button
        voice_btn = QPushButton("🎤 Voice")
        voice_btn.clicked.connect(self.start_voice_input)
        input_layout.addWidget(voice_btn)
        
        layout.addLayout(input_layout)
        
        # Clear Button
        clear_btn = QPushButton("🗑️ Clear History")
        clear_btn.clicked.connect(self.clear_chat)
        layout.addWidget(clear_btn)
        
        return widget
    
    def create_settings_tab(self) -> QWidget:
        """Create settings interface"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # API Key Section
        layout.addWidget(QLabel("🔑 API Configuration"))
        api_layout = QHBoxLayout()
        api_label = QLabel("OpenAI API Key:")
        self.api_input = QLineEdit()
        self.api_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_input)
        
        api_btn = QPushButton("💾 Save API Key")
        api_btn.clicked.connect(self.save_api_key)
        api_layout.addWidget(api_btn)
        layout.addLayout(api_layout)
        
        layout.addWidget(QLabel("📌 Get your API key from: https://platform.openai.com/api-keys"))
        
        # Voice Settings
        layout.addWidget(QLabel("🎙️ Voice Settings"))
        
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Volume:"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(config.get("volume", 80))
        self.volume_label = QLabel(f"{config.get('volume', 80)}%")
        self.volume_slider.valueChanged.connect(self.update_volume)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_label)
        layout.addLayout(volume_layout)
        
        # Speech Rate
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("Speech Rate:"))
        self.rate_spinbox = QSpinBox()
        self.rate_spinbox.setMinimum(50)
        self.rate_spinbox.setMaximum(200)
        self.rate_spinbox.setValue(int(config.get("speech_rate", 1.0) * 100))
        self.rate_spinbox.setSuffix("%")
        self.rate_spinbox.valueChanged.connect(self.update_rate)
        rate_layout.addWidget(self.rate_spinbox)
        layout.addLayout(rate_layout)
        
        # Model Selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("AI Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"])
        self.model_combo.setCurrentText(config.get("model", "gpt-3.5-turbo"))
        self.model_combo.currentTextChanged.connect(self.update_model)
        model_layout.addWidget(self.model_combo)
        layout.addLayout(model_layout)
        
        layout.addStretch()
        return widget
    
    def create_system_tab(self) -> QWidget:
        """Create system information tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("🖥️ System Information"))
        
        self.system_info = QTextEdit()
        self.system_info.setReadOnly(True)
        layout.addWidget(self.system_info)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.update_system_info)
        layout.addWidget(refresh_btn)
        
        self.update_system_info()
        return widget
    
    def send_message(self):
        """Send message to ChatGPT"""
        message = self.chat_input.text().strip()
        if not message:
            return
        
        if not config.get("api_key"):
            QMessageBox.warning(self, "Error", "Please set your API key in settings first!")
            return
        
        # Add to display
        self.chat_display.append(f"👤 You: {message}\n")
        self.chat_input.clear()
        
        # Send in thread
        self.chat_thread = ChatThread(message)
        self.chat_thread.response_signal.connect(self.display_response)
        self.chat_thread.error_signal.connect(self.display_error)
        self.chat_thread.start()
    
    def display_response(self, response: str):
        """Display ChatGPT response"""
        self.chat_display.append(f"🤖 JARVIS: {response}\n")
    
    def display_error(self, error: str):
        """Display error message"""
        self.chat_display.append(f"❌ Error: {error}\n")
        QMessageBox.critical(self, "Error", error)
    
    def start_voice_input(self):
        """Start voice recognition"""
        self.chat_display.append("🎤 Listening...\n")
        recognizer.start_listening(
            callback=self.on_voice_recognized,
            error_callback=self.on_voice_error
        )
    
    def on_voice_recognized(self, text: str):
        """Handle recognized voice"""
        self.chat_input.setText(text)
        self.send_message()
    
    def on_voice_error(self, error: str):
        """Handle voice recognition error"""
        self.chat_display.append(f"❌ Voice Error: {error}\n")
    
    def clear_chat(self):
        """Clear chat history"""
        reply = QMessageBox.question(
            self, "Clear History",
            "Are you sure you want to clear chat history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.chat_display.clear()
            chatgpt.clear_history()
    
    def save_api_key(self):
        """Save API key"""
        api_key = self.api_input.text().strip()
        if not api_key or len(api_key) < 20:
            QMessageBox.warning(self, "Error", "Please enter a valid API key!")
            return
        
        chatgpt.set_api_key(api_key)
        QMessageBox.information(self, "Success", "API key saved successfully!")
    
    def update_volume(self, value):
        """Update volume"""
        self.volume_label.setText(f"{value}%")
        tts.set_volume(value)
        config.set("volume", value)
    
    def update_rate(self, value):
        """Update speech rate"""
        rate = value / 100.0
        tts.set_rate(rate)
        config.set("speech_rate", rate)
    
    def update_model(self, model):
        """Update AI model"""
        config.set("model", model)
    
    def update_system_info(self):
        """Update system information"""
        info = system_commands.get_system_info()
        text = f"""
System Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OS: {info['os']}
CPU Cores: {info['cpu_count']}
CPU Usage: {info['cpu_percent']}%
Memory: {info['memory_percent']}%
Disk: {info['disk_percent']}%
Total Memory: {info['total_memory']}
        """
        self.system_info.setText(text)
    
    def apply_theme(self):
        """Apply dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1117;
            }
            QWidget {
                background-color: #0d1117;
                color: #c9d1d9;
            }
            QTabWidget::pane {
                border: 1px solid #30363d;
            }
            QTabBar::tab {
                background-color: #161b22;
                color: #8b949e;
                padding: 8px 20px;
                border: none;
                border-bottom: 2px solid transparent;
            }
            QTabBar::tab:selected {
                background-color: #0d1117;
                color: #58a6ff;
                border-bottom: 2px solid #58a6ff;
            }
            QPushButton {
                background-color: #238636;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
            QPushButton:pressed {
                background-color: #1f6feb;
            }
            QLineEdit, QTextEdit, QSpinBox, QComboBox {
                background-color: #0d1117;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 8px;
            }
            QSlider::groove:horizontal {
                background: #30363d;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #58a6ff;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)
