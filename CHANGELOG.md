# 📋 Changelog - Siya AI Cat Assistant

## 🎉 Version 2.0 - User-Defined API Keys (Latest)

### 🔑 Major Changes

#### **1. API Key Management Overhaul**
- ✅ **No more hardcoded API keys**
- ✅ **Interactive UI dialogs** for API key entry
- ✅ **Secure JSON storage** (not in code)
- ✅ **First-run setup wizards**
- ✅ **Settings tabs** to change keys anytime

#### **2. All Three Versions Updated**

**siya_free.py:**
- Welcome screen on first run
- Choose Ollama or Groq API
- Enter Groq API key through dialog (if chosen)
- Settings tab to change engine
- Config saved in `siya_config.json`

**siya_advanced.py:**
- API key prompt on first run
- Validates key immediately
- Detects credit errors (429)
- Suggests FREE alternative
- Config saved in `siya_openai_config.json`

**siya.py:**
- API key prompt on first run
- Same validation as advanced
- Detects credit errors
- Config saved in `siya_openai_config.json`

#### **3. Security Improvements**
- API keys in `.gitignore`
- Masked key display in UI
- Key validation before use
- Error handling for invalid keys
- Separate config files per version

#### **4. User Experience**
- No code editing required
- Clear error messages
- Helpful dialog boxes
- Step-by-step setup
- Visual feedback

### 📁 New Files

| File | Purpose |
|------|---------|
| `siya_config.json` | FREE version config (auto-created) |
| `siya_openai_config.json` | OpenAI versions config (auto-created) |
| `.env.example` | Example environment file |
| `.gitignore` | Git ignore patterns (includes config files) |
| `UPDATED_README.md` | Migration and setup guide |
| `CHANGELOG.md` | This file |

### 📝 Updated Files

| File | Changes |
|------|---------|
| `siya_free.py` | + ConfigManager, + Welcome screen, + Settings tab |
| `siya_advanced.py` | + ConfigManager, + API key prompt, + Validation |
| `siya.py` | + ConfigManager, + API key prompt, + Validation |
| `requirements.txt` | - python-dotenv, + requests |
| `.env` | Deprecated (kept for info only) |
| `README.md` | Updated with new setup instructions |

### 🔧 Technical Details

#### API Key Flow (FREE Version):
```
1. User runs siya_free.py
2. Check for existing config
3. If no config: Show welcome screen
4. User chooses Ollama or Groq
5. If Groq: Prompt for API key
6. Save choice to siya_config.json
7. Load main UI
```

#### API Key Flow (OpenAI Versions):
```
1. User runs siya.py or siya_advanced.py
2. Check for existing config
3. If no config: Show API key dialog
4. User enters OpenAI API key
5. Validate key (test API call)
6. If valid: Save to siya_openai_config.json
7. If invalid/no credits: Show error, exit
8. Load main UI
```

#### Config File Format (FREE):
```json
{
  "use_local_ai": true,
  "groq_api_key": "",
  "ollama_model": "llama2",
  "ollama_url": "http://localhost:11434"
}
```

#### Config File Format (OpenAI):
```json
{
  "openai_api_key": "sk-..."
}
```

### ⚠️ Breaking Changes

1. **`.env` file no longer used**
   - Migration: Run app, enter key in dialog
   - Old keys not automatically migrated
   - Need to re-enter API keys

2. **`python-dotenv` removed from requirements**
   - Migration: `pip install -r requirements.txt`
   - No code changes needed

3. **API keys must be entered through UI**
   - Can't set via environment variables anymore
   - Must use config files or UI dialogs

### 🔄 Migration Guide

#### From Version 1.0 to 2.0:

**Before:**
```bash
# Edit .env file
echo "OPENAI_API_KEY=sk-abc..." > .env

# Or edit code
GROQ_API_KEY = "gsk-xyz..."
```

**After:**
```bash
# Just run the app
python siya_free.py

# Enter API key in dialog (one time)
# Config saved automatically
```

**Steps:**
1. Backup your old API keys (from .env)
2. Run new version of Siya
3. Enter API key when prompted
4. Key saved in config JSON
5. Delete old .env (optional)

### 🐛 Bug Fixes

- Fixed error when OpenAI credits exhausted
- Better error messages for invalid API keys
- Proper handling of 401/429 errors
- Clear path to FREE alternative
- Validation before saving API keys

### ✨ New Features

#### User-Friendly Setup:
- Interactive welcome screens
- Step-by-step configuration
- Visual dialogs for API keys
- Helpful error messages
- Links to get API keys

#### Settings Management:
- Settings tab (FREE version)
- Change AI engine anytime
- Update API keys easily
- View current configuration
- No code editing needed

#### Security:
- API keys in separate files
- Keys added to .gitignore
- Masked display in UI
- Validation before use
- Safe to share code

### 📊 Comparison

| Feature | v1.0 | v2.0 |
|---------|------|------|
| API Keys | Hardcoded | User-entered |
| Setup | Edit code | UI dialogs |
| Config | .env file | JSON files |
| Security | Low | High |
| Shareable | No | Yes |
| User-friendly | No | Yes |
| Errors | Unclear | Clear messages |
| Migration | N/A | Guided |

---

## 🎯 Version 1.0 - Initial Release

### Features

#### Three Versions:
- `siya_free.py` - FREE with Ollama/Groq
- `siya_advanced.py` - OpenAI with voice & tasks
- `siya.py` - OpenAI basic version

#### Core Features:
- AI-powered chat
- Animated cat UI
- Task management (advanced/free)
- Voice input (advanced/basic)
- Text-to-speech (advanced/basic)
- Emoji cat (free) / ASCII cat (advanced/basic)

#### Setup:
- Edit .env file for OpenAI
- Edit code for Groq
- Manual configuration
- Limited error handling

---

## 🚀 Future Plans

### Version 2.1 (Planned):
- [ ] Export chat history
- [ ] Import/export tasks
- [ ] Custom cat emojis
- [ ] Theme customization
- [ ] Keyboard shortcuts
- [ ] Multi-language support

### Version 3.0 (Ideas):
- [ ] Plugin system
- [ ] Cloud sync
- [ ] Mobile companion app
- [ ] Voice wake word
- [ ] Calendar integration
- [ ] Email notifications

---

## 📞 Support

### Getting Help:

**For Setup Issues:**
1. Read `UPDATED_README.md`
2. Check `QUICKSTART.md`
3. See FAQ in `README.md`

**For Errors:**
1. Check error message carefully
2. Read `UPDATED_README.md` errors section
3. Delete config file and try again
4. Use FREE version if OpenAI has issues

**For Updates:**
1. Pull latest code
2. Run `pip install -r requirements.txt`
3. Delete old config files
4. Re-enter API keys

---

## 🙏 Credits

### Contributors:
- Development: Pratik
- AI Models: OpenAI, Groq, Ollama
- Community: Users like you!

### Technologies:
- Python
- tkinter (GUI)
- OpenAI API
- Groq API
- Ollama
- pyttsx3 (TTS)
- sounddevice (Audio)

---

**Current Version: 2.0**
**Release Date: 2024**
**Status: Stable**

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2024 | User-defined API keys, UI dialogs, Security |
| 1.0 | 2024 | Initial release, Three versions, Core features |

---

**See `UPDATED_README.md` for migration guide!**
**See `README.md` for complete documentation!**

😺 **Happy chatting with Siya!** ✨
