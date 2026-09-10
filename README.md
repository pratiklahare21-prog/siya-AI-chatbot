# 😺 Siya - Your FREE AI Cat Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-yellow)
![Status](https://img.shields.io/badge/status-active-success)

**A beautiful, interactive AI assistant with a playful cat personality - 100% FREE!**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [FAQ](#-faq)

</div>

---

## 🌟 Features

### 💬 **Smart AI Conversations**
- Powered by **FREE** AI engines (Ollama or Groq)
- Natural, friendly, and helpful responses
- Cat-themed personality 🐱

### 😺 **Animated Emoji Cat**
- **9 different expressions** that react to your interactions
- **120pt emoji** - huge and adorable!
- Real-time mood changes based on activity

### ✅ **Task Management**
- Add tasks via text commands
- Visual task list with one-click completion
- Automatic saving between sessions

### 🎨 **Beautiful Modern UI**
- Dark theme design (easy on the eyes)
- Tabbed interface (Chat, Tasks, Settings)
- Smooth animations and transitions
- Professional appearance

### 🆓 **100% FREE Forever**
- **No API costs** - zero subscription fees
- **Two free options**: Ollama (local) or Groq (cloud)
- **Unlimited usage** with Ollama
- **14,400 requests/day** with Groq (more than enough!)

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [AI Engine Options](#-ai-engine-options)
  - [Option 1: Ollama (Recommended)](#option-1-ollama-recommended)
  - [Option 2: Groq API](#option-2-groq-api)
- [Usage Guide](#-usage-guide)
- [Emoji Cat Guide](#-emoji-cat-guide)
- [Task Management](#-task-management)
- [Settings](#️-settings)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Installation

### Prerequisites
- **Python 3.8+** installed
- **Windows 10/11** (for best emoji support)
- Internet connection (for initial setup)

### Step 1: Clone or Download
```bash
git clone https://github.com/yourusername/siya.git
cd siya
```

### Step 2: Install Dependencies
```bash
# Using the installer (Windows)
install.bat

# OR manually
pip install -r requirements.txt
```

### Step 3: Choose Your AI Engine
See [AI Engine Options](#-ai-engine-options) below

---

## ⚡ Quick Start

### Super Fast Launch

**Option 1: Use the Launcher**
```bash
# Double-click this file
LAUNCHER.bat

# Then choose:
# 1 = FREE version (recommended)
# 2 = Advanced version (needs OpenAI credits)
# 3 = Basic version (needs OpenAI credits)
```

**Option 2: Direct Launch**
```bash
# Run the FREE version directly
python siya_free.py

# OR double-click
run_siya_free.bat
```

### First Run Setup

When you first run Siya, you'll see a **welcome screen** with two options:

1. **Ollama (Local)** - Best for privacy and unlimited use
2. **Groq API (Cloud)** - Best for quick setup

Choose one and follow the on-screen instructions!

---

## 🤖 AI Engine Options

### Option 1: Ollama (Recommended)

**Why Choose Ollama?**
- ✅ **100% FREE** forever
- ✅ **Private** - Runs on your PC
- ✅ **No internet** needed after setup
- ✅ **Unlimited** usage
- ✅ **Fast** responses

**Setup Steps:**

1. **Install Ollama**
   - Visit: https://ollama.com
   - Download for Windows
   - Install (takes 2 minutes)

2. **Download AI Model**
   ```bash
   # Open Command Prompt or PowerShell
   ollama run llama2
   
   # This will download ~4GB
   # Wait for it to complete
   ```

3. **Run Siya**
   ```bash
   python siya_free.py
   ```

4. **Choose Ollama in Welcome Screen**
   - Select "Option 1: Ollama"
   - Choose your model (llama2 recommended)
   - Click "Save & Start Siya"

**Available Models:**
- `llama2` (4GB) - Recommended, great balance
- `mistral` (4GB) - Fast and efficient
- `tinyllama` (600MB) - Very fast, lighter responses
- `llama2:13b` (7GB) - Better quality
- `llama2:70b` (40GB) - Best quality (needs powerful PC)

**Model Commands:**
```bash
# List installed models
ollama list

# Download a specific model
ollama pull mistral

# Switch models (in Settings tab)
```

---

### Option 2: Groq API

**Why Choose Groq?**
- ✅ **100% FREE** (no credit card!)
- ✅ **Quick setup** (5 minutes)
- ✅ **No downloads** required
- ✅ **Cloud-based** reliability
- ✅ **14,400 requests/day** limit (very generous)

**Setup Steps:**

1. **Get Free API Key**
   - Visit: https://console.groq.com
   - Sign up (FREE, no credit card needed)
   - Go to "API Keys" section
   - Click "Create API Key"
   - Copy your key (starts with `gsk_`)

2. **Run Siya**
   ```bash
   python siya_free.py
   ```

3. **Choose Groq in Welcome Screen**
   - Select "Option 2: Groq API"
   - Paste your API key
   - Click "Save & Start Siya"

**API Key Format:**
```
gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Daily Limits:**
- 14,400 requests per day
- ~600 requests per hour
- More than enough for personal use!

---

## 📖 Usage Guide

### Main Interface

```
┌─────────────────────────────────────┐
│  [💬 Chat] [✅ Tasks] [⚙️ Settings] │  ← Tabs
├─────────────────────────────────────┤
│                                     │
│              😺                     │  ← Animated Cat (120pt)
│         (HUGE EMOJI)                │
│                                     │
│     😺 Ready to help!               │  ← Status
├─────────────────────────────────────┤
│  💬 Conversation                    │
│  ┌───────────────────────────────┐ │
│  │ Chat messages appear here...  │ │
│  │ [Time] 👤 You: Hello!         │ │
│  │ [Time] 🐱 Siya: Hi there!     │ │
│  │                               │ │
│  └───────────────────────────────┘ │
├─────────────────────────────────────┤
│  [⌨️ Type Message]  [🗑️ Clear]     │
└─────────────────────────────────────┘
```

### Chat Tab

**How to Chat:**
1. Click "⌨️ Type Message" button
2. Type your question or message
3. Press Enter or click "Send"
4. Watch the cat react!
5. Get intelligent responses

**Example Conversations:**
```
You: What's 156 times 23?
Siya: 3,588! Need help with anything else? 🐱

You: Explain recursion in simple terms
Siya: Recursion is when a function calls itself...

You: Tell me a joke
Siya: Why don't cats play poker? Too many cheetahs! 😹
```

### Tasks Tab

**Adding Tasks:**

**Method 1: Via Chat**
```
Type: "add task buy groceries"
Type: "remind me to exercise"
Type: "create task finish homework"
```

**Method 2: Via Tasks Tab**
1. Click "✅ Tasks" tab
2. Type task in input field
3. Press Enter or click "+ Add Task"

**Managing Tasks:**
- View all pending tasks in list
- Click "✓ Done" to complete
- Tasks save automatically
- Persist between sessions

### Settings Tab

**What You Can Change:**
- Switch between Ollama and Groq
- Update API key (for Groq)
- Change Ollama model
- View app information

**To Change AI Engine:**
1. Go to "⚙️ Settings" tab
2. Click "Change AI Engine"
3. Choose new option
4. Follow setup steps

---

## 😺 Emoji Cat Guide

### All 9 Expressions

| Emoji | Name | When It Appears |
|-------|------|-----------------|
| 😺 | Happy Cat | Idle, ready to chat |
| 😸 | Grinning Cat | Excited (you're typing) |
| 🤔 | Thinking Face | Processing your message |
| 😻 | Heart Eyes Cat | Responding to you |
| 😹 | Laughing Cat | Task added successfully |
| 😽 | Kissing Cat | Task completed |
| 😿 | Crying Cat | Connection problems |
| 🙀 | Surprised Cat | Error occurred |
| 😾 | Grumpy Cat | Reserved for future |

### Expression Flow

**Normal Chat:**
```
Start: 😺 (idle)
  ↓
You type: 😸 (excited)
  ↓
You send: 🤔 (thinking)
  ↓
Siya responds: 😻 (speaking)
  ↓
Wait 3 sec: 😺 (back to idle)
```

**Adding Task:**
```
Command: "add task..."
  ↓
Processing: 🤔 (thinking)
  ↓
Task added: 😹 (joy!)
  ↓
Wait 2 sec: 😺 (idle)
```

**Completing Task:**
```
Click "✓ Done"
  ↓
Completed: 😽 (loving)
  ↓
Wait 2 sec: 😺 (idle)
```

---

## 💡 Task Management

### Task Features

- **Create**: Add tasks via chat or Tasks tab
- **View**: See all pending tasks in organized list
- **Complete**: One-click task completion
- **Persist**: Tasks save automatically to JSON
- **Track**: Each task has unique ID and timestamp

### Task Commands

**In Chat:**
```
"add task buy milk"
"remind me to call mom"
"create task study for exam"
"new task workout at gym"
```

**Voice-like Commands:**
```
"remind me to [task]"
"don't forget to [task]"
"I need to [task]"
```

### Task Storage

Tasks are saved in: `siya_tasks.json`

**Format:**
```json
{
  "id": 1,
  "description": "Buy groceries",
  "created": "2024-01-15T10:30:00",
  "completed": false
}
```

---

## ⚙️ Settings

### Configuration File

Settings are stored in: `siya_config.json`

**Default Configuration:**
```json
{
  "use_local_ai": true,
  "groq_api_key": "",
  "ollama_model": "llama2",
  "ollama_url": "http://localhost:11434"
}
```

### Changing Settings

**Via Settings Tab:**
1. Click "⚙️ Settings"
2. View current configuration
3. Click "Change AI Engine" to switch
4. Or update API key directly

**Manual Edit:**
You can also edit `siya_config.json` directly

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Issue: "Couldn't connect to my brain"
**Cause:** Ollama not running  
**Solution:**
```bash
# Start Ollama
ollama serve

# Or run the model
ollama run llama2
```

#### Issue: "API error 401"
**Cause:** Invalid Groq API key  
**Solution:**
1. Go to Settings tab
2. Update API key
3. Make sure it starts with `gsk_`
4. Get new key at: https://console.groq.com

#### Issue: "No module named 'tkinter'"
**Cause:** Tkinter not installed  
**Solution:**
```bash
# Windows (reinstall Python with tcl/tk)
# Or use Python from python.org

# Linux
sudo apt-get install python3-tk
```

#### Issue: Emoji shows as boxes
**Cause:** Old Windows or missing fonts  
**Solution:**
- Update to Windows 10/11
- Or install emoji fonts
- App still works, just visual issue

#### Issue: "Module not found" errors
**Cause:** Dependencies not installed  
**Solution:**
```bash
pip install -r requirements.txt
# Or run install.bat
```

#### Issue: Ollama model not found
**Cause:** Model not downloaded  
**Solution:**
```bash
# Download the model
ollama pull llama2

# Or run directly (auto-downloads)
ollama run llama2
```

---

## ❓ FAQ

### General Questions

**Q: Is Siya really 100% free?**  
A: Yes! Both Ollama and Groq are completely free. No hidden costs, no subscriptions, no credit card needed.

**Q: Which AI engine should I use?**  
A: **Ollama** for privacy and unlimited use. **Groq** for quick setup and cloud reliability.

**Q: Can I switch between engines later?**  
A: Yes! Go to Settings → Change AI Engine.

**Q: Does it work offline?**  
A: With Ollama, yes (after initial model download). With Groq, internet required.

### Technical Questions

**Q: What Python version do I need?**  
A: Python 3.8 or higher.

**Q: How much disk space does Ollama need?**  
A: 
- llama2: ~4GB
- mistral: ~4GB
- tinyllama: ~600MB
- Plus ~1GB for Ollama itself

**Q: Are my conversations private?**  
A: With Ollama, 100% private (runs locally). With Groq, conversations go to their servers.

**Q: Can I use my own OpenAI key?**  
A: Not in this free version, but you can use `siya_advanced.py` for OpenAI support.

### Feature Questions

**Q: Why no voice input?**  
A: Voice transcription requires paid APIs. We removed it to keep Siya 100% free.

**Q: Can I add voice back?**  
A: Yes, but you'll need OpenAI credits. Check `siya_advanced.py` for the original version.

**Q: How many tasks can I add?**  
A: Unlimited! They're stored locally in JSON.

**Q: Can I export my chat history?**  
A: Not currently, but you can add this feature (see Contributing).

---

## 🎯 Use Cases

### For Students
- Homework help and explanations
- Study planning with tasks
- Quick calculations and research
- Writing assistance

### For Developers
- Code debugging help
- Algorithm explanations
- Task tracking for projects
- Quick reference lookups

### For Professionals
- Daily task management
- Quick information lookup
- Email/document drafting
- Meeting reminders

### For Everyone
- General questions and answers
- Entertainment (jokes, stories)
- Learning new topics
- Staying organized

---

## 📊 Comparison Table

| Feature | Siya FREE | ChatGPT | Other AI |
|---------|-----------|---------|----------|
| Cost | $0 | $20/mo | Varies |
| Privacy | High (Ollama) | Low | Varies |
| Offline | Yes (Ollama) | No | No |
| Limits | None (Ollama) | Yes | Yes |
| Setup | 10 min | Instant | Varies |
| Tasks | Built-in | No | Varies |
| Cat | Yes! 😺 | No | No |

---

## 🎨 Customization

### Change Cat Personality

Edit `siya_free.py`, find `ask_siya_free()` function:

```python
"content": "You are Siya, a helpful AI cat assistant..."
# Change this to customize personality!
```

### Change Colors

Find these color codes in `setup_ui()`:

```python
bg="#1a1a2e"  # Main background
fg="#00d4ff"  # Accent color (cyan)
fg="#00ff88"  # Success color (green)
```

### Add Custom Emoji

In `set_cat_mood()`, add your own:

```python
moods = {
    "happy": "😺",
    "custom": "🦁",  # Add new expressions!
}
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Ways to Contribute

1. **Report Bugs**: Open an issue
2. **Suggest Features**: Open an issue with "Feature Request"
3. **Submit Code**: Fork, code, PR
4. **Improve Docs**: Fix typos, add examples
5. **Share**: Tell others about Siya!

### Development Setup

```bash
git clone https://github.com/yourusername/siya.git
cd siya
pip install -r requirements.txt
python siya_free.py
```

### Code Style

- Follow PEP 8
- Add comments for complex logic
- Update README for new features

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **Ollama** - For free local AI
- **Groq** - For free cloud AI
- **Python** - For being awesome
- **You** - For using Siya! 😺

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/siya/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/siya/discussions)
- **Email**: your.email@example.com

---

## 🎉 Final Notes

Siya is built with ❤️ to provide a FREE, private, and fun AI assistant experience.

**Key Points:**
- 🆓 100% FREE forever
- 😺 Fun and engaging
- ✅ Actually useful
- 🔒 Private option available
- 🚀 Easy to use

**Get Started:**
```bash
python siya_free.py
```

**Enjoy your FREE AI cat assistant! 😺✨**

---

<div align="center">

Made with ❤️ and 🐱 | © 2024 Siya Project

[⬆ Back to Top](#-siya---your-free-ai-cat-assistant)

</div>
