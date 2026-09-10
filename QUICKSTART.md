# 🚀 Quick Start Guide for Siya

## Step 1: Install Dependencies

Double-click `install.bat` or run in terminal:
```bash
install.bat
```

This will install:
- pyttsx3 (text-to-speech)
- Updated OpenAI library
- Audio libraries (sounddevice, scipy)

## Step 2: Run Siya

Double-click `run_siya.bat` or run:
```bash
python siya.py
```

## 🎮 How to Use

### Voice Mode (Recommended!)
1. Click the **"🎤 Hold to Speak"** button
2. Speak your question clearly (you have 5 seconds)
3. Wait for Siya to respond with voice!

### Text Mode
1. Click **"⌨️ Type Message"**
2. Type your message
3. Press Enter or click Send

## 💡 What Can You Ask?

Try these:
- "What's the weather like today?"
- "Tell me a joke"
- "Help me with Python coding"
- "What's 25 times 37?"
- "Explain quantum physics simply"
- "Give me a motivational quote"

## 🐱 Cat Mood Guide

Watch Siya's expression change:
- **😺 Happy face** = Ready to chat
- **👂 Attentive** = Listening to you
- **🤔 Thoughtful** = Thinking about your question
- **💬 Talking** = Speaking the answer

## ⚠️ Troubleshooting

### No voice output?
- Check your speaker volume
- On Windows, ensure Windows Speech Engine is working

### Microphone not working?
- Check Windows microphone permissions
- Test your mic in Windows Settings > Privacy > Microphone

### API errors?
- Verify your `.env` file has the correct OpenAI API key
- Check your internet connection
- Ensure you have API credits

## 🎨 Customization Tips

Want to change Siya's personality? Edit `siya.py`:
- Find the `ask_siya()` function
- Modify the system message to change behavior
- Make Siya more funny, serious, or technical!

---

**Have fun with Siya! 🐱✨**
