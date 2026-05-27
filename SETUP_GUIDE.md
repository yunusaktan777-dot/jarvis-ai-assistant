## JARVIS AI Assistant - Complete Setup Guide

### 📋 System Requirements

- **Python:** 3.9 or higher
- **OS:** Windows 10+, macOS 10.12+, or Linux (Ubuntu 18.04+)
- **RAM:** 2GB minimum
- **Disk Space:** 500MB
- **Microphone:** Required for voice input

### 🚀 Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/yunusaktan777-dot/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Get OpenAI API Key

1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Create a new API key
4. Copy the key (you'll need it in the app)

#### 5. Run JARVIS

```bash
python main.py
```

### ⚙️ Configuration

**First Launch:**
1. Go to the **Settings** tab (⚙️)
2. Paste your OpenAI API Key in the "OpenAI API Key" field
3. Click **"💾 Save API Key"**
4. The app will confirm success

**Voice Settings:**
- **Volume:** Adjust speaker volume (0-100%)
- **Speech Rate:** Control voice speed (50-200%)
- **AI Model:** Choose between GPT-3.5, GPT-4, or GPT-4 Turbo

### 💬 How to Use

**Text Chat:**
1. Type your message in the input field
2. Press Enter or click **📤 Send**
3. JARVIS responds with text and voice

**Voice Command:**
1. Click **🎤 Voice** button
2. Speak clearly into your microphone
3. Wait for recognition to complete
4. JARVIS processes and responds

**Keyboard Shortcut:**
- Press `Ctrl + Alt + J` to activate voice input

### 🖥️ System Information Tab

View real-time system metrics:
- CPU Usage
- Memory Usage
- Disk Usage
- OS Information
- CPU Cores

### 📁 File Structure

```
jarvis-ai-assistant/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── core/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── chatgpt.py         # AI communication
│   ├── speech_recognition.py  # Voice input
│   ├── text_to_speech.py  # Voice output
│   └── system_commands.py # System operations
├── gui/
│   ├── __init__.py
│   └── main_window.py     # GUI interface
└── README.md              # Documentation
```

### 🔐 Security

- API keys are **encrypted locally** using Fernet encryption
- Configuration stored in `~/.jarvis/` directory
- Encryption keys are generated automatically on first run

### ⚡ Performance Tips

1. **Faster Responses:**
   - Use GPT-3.5-turbo for quick answers (cheaper)
   - Use GPT-4 for complex tasks

2. **Better Voice Recognition:**
   - Speak clearly
   - Reduce background noise
   - Use microphone 15-30cm away

3. **Smooth Operation:**
   - Keep system RAM available
   - Close unnecessary applications
   - Ensure stable internet connection

### 🐛 Troubleshooting

**API Key Error:**
- ❌ Invalid API key format
- ✅ Ensure key starts with `sk-`
- ✅ Check OpenAI account has available credits

**Microphone Not Working:**
- ❌ Check microphone is connected
- ✅ Test microphone in Windows/Mac settings
- ✅ Restart the application

**No Voice Output:**
- ❌ Check volume settings in GUI
- ✅ Test speakers/headphones
- ✅ Check system volume

**Slow Responses:**
- ❌ Poor internet connection
- ❌ OpenAI API rate limit
- ✅ Wait a few seconds and try again

### 📚 API Pricing

- **GPT-3.5-turbo:** ~$0.0005 per 1K tokens
- **GPT-4:** ~$0.03 per 1K tokens
- **GPT-4-turbo:** ~$0.01 per 1K tokens

[Check current pricing](https://openai.com/pricing)

### 🔗 Useful Links

- [OpenAI API Docs](https://platform.openai.com/docs)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [OpenAI Pricing](https://openai.com/pricing)
- [GitHub Repository](https://github.com/yunusaktan777-dot/jarvis-ai-assistant)

### 💡 Tips & Tricks

**Save API Key Securely:**
```bash
# The app automatically encrypts your API key
# Check ~/.jarvis/config.json (encrypted)
```

**Clear Chat History:**
- Click **🗑️ Clear History** button in Chat tab
- Conversation context will be reset

**Modify Settings:**
- All settings auto-save in `~/.jarvis/config.json`

### 🤝 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify your API key
3. Check internet connection
4. Open an issue on [GitHub](https://github.com/yunusaktan777-dot/jarvis-ai-assistant/issues)

### 📜 License

MIT License - See LICENSE file for details

---

**Happy chatting with JARVIS! 🤖**
