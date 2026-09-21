# 😺 Siya - AI Cat Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-yellow)
![Status](https://img.shields.io/badge/status-active-success)

**A beautiful, interactive AI assistant with a playful cat personality - 100% FREE!**

🎨 **Now with Animated Cat Image Interface!** 🐱

[Features](#-features) • [Quick Start](#-quick-start) • [Versions](#-four-versions-available) • [Installation](#-installation) • [Documentation](#-documentation)

</div>

---
 
## 🌟 Features

### 💬 **Smart AI Conversations**
- Powered by **FREE** AI engines (Ollama or Groq)
- Also supports OpenAI (paid)
- Natural, friendly, and helpful responses
- Cat-themed personality 🐱

### 🎨 **Beautiful Interfaces**
- **🆕 Image Version** - Animated cat image with 6 reactive animations
- **Emoji Version** - 9 different emoji expressions (120pt)
- **ASCII Version** - Classic ASCII art cat
- Modern dark theme UI
- Smooth transitions

### ✅ **Task Management**
- Add tasks via text commands
- Visual task list with one-click completion
- Automatic saving between sessions
- Never forget anything!

### 🆓 **100% FREE Forever**
- **No API costs** with Ollama (local AI)
- **Free cloud option** with Groq (14,400 requests/day)
- **Optional paid** OpenAI support
- **Your choice** - privacy or convenience

### 🔒 **User-Friendly & Secure**
- Interactive setup wizards
- User-defined API keys (no hardcoding)
- Settings management through UI
- Safe to share on GitHub

---

## 🎯 Four Versions Available

### 1. 🎨 **Siya Image** (NEW! Recommended for Best Visuals)
- **File:** `siya_image.py`
- **Cost:** $0 forever
- **Interface:** Animated cat image with 6 reactive animations
- **Features:** Text chat, tasks, settings, FREE AI
- **Setup:** Use your own cat image or auto-generated placeholder
- **Perfect for:** Best visual experience, showcasing photos

### 2. 🆓 **Siya Free** (Recommended for Most Users)
- **File:** `siya_free.py`
- **Cost:** $0 forever
- **Interface:** Giant emoji cat (9 expressions)
- **Features:** Text chat, tasks, settings, FREE AI
- **Setup:** Choose Ollama or Groq on first run
- **Perfect for:** Privacy, unlimited use, no costs

### 3. 💰 **Siya Advanced**
- **File:** `siya_advanced.py`
- **Cost:** OpenAI API ($5-20/month)
- **Interface:** ASCII art cat with animations
- **Features:** Voice input/output, TTS, tasks, OpenAI API
- **Setup:** Enter API key when prompted
- **Perfect for:** Voice interaction, premium features

### 4. 💰 **Siya Basic**
- **File:** `siya.py`
- **Cost:** OpenAI API ($5-20/month)
- **Interface:** ASCII art cat
- **Features:** Text chat, TTS, OpenAI API
- **Setup:** Enter API key when prompted
- **Perfect for:** Simple OpenAI chat interface

---

## ⚡ Quick Start

### 🎨 **Option 1: Image Version (Best Visuals)**

```bash
# Install dependencies
pip install -r requirements.txt

# Optional: Add your cat image
# Save as cat_source.png, then run:
python setup_cat_image.py

# Run Siya
python siya_image.py
# OR double-click: run_siya_image.bat
```

### 🆓 **Option 2: Free Version (Easiest)**

```bash
# 1. Install Ollama (one time)
# Visit: https://ollama.com and download

# 2. Download AI model (one time)
ollama run llama2

# 3. Run Siya
python siya_free.py
# OR double-click: run_siya_free.bat

# 4. Choose Ollama in welcome screen
# 5. Start chatting for FREE!
```

### 💰 **Option 3: OpenAI Versions**

```bash
# 1. Get API key from platform.openai.com

# 2. Run version of choice
python siya_advanced.py  # Voice + Tasks
# OR
python siya.py  # Simple

# 3. Enter API key when prompted
# 4. Start chatting!
```

---

## 📋 Detailed Comparison

| Feature | Image | Free | Advanced | Basic |
|---------|-------|------|----------|-------|
| **Cost** | $0 | $0 | $5-20/mo | $5-20/mo |
| **Cat Visual** | 🎨 Image | 😺 Emoji | ASCII | ASCII |
| **Animations** | 6 types | Size only | States | States |
| **Text Chat** | ✅ | ✅ | ✅ | ✅ |
| **Voice Input** | ❌ | ❌ | ✅ | ✅ |
| **Text-to-Speech** | ❌ | ❌ | ✅ | ✅ |
| **Task Manager** | ✅ | ✅ | ✅ | ❌ |
| **Settings Tab** | ✅ | ✅ | ❌ | ❌ |
| **API Setup** | UI Wizard | UI Wizard | UI Dialog | UI Dialog |
| **Offline Mode** | ✅ (Ollama) | ✅ (Ollama) | ❌ | ❌ |
| **Customization** | Your images! | Limited | Limited | Limited |

---

## 🚀 Installation

### Prerequisites
- **Python 3.8+** installed
- **Windows 10/11** (best emoji/image support)
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

### Step 3: Choose Your Version
See [Quick Start](#-quick-start) above for version-specific instructions.

---

## 🎨 Image Version Setup

### Using Your Own Cat Image

**Step 1: Prepare Image**
- Save your cat image as `cat_source.png` (or `.jpg`)
- Place in the `siya` folder
- Recommended: 600x600 pixels, square

**Step 2: Process Image**
```bash
python setup_cat_image.py
```

This will:
- ✅ Load your image
- ✅ Convert to RGB if needed
- ✅ Resize to optimal size
- ✅ Save as `cat_image.png`

**Step 3: Run**
```bash
python siya_image.py
```

### Using Placeholder Cat

Just run directly:
```bash
python siya_image.py
```

App will create a cute placeholder cat automatically!

---

## 🤖 AI Engine Options

### Option 1: Ollama (Recommended - 100% Free)

**Why Choose Ollama?**
- ✅ **100% FREE** forever
- ✅ **Private** - Runs on your PC
- ✅ **No internet** needed after setup
- ✅ **Unlimited** usage
- ✅ **Fast** responses

**Setup:**
```bash
# 1. Install from https://ollama.com

# 2. Download model
ollama run llama2

# 3. Run Siya (Image or Free version)
python siya_image.py

# 4. Choose Ollama in welcome screen
```

**Available Models:**
- `llama2` (4GB) - Recommended
- `mistral` (4GB) - Fast & efficient
- `tinyllama` (600MB) - Very fast
- `llama2:13b` (7GB) - Better quality

### Option 2: Groq API (Free Cloud)

**Why Choose Groq?**
- ✅ **100% FREE** (no credit card!)
- ✅ **Quick setup** (5 minutes)
- ✅ **No downloads**
- ✅ **14,400 requests/day**

**Setup:**
```bash
# 1. Get key from https://console.groq.com

# 2. Run Siya
python siya_image.py  # or siya_free.py

# 3. Choose Groq, enter API key

# 4. Start chatting!
```

### Option 3: OpenAI (Paid)

**For Advanced/Basic versions:**
```bash
# 1. Get key from platform.openai.com/api-keys

# 2. Run version
python siya_advanced.py

# 3. Enter key when prompted

# Cost: ~$5-20/month
```

---

## 📖 Usage Guide

### Chat Interface

```
┌──────────────────────────────────────┐
│  [💬 Chat] [✅ Tasks] [⚙️ Settings] │
├──────────────────────────────────────┤
│                                      │
│         🐱 Cat Display               │
│      (Image/Emoji/ASCII)             │
│                                      │
│      😺 Ready to help!               │
├──────────────────────────────────────┤
│  💬 Conversation                     │
│  ┌────────────────────────────────┐ │
│  │ [12:30] 👤 You: Hello!         │ │
│  │ [12:30] 🐱 Siya: Hi! Meow!     │ │
│  └────────────────────────────────┘ │
├──────────────────────────────────────┤
│  [⌨️ Type Message]  [🗑️ Clear]      │
└──────────────────────────────────────┘
```

### Example Conversations

```
You: What's 245 times 17?
Siya: 4,165! Need help with anything else? 🐱

You: Tell me a joke
Siya: Why don't cats play poker? Too many cheetahs! 😹

You: add task buy groceries
Siya: Got it! Task added: 'buy groceries' 📝
```

### Task Commands

```
"add task [description]"
"remind me to [description]"
"create task [description]"
"new task [description]"
```

---

## 🎬 Animations (Image Version)

| Animation | When | Description |
|-----------|------|-------------|
| **Happy** | Idle | Normal display |
| **Thinking** | Processing | Slight dim effect |
| **Speaking** | Responding | Gentle glow |
| **Excited** | Task added | Bounce up/down (0.6s) |
| **Loving** | Task completed | Brightness pulse (1.2s) |
| **Error** | Problems | Shake left/right (0.4s) |

---

## 🎨 Customization

### Change Cat Image (Image Version)

```bash
# Replace with your image
copy new_cat.png cat_source.png
python setup_cat_image.py
```

### Change Emoji (Free Version)

In `siya_free.py`:
```python
moods = {
    "happy": "😺",     # Change to any emoji!
    "thinking": "🤔",
    # etc.
}
```

### Change Colors (Any Version)

Find these values and modify:
```python
bg="#1a1a2e"    # Main background
fg="#00d4ff"    # Accent color
```

### Change AI Personality

Find the system prompt:
```python
"You are Siya, a helpful AI cat assistant..."
# Customize this message!
```

---

## 🔑 API Key Management

### Configuration Files

| Version | Config File | Stores |
|---------|-------------|--------|
| Image/Free | `siya_config.json` | AI choice, Groq key, Ollama model |
| Advanced/Basic | `siya_openai_config.json` | OpenAI API key |

### Changing API Keys

**Image/Free Versions:**
1. Go to ⚙️ Settings tab
2. Click "Change AI Engine"
3. Enter new configuration

**OpenAI Versions:**
1. Delete `siya_openai_config.json`
2. Run app again
3. Enter new API key

---

## 🐛 Troubleshooting

### Common Issues

**"Error 429: No credits remaining"**
- OpenAI account out of credits
- Solution: Use FREE version instead!
```bash
python siya_free.py
```

**"Can't connect to my brain" (Ollama)**
```bash
# Start Ollama
ollama serve

# Or run model directly
ollama run llama2
```

**"No module named 'PIL'"**
```bash
pip install Pillow
```

**"Invalid API key"**
- Delete config file
- Run app again
- Enter correct key

**Cat image not showing**
- Check `cat_image.png` exists
- Run `setup_cat_image.py`
- Or let app create placeholder

### Error 429 Guide

If you get OpenAI credit errors:

**Option 1: Add Credits**
- Visit https://platform.openai.com/billing
- Add payment method
- Purchase credits

**Option 2: Use FREE Version** (Recommended!)
```bash
python siya_image.py
# Choose Ollama - no costs ever!
```

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **README.md** | This file - complete guide |
| **IMAGE_VERSION_GUIDE.md** | Image version documentation |
| **UPDATED_README.md** | v2.0 migration guide |
| **CHANGELOG.md** | Version history |
| **QUICKSTART.md** | Quick getting started |
| **FREE_SETUP.md** | FREE version setup |
| **EMOJI_CAT_GUIDE.md** | Emoji expressions |
| **SOLUTION_SUMMARY.md** | Problem/solution reference |

---

## 💡 Tips & Best Practices

### For Best Experience

1. **Use Image Version** with your own cat photo
2. **Choose Ollama** for unlimited free usage
3. **Enable Tasks** to stay organized
4. **Clear chat** between topics
5. **Check Settings** to customize

### Performance Tips

1. Keep images under 800x800
2. Use PNG format for quality
3. Close other heavy apps
4. Use smaller Ollama models if slow

### Privacy Tips

1. Use Ollama (100% local)
2. Don't share config files
3. Add configs to `.gitignore`
4. Use different keys for testing

---

## 🎯 Use Cases

### For Students
- Homework help
- Study planning with tasks
- Quick calculations
- Research assistance

### For Developers
- Code debugging
- Task tracking
- Quick reference
- Algorithm explanations

### For Professionals
- Daily task management
- Information lookup
- Email drafting
- Meeting reminders

### For Everyone
- General Q&A
- Entertainment
- Learning
- Staying organized

---

## 🆚 Version Recommendations

### Choose **Image Version** if:
- ✅ Want best visual experience
- ✅ Have your own cat photos
- ✅ Like smooth animations
- ✅ Want to impress others

### Choose **Free Version** if:
- ✅ Want quick setup
- ✅ Like emoji interface
- ✅ Don't have images
- ✅ Want simplicity

### Choose **Advanced Version** if:
- ✅ Need voice input
- ✅ Have OpenAI credits
- ✅ Want TTS output
- ✅ Premium features

### Choose **Basic Version** if:
- ✅ Want simplest paid option
- ✅ Have OpenAI credits
- ✅ Don't need tasks
- ✅ Minimal interface

---

## 🤝 Contributing

We welcome contributions!

### Ways to Help

1. **Report Bugs** - Open an issue
2. **Suggest Features** - Create feature request
3. **Submit Code** - Fork and PR
4. **Improve Docs** - Fix typos, add examples
5. **Share** - Tell others about Siya!

### Development

```bash
git clone https://github.com/yourusername/siya.git
cd siya
pip install -r requirements.txt
python siya_image.py
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

Feel free to use, modify, and distribute!

---

## 🙏 Acknowledgments

- **Ollama** - Free local AI
- **Groq** - Free cloud AI
- **OpenAI** - Premium AI option
- **PIL/Pillow** - Image processing
- **Python** - Programming language
- **You** - For using Siya! 😺

---

## 📊 Feature Matrix

| Feature | Image | Free | Advanced | Basic |
|---------|-------|------|----------|-------|
| Text Chat | ✅ | ✅ | ✅ | ✅ |
| Voice Input | ❌ | ❌ | ✅ | ✅ |
| Text-to-Speech | ❌ | ❌ | ✅ | ✅ |
| Task Manager | ✅ | ✅ | ✅ | ❌ |
| Settings Tab | ✅ | ✅ | ❌ | ❌ |
| Free Option | ✅ | ✅ | ❌ | ❌ |
| Paid Option | ❌ | ❌ | ✅ | ✅ |
| Offline Mode | ✅ | ✅ | ❌ | ❌ |
| Custom Images | ✅ | ❌ | ❌ | ❌ |
| Animations | 6 types | Limited | Limited | Limited |
| Visual Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 🚀 Quick Reference

### Launch Commands

```bash
# Image Version (recommended for visuals)
python siya_image.py

# Free Version (recommended for most users)
python siya_free.py

# Advanced Version (voice + tasks)
python siya_advanced.py

# Basic Version (simple chat)
python siya.py

# Or use batch files
run_siya_image.bat
run_siya_free.bat
run_siya.bat
```

### Setup Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Setup cat image (Image version)
python setup_cat_image.py

# Install Ollama
# Visit: https://ollama.com

# Download AI model
ollama run llama2
```

---

## 🎉 Final Notes

Siya is built with ❤️ to provide a FREE, private, and fun AI assistant experience.

### Key Highlights

- 🆓 **FREE forever** (Ollama option)
- 🎨 **Beautiful interfaces** (4 versions!)
- 😺 **Fun cat personality**
- ✅ **Actually useful** (tasks, chat, help)
- 🔒 **Private** (local AI option)
- 🚀 **Easy to use** (setup wizards)

### Get Started Now!

**Best for most users:**
```bash
python siya_image.py
```

**Best for free:**
```bash
python siya_free.py
```

**Best for voice:**
```bash
python siya_advanced.py
```

---

## 📞 Support & Contact

- **Issues:** [GitHub Issues](https://github.com/yourusername/siya/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/siya/discussions)
- **Email:** your.email@example.com

---

<div align="center">

**🐱 Enjoy your AI Cat Assistant! 😺✨**

Made with ❤️ and 🐱 | © 2024 Siya Project

**Star ⭐ this repo if you love Siya!**

[⬆ Back to Top](#-siya---your-free-ai-cat-assistant)

</div>
