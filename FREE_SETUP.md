# 🆓 FREE Siya Setup Guide

## 🎉 No More API Costs!
Your new version uses **100% FREE AI** with two options:
---
## Option 1: Ollama (Recommended - Completely Free!)

### ✅ Pros:
- 💯 **100% FREE** - No API keys, no costs, ever!
- 🔒 **Private** - Runs on your PC, no internet needed
- ⚡ **Fast** - No network delays
- 🚀 **Unlimited usage** - Use as much as you want!

### 📥 Installation:

1. **Download Ollama**
   - Visit: https://ollama.com
   - Click "Download" for Windows
   - Install the application

2. **Install AI Model**
   - Open Command Prompt or PowerShell
   - Run: `ollama run llama2`
   - Wait for download (about 4GB)
   - Model will start automatically

3. **Run Siya**
   ```bash
   python siya_free.py
   ```
   
   Or create this batch file `run_siya_free.bat`:
   ```batch
   @echo off
   venv\Scripts\python.exe siya_free.py
   pause
   ```

### 🎯 That's it! No API keys needed!
---
## Option 2: Groq API (Free Online)

### ✅ Pros:
- 🆓 **FREE** - No credit card required
- ☁️ **Cloud-based** - No large downloads
- 🚀 **Fast** - Groq is super fast
- 📈 **Generous limits** - 14,400 requests per day!

### 📥 Setup:

1. **Get Free API Key**
   - Visit: https://console.groq.com
   - Sign up (no credit card needed!)
   - Go to API Keys section
   - Create new API key

2. **Update Code**
   - Open `siya_free.py`
   - Find line: `GROQ_API_KEY = "gsk_your_free_api_key_here"`
   - Replace with your actual key
   - Find line: `USE_LOCAL_AI = True`
   - Change to: `USE_LOCAL_AI = False`

3. **Run Siya**
   ```bash
   python siya_free.py
   ```
---

## 🎨 New Emoji Cat Features

### Cartoon Emoji Expressions:

- 😺 **Happy** - Default idle state
- 😸 **Listening** - When you're typing
- 🤔 **Thinking** - Processing your message
- 😻 **Speaking** - Responding to you
- 😹 **Excited** - Task added successfully
- 😽 **Loving** - Task completed
- 😿 **Sleepy** - Connection issues
- 🙀 **Surprised** - Errors
- 😾 **Grumpy** - (reserved for future)

### Big Emoji Display:
The cat now shows as a **HUGE emoji** (120pt font) instead of ASCII art!

---

## 🆚 Comparison: Ollama vs Groq

| Feature | Ollama | Groq |
|---------|--------|------|
| Cost | FREE | FREE |
| Setup | Medium | Easy |
| Download Size | 4GB | None |
| Internet | Not needed | Required |
| Privacy | 100% Private | Cloud |
| Speed | Fast | Very Fast |
| Daily Limit | Unlimited | 14,400 |
| Models | Multiple | Multiple |

**Recommendation:** 
- **Ollama** if you have disk space and want privacy
- **Groq** if you want quick setup

---
## 🚀 Quick Start

### For Ollama:
```bash
# Install Ollama from https://ollama.com
ollama run llama2

# Run Siya
python siya_free.py
```

### For Groq:
```bash
# 1. Get key from https://console.groq.com
# 2. Update GROQ_API_KEY in siya_free.py
# 3. Set USE_LOCAL_AI = False

python siya_free.py
```
---

## 📦 Requirements

Only need ONE dependency for Groq:
```bash
pip install requests
```

For Ollama, requests is optional (but recommended).

---

## 🎯 What Works

✅ **Text Chat** - Type and get responses
✅ **Task Management** - Add/complete tasks
✅ **Emoji Cat** - Big cartoon emotions
✅ **Free AI** - No API costs
✅ **Smart Responses** - Helpful AI
✅ **Fast** - Quick responses

❌ **Voice Input** - Removed (required paid API)
❌ **Text-to-Speech** - Optional (works if pyttsx3 installed)

---

## 💡 Pro Tips

### Make it Faster:
- Use Ollama for instant responses
- Use smaller models: `ollama run llama2:7b`

### Better Responses:
- Use larger models: `ollama run llama2:13b`
- Or with Groq: Use `llama-3.3-70b-versatile` (already set)

### Save Data:
- Tasks auto-save to `siya_tasks.json`
- Chat history not saved (privacy)

---

## 🐛 Troubleshooting

### Ollama: "Couldn't connect to my brain"
**Fix:**
1. Check Ollama is running: `ollama list`
2. Start the server: `ollama serve`
3. Pull model: `ollama pull llama2`
4. Run model: `ollama run llama2`

### Groq: "API error"
**Fix:**
1. Check your API key is correct
2. Verify you set `USE_LOCAL_AI = False`
3. Check internet connection
4. Generate new key at: https://console.groq.com

### Cat emoji not showing
**Fix:**
1. Windows 10/11 has emoji support built-in
2. Update to latest Windows version
3. Or emojis will show as boxes (still works!)

---

## 🎓 Available Ollama Models

Try different models:

**Small & Fast:**
```bash
ollama run tinyllama    # 600MB, very fast
ollama run llama2:7b    # 4GB, good balance
```

**Medium:**
```bash
ollama run llama2:13b   # 7GB, better quality
ollama run mistral      # 4GB, fast & good
```

**Large:**
```bash
ollama run llama2:70b   # 40GB, best quality
```

Update the model in code:
```python
"model": "llama2"  # Change to "mistral" or "tinyllama"
```

---

## 🌟 Features Comparison

| Feature | Old (OpenAI) | New (Free) |
|---------|--------------|------------|
| API Cost | $$$$ | FREE |
| Voice Input | ✅ | ❌ |
| Text Chat | ✅ | ✅ |
| Cat Visual | ASCII | Emoji 😺 |
| Tasks | ✅ | ✅ |
| Privacy | Cloud | Local option |
| Speed | Fast | Fast |
| Limits | Based on $ | Unlimited |

---

## 🎉 You're Ready!

Choose your setup:
1. **Ollama** - Best for privacy & unlimited use
2. **Groq** - Best for quick setup

Both are **100% FREE!** 🎊

Run with:
```bash
python siya_free.py
```

Enjoy your free AI cat assistant! 😺✨
