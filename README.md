# 🐱 Siya - Your AI Cat Assistant

Siya is an interactive AI assistant with a fun cartoon cat UI! It combines voice recognition, text-to-speech, and OpenAI's GPT models to create an engaging conversational experience.

## ✨ Features

- 🎨 **Animated Cat UI**: Beautiful cartoon cat interface that changes expressions based on activity
- 🎤 **Voice Input**: Speak naturally to Siya with voice recognition
- 💬 **Text-to-Speech**: Siya speaks responses back to you
- ⌨️ **Text Input**: Type messages if you prefer not to use voice
- 🧠 **AI-Powered**: Uses OpenAI's GPT models for intelligent responses
- 🎭 **Cat Personality**: Friendly assistant with a playful cat theme

## 🎯 Two Versions Available

### Basic Version (`siya.py`)
Simple chat interface with voice and text input

### Advanced Version (`siya_advanced.py`) ⭐ RECOMMENDED
- Everything from basic version
- **Task Management** with dedicated Tasks tab
- Enhanced UI with tabbed interface
- Task persistence (saves to JSON file)
- Better visual organization

## 🚀 Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your OpenAI API key**:
   - Create a `.env` file in the project directory
   - Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## 🎮 Usage

**Basic Version:**
```bash
python siya.py
```

**Advanced Version (Recommended):**
```bash
python siya_advanced.py
```

Or simply double-click `run_siya.bat`

### Interaction Methods

1. **Voice Input**: 
   - Click the "🎤 Hold to Speak" button
   - Speak your question or command
   - Siya will transcribe, respond, and speak back!

2. **Text Input**:
   - Click the "⌨️ Type Message" button
   - Type your message and press Enter or click Send

### Cat Expressions

- 😺 **Idle**: Ready and waiting
- 👂 **Listening**: Recording your voice
- 🤔 **Thinking**: Processing your request
- 💬 **Speaking**: Delivering the response

### Task Management (Advanced Version Only)

Siya can help you stay organized!

**Voice Commands:**
- "Add task buy groceries"
- "Remind me to call mom"
- "Create task finish homework"

**Or use the Tasks tab:**
1. Click the "✅ Tasks" tab
2. Type your task and click "Add Task"
3. Mark tasks complete when done

All tasks are saved automatically!

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Microphone (for voice input)
- Speakers (for voice output)

## 🛠️ Technical Stack

- **GUI**: tkinter (Python's built-in GUI library)
- **Voice Recognition**: OpenAI Whisper API
- **AI Brain**: OpenAI GPT-4o-mini
- **Text-to-Speech**: pyttsx3
- **Audio Recording**: sounddevice + scipy

## 🎨 Customization

You can customize Siya's:
- **Personality**: Edit the system prompt in the `ask_siya()` function
- **Colors**: Modify the color codes in `SiyaCatUI.__init__()`
- **Cat Drawings**: Update the ASCII art in the `draw_cat_*()` methods
- **Voice**: Adjust the TTS settings in `__init__()` method

## 📝 Notes

- Default recording time is 5 seconds per voice input
- The app requires an active internet connection for OpenAI API calls
- Voice output quality depends on your system's TTS engine

## 🐾 Future Enhancements

- [ ] Task scheduling and reminders
- [ ] File operations support
- [ ] Multi-language support
- [ ] Custom wake words
- [ ] Chat history saving
- [ ] More cat animations

## 📄 License

This project is open source and available for personal use.

---

Made with ❤️ and 🐱 by Pratik
