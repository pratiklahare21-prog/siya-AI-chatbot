# 🎉 Siya Complete Guide - All Versions

## 📋 Table of Contents
1. [Overview](#overview)
2. [Four Versions](#four-versions)
3. [Quick Start](#quick-start)
4. [Detailed Setup](#detailed-setup)
5. [Features Comparison](#features-comparison)
6. [File Structure](#file-structure)
7. [Troubleshooting](#troubleshooting)

---

## Overview

**Siya** is a FREE AI cat assistant with multiple versions to suit your needs!

### Latest Updates (v2.0)
- ✅ User-defined API keys (no hardcoding!)
- ✅ Interactive setup wizards
- ✅ NEW: Animated cat image interface
- ✅ Security improvements
- ✅ Comprehensive documentation

---

## Four Versions

### 🎨 1. Image Version (siya_image.py)

**Best For:** Visual experience, showcasing photos

**Features:**
- Full-color animated cat image
- 6 reactive animations (bounce, pulse, shake)
- Use your own cat photos!
- Task management
- Settings tab
- FREE AI (Ollama/Groq)

**Animations:**
- Happy (idle)
- Thinking (dimmed)
- Speaking (glowing)
- Excited (bouncing)
- Loving (pulsing)
- Error (shaking)

**Setup:**
```bash
# Optional: Add your cat image
python setup_cat_image.py

# Run
python siya_image.py
```

---

### 🆓 2. Free Version (siya_free.py)

**Best For:** Most users, privacy, no costs

**Features:**
- Giant emoji cat (120pt)
- 9 different expressions
- Task management
- Settings tab
- FREE AI (Ollama/Groq)
- No API costs ever!

**Emoji Moods:**
😺 😸 🤔 😻 😹 😽 😿 🙀 😾

**Setup:**
```bash
# Install Ollama
ollama run llama2

# Run
python siya_free.py
```

---

### 💰 3. Advanced Version (siya_advanced.py)

**Best For:** Voice interaction, premium features

**Features:**
- Voice input (microphone)
- Text-to-speech output
- Task management
- ASCII art cat (4 states)
- OpenAI API
- Requires credits ($5-20/month)

**Setup:**
```bash
# Get API key from platform.openai.com

# Run
python siya_advanced.py

# Enter key when prompted
```

---

### 💰 4. Basic Version (siya.py)

**Best For:** Simple OpenAI chat

**Features:**
- Text chat only
- Text-to-speech output
- ASCII art cat
- OpenAI API
- Simpler interface
- Requires credits ($5-20/month)

**Setup:**
```bash
# Get API key from platform.openai.com

# Run
python siya.py

# Enter key when prompted
```

---

## Quick Start

### Absolute Fastest (Uses Placeholder)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run image version (creates placeholder cat)
python siya_image.py

# 3. Choose Ollama in welcome screen

# 4. Start chatting!
```

### With Your Cat Image

```bash
# 1. Save your cat as cat_source.png

# 2. Process it
python setup_cat_image.py

# 3. Run
python siya_image.py

# 4. See your cat animated!
```

### With FREE AI (No Costs)

```bash
# 1. Install Ollama from https://ollama.com

# 2. Download model
ollama run llama2

# 3. Run any FREE version
python siya_image.py
# OR
python siya_free.py

# 4. Choose Ollama, start chatting!
```

### With OpenAI (Paid)

```bash
# 1. Get key from platform.openai.com

# 2. Run paid version
python siya_advanced.py
# OR
python siya.py

# 3. Enter key, start chatting!
```

---

## Detailed Setup

### Prerequisites

**Required:**
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for setup)

**Optional:**
- Ollama (for FREE versions)
- OpenAI account (for paid versions)
- Cat image (for image version)

### Step-by-Step Installation

**1. Get the Code**
```bash
git clone https://github.com/yourusername/siya.git
cd siya
```

**2. Create Virtual Environment (Recommended)**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

This installs:
- openai (AI API)
- Pillow (image processing)
- requests (HTTP)
- sounddevice (audio - for voice)
- scipy (audio processing - for voice)
- pyttsx3 (text-to-speech - for voice)

**4. Choose Version**

See version-specific instructions above.

---

## Features Comparison

### Visual Interface

| Version | Cat Display | Size | Expressions | Animations |
|---------|-------------|------|-------------|------------|
| Image | Full-color image | 300x300 | 6 moods | 6 types |
| Free | Emoji | 120pt | 9 moods | Size change |
| Advanced | ASCII art | ~15 lines | 4 states | State change |
| Basic | ASCII art | ~15 lines | 4 states | State change |

### Functionality

| Feature | Image | Free | Advanced | Basic |
|---------|-------|------|----------|-------|
| Text Chat | ✅ | ✅ | ✅ | ✅ |
| Voice Input | ❌ | ❌ | ✅ | ✅ |
| Voice Output (TTS) | ❌ | ❌ | ✅ | ✅ |
| Task Manager | ✅ | ✅ | ✅ | ❌ |
| Settings Tab | ✅ | ✅ | ❌ | ❌ |
| Custom Images | ✅ | ❌ | ❌ | ❌ |

### AI Options

| Version | FREE (Ollama) | FREE (Groq) | Paid (OpenAI) |
|---------|---------------|-------------|---------------|
| Image | ✅ | ✅ | ❌ |
| Free | ✅ | ✅ | ❌ |
| Advanced | ❌ | ❌ | ✅ |
| Basic | ❌ | ❌ | ✅ |

### Cost Comparison

| Version | Minimum Cost | Maximum Cost | Best For |
|---------|--------------|--------------|----------|
| Image | $0/month | $0/month | Free users |
| Free | $0/month | $0/month | Free users |
| Advanced | $5/month | $20/month | Voice users |
| Basic | $5/month | $20/month | Simple chat |

---

## File Structure

```
siya/
├── Core Files
│   ├── siya_image.py          ← Image version (NEW!)
│   ├── siya_free.py           ← Free emoji version
│   ├── siya_advanced.py       ← Advanced OpenAI version
│   └── siya.py                ← Basic OpenAI version
│
├── Setup & Utilities
│   ├── setup_cat_image.py     ← Image processor
│   ├── install.bat            ← Dependency installer
│   ├── LAUNCHER.bat           ← Version chooser
│   ├── run_siya_image.bat     ← Image launcher
│   ├── run_siya_free.bat      ← Free launcher
│   └── run_siya.bat           ← Advanced launcher
│
├── Configuration
│   ├── requirements.txt       ← Python dependencies
│   ├── .env                   ← Deprecated (info only)
│   ├── .env.example           ← Example config
│   ├── .gitignore             ← Git exclusions
│   ├── siya_config.json       ← FREE version config (auto)
│   └── siya_openai_config.json ← OpenAI config (auto)
│
├── Data Files
│   ├── siya_tasks.json        ← Your tasks (auto)
│   ├── cat_image.png          ← Processed cat (auto)
│   └── cat_source.png         ← Your cat (optional)
│
├── Documentation
│   ├── README.md              ← Main documentation
│   ├── COMPLETE_GUIDE.md      ← This file
│   ├── IMAGE_VERSION_GUIDE.md ← Image version details
│   ├── UPDATED_README.md      ← v2.0 migration
│   ├── CHANGELOG.md           ← Version history
│   ├── QUICKSTART.md          ← Quick start
│   ├── FREE_SETUP.md          ← FREE setup guide
│   ├── EMOJI_CAT_GUIDE.md     ← Emoji reference
│   └── SOLUTION_SUMMARY.md    ← Problem solutions
│
└── Environment
    └── venv/                  ← Virtual environment
```

---

## Troubleshooting

### Installation Issues

**"pip not found"**
```bash
# Install pip
python -m ensurepip --upgrade
```

**"Python not found"**
- Download from python.org
- Install Python 3.8+
- Check "Add to PATH" during install

**"Module not found"**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Runtime Issues

**Error 429: No Credits (OpenAI)**

**Problem:** OpenAI account out of credits

**Solutions:**
1. Add credits at platform.openai.com/billing
2. Use FREE version instead:
```bash
python siya_image.py
```

**"Can't connect to my brain" (Ollama)**

**Problem:** Ollama not running

**Solutions:**
```bash
# Start Ollama server
ollama serve

# Or run model directly
ollama run llama2
```

**"Invalid API key"**

**Problem:** Wrong or expired API key

**Solutions:**
1. Get new key from respective platform
2. Delete config file:
   - `siya_config.json` (Free/Image)
   - `siya_openai_config.json` (Advanced/Basic)
3. Run app again
4. Enter correct key

**"No module named 'PIL'"**

**Problem:** Pillow not installed

**Solution:**
```bash
pip install Pillow
```

**"No module named 'tkinter'"**

**Problem:** Tkinter not installed

**Solution:**
- Windows: Reinstall Python with tcl/tk
- Linux: `sudo apt-get install python3-tk`
- Mac: Included with Python from python.org

### Image Version Issues

**Cat image not showing**

**Check:**
1. File exists: `cat_image.png`
2. In correct folder
3. Valid image format

**Solution:**
```bash
# Let app create placeholder
python siya_image.py

# Or process your image
python setup_cat_image.py
```

**Image looks blurry**

**Cause:** Low resolution source

**Solution:**
- Use higher resolution image (600x600+)
- Ensure good quality source

**Animations not smooth**

**Cause:** System performance

**Solution:**
- Close other apps
- Use smaller image
- Reduce animation speed in code

### Free Version Issues

**Ollama connection failed**

**Check:**
1. Ollama installed
2. Model downloaded
3. Server running

**Commands:**
```bash
# Check installation
ollama list

# Download model
ollama pull llama2

# Start server
ollama serve
```

**Groq API error**

**Check:**
1. Valid API key
2. Key starts with "gsk_"
3. Internet connection

**Solution:**
1. Go to Settings tab
2. Update API key
3. Or get new key from console.groq.com

### Advanced/Basic Version Issues

**Voice not working**

**Check:**
1. Microphone connected
2. Microphone permissions
3. Windows settings

**Solution:**
- Settings > Privacy > Microphone
- Allow app access
- Test in Voice Recorder first

**TTS not working**

**Check:**
1. Speakers working
2. Volume not muted
3. Windows TTS installed

**Solution:**
- Settings > Time & Language > Speech
- Test Windows TTS
- Restart app

---

## Configuration

### Config Files

**siya_config.json** (Image/Free versions)
```json
{
  "use_local_ai": true,
  "groq_api_key": "gsk_...",
  "ollama_model": "llama2",
  "ollama_url": "http://localhost:11434"
}
```

**siya_openai_config.json** (Advanced/Basic versions)
```json
{
  "openai_api_key": "sk-..."
}
```

**siya_tasks.json** (All versions with tasks)
```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "created": "2024-01-15T10:30:00",
    "completed": false
  }
]
```

### Changing Configuration

**Through UI (Recommended):**
1. Open Settings tab (Image/Free versions)
2. Click "Change AI Engine"
3. Follow prompts

**Manual (Advanced):**
1. Close app
2. Edit JSON file
3. Save changes
4. Restart app

---

## Best Practices

### For Best Experience

1. **Choose Right Version**
   - Visual focus → Image
   - Free forever → Free
   - Voice needed → Advanced
   - Simple chat → Basic

2. **Use Appropriate AI**
   - Privacy → Ollama
   - Convenience → Groq
   - Premium → OpenAI

3. **Optimize Performance**
   - Keep images reasonable size
   - Close unused apps
   - Use smaller AI models if slow

4. **Stay Organized**
   - Use task manager
   - Clear chat between topics
   - Review settings regularly

### Security

1. **Protect API Keys**
   - Never share config files
   - Add to `.gitignore`
   - Use different keys for testing

2. **Privacy**
   - Use Ollama for 100% local
   - Don't share sensitive info
   - Review AI provider policies

3. **Updates**
   - Check for updates regularly
   - Read CHANGELOG.md
   - Backup configs before updating

---

## Tips & Tricks

### Productivity

**Task Commands:**
```
"add task [description]"
"remind me to [description]"
"create task [description]"
```

**Quick Actions:**
- Press Enter to send message
- Clear chat for fresh context
- Use Settings to switch AI

### Customization

**Change Colors:**
```python
# In any version, find and modify:
bg="#2d3436"  # Background
fg="#00d4ff"  # Accent
```

**Change Personality:**
```python
# Find system prompt:
"You are Siya, a helpful AI cat..."
# Modify to your liking!
```

**Change Animations:**
```python
# In siya_image.py:
self.canvas.after(100, ...)  # Change timing
scale = 1.1  # Change intensity
```

---

## Getting Help

### Resources

1. **README.md** - Complete documentation
2. **This Guide** - Comprehensive overview
3. **Specific Guides** - Version-specific docs
4. **CHANGELOG.md** - Version history

### Common Questions

**Q: Which version should I use?**
A: Image for visuals, Free for most users

**Q: Is it really free?**
A: Yes! With Ollama or Groq (Image/Free versions)

**Q: Can I switch versions?**
A: Yes! Just run different file

**Q: Can I use my own cat photo?**
A: Yes! In Image version

**Q: Do I need internet?**
A: With Ollama, no (after setup)

**Q: Is my data private?**
A: With Ollama, 100% private

---

## Summary

### Version Recommendations

| If You Want... | Use This Version |
|----------------|------------------|
| Best visuals | 🎨 Image |
| Free forever | 🆓 Free |
| Voice input | 💰 Advanced |
| Simple chat | 💰 Basic |
| Privacy | 🎨 Image or 🆓 Free (with Ollama) |
| No costs | 🎨 Image or 🆓 Free |
| Custom photos | 🎨 Image |
| Task management | 🎨 Image, 🆓 Free, or 💰 Advanced |

### Quick Commands

```bash
# Choose version launcher
LAUNCHER.bat

# Or run directly:
python siya_image.py     # Image version
python siya_free.py      # Free version
python siya_advanced.py  # Advanced version
python siya.py           # Basic version

# Setup helpers:
python setup_cat_image.py  # Process cat image
install.bat                # Install dependencies
```

---

## Conclusion

Siya offers four versions to match your needs:

- **🎨 Image** - Beautiful animated cat photos
- **🆓 Free** - Emoji cat, no costs
- **💰 Advanced** - Voice, tasks, premium
- **💰 Basic** - Simple OpenAI chat

All versions are:
- ✅ Easy to use
- ✅ Well documented
- ✅ Actively maintained
- ✅ User-friendly

Choose the one that fits your needs and enjoy your AI cat assistant!

---

**🐱 Happy chatting with Siya! 😺✨**

For more help, check the other documentation files or open an issue on GitHub.
