"""
Siya Floating - Reactive Cat Assistant with Real Task Execution
Features:
  - Always-on-top floating cat window
  - Draggable anywhere on screen
  - Expressive emotions & animations with your cat image
  - NO API KEYS REQUIRED - 100% local intelligence
  - Performs REAL tasks (open apps, math, files, weather, etc.)
  - Chat interface expandable with one click
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageDraw
import threading
from datetime import datetime
import json
from pathlib import Path
import os
import sys
import subprocess
import webbrowser
import math
import random
import platform
import urllib.request
import urllib.parse


CONFIG_FILE = Path("siya_floating_config.json")
TASKS_FILE = Path("siya_floating_tasks.json")
CAT_IMAGE_FILE = Path("cat_image.png")


class ConfigManager:
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.config = self.load_config()

    def load_config(self):
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "cat_size": 100,
            "position": {"x": None, "y": None},
            "opacity": 0.95,
            "tts_enabled": False,
            "sound_enabled": True,
            "auto_idle_animations": True
        }

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()


class TaskManager:
    def __init__(self):
        self.tasks_file = TASKS_FILE
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        return []

    def save_tasks(self):
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, description):
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "created": datetime.now().isoformat(),
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                return True
        return False

    def get_pending(self):
        return [t for t in self.tasks if not t["completed"]]


class ExpressiveCat:
    """Handles cat image with expressive emotions and animations"""
    def __init__(self, canvas, width=100, height=100):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.base_image = None
        self.current_photo = None
        self.image_id = None
        self.animation_active = False
        self._bounce_offset = 0
        self._blink_state = False
        self.load_image()

    def load_image(self):
        if CAT_IMAGE_FILE.exists():
            img = Image.open(CAT_IMAGE_FILE)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            self.base_image = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
        else:
            self.base_image = self._create_default_cat()
            self.base_image.save(CAT_IMAGE_FILE)
        self.show_normal()

    def _create_default_cat(self):
        size = (self.width, self.height)
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cx, cy = size[0] // 2, size[1] // 2
        r = int(min(size) * 0.38)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 200, 100), outline=(200, 150, 50), width=3)
        ear_w, ear_h = int(r * 0.45), int(r * 0.55)
        draw.polygon([(cx - r + ear_w // 2, cy - r), (cx - r, cy - r - ear_h),
                      (cx - r + ear_w * 2, cy - r + ear_h // 4)], fill=(255, 200, 100), outline=(200, 150, 50))
        draw.polygon([(cx + r - ear_w // 2, cy - r), (cx + r, cy - r - ear_h),
                      (cx + r - ear_w * 2, cy - r + ear_h // 4)], fill=(255, 200, 100), outline=(200, 150, 50))
        eye_r = int(r * 0.2)
        eye_y = cy - int(r * 0.1)
        draw.ellipse([cx - int(r * 0.45) - eye_r, eye_y - eye_r, cx - int(r * 0.45) + eye_r, eye_y + eye_r],
                     fill=(30, 30, 40), outline=(0, 0, 0))
        draw.ellipse([cx + int(r * 0.45) - eye_r, eye_y - eye_r, cx + int(r * 0.45) + eye_r, eye_y + eye_r],
                     fill=(30, 30, 40), outline=(0, 0, 0))
        hr = int(eye_r * 0.4)
        draw.ellipse([cx - int(r * 0.45) - hr + int(eye_r * 0.3), eye_y - hr,
                      cx - int(r * 0.45) + hr + int(eye_r * 0.3), eye_y + hr], fill=(255, 255, 255))
        draw.ellipse([cx + int(r * 0.45) - hr + int(eye_r * 0.3), eye_y - hr,
                      cx + int(r * 0.45) + hr + int(eye_r * 0.3), eye_y + hr], fill=(255, 255, 255))
        nose_w, nose_h = int(r * 0.22), int(r * 0.15)
        nose_y = cy + int(r * 0.15)
        draw.polygon([(cx, nose_y + nose_h), (cx - nose_w, nose_y - nose_h // 2),
                      (cx + nose_w, nose_y - nose_h // 2)], fill=(255, 120, 120))
        mouth_y = nose_y + nose_h + int(r * 0.1)
        draw.arc([cx - int(r * 0.25), nose_y + nose_h - int(r * 0.05),
                  cx, mouth_y + int(r * 0.05)], 0, 180, fill=(100, 60, 30), width=2)
        draw.arc([cx, nose_y + nose_h - int(r * 0.05),
                  cx + int(r * 0.25), mouth_y + int(r * 0.05)], 0, 180, fill=(100, 60, 30), width=2)
        for i, dy in enumerate([-int(r * 0.1), 0, int(r * 0.1)]):
            wy = cy + int(r * 0.12) + dy
            draw.line([(cx - r * 1.1, wy), (cx - r * 0.55, wy)], fill=(255, 255, 255), width=1)
            draw.line([(cx + r * 1.1, wy), (cx + r * 0.55, wy)], fill=(255, 255, 255), width=1)
        return img

    def _display(self, pil_image):
        self.current_photo = ImageTk.PhotoImage(pil_image)
        if self.image_id:
            self.canvas.itemconfig(self.image_id, image=self.current_photo)
        else:
            self.image_id = self.canvas.create_image(
                self.width // 2, self.height // 2, image=self.current_photo
            )

    def show_normal(self):
        if self.animation_active:
            return
        img = self.base_image.copy()
        if self._blink_state:
            img = self._draw_closed_eyes(img)
        self._display(img)

    def _draw_closed_eyes(self, img):
        draw = ImageDraw.Draw(img)
        w, h = img.size
        cx, cy = w // 2, h // 2
        r = int(min(w, h) * 0.38)
        eye_y = cy - int(r * 0.1)
        ex1 = cx - int(r * 0.45)
        ex2 = cx + int(r * 0.45)
        lw = int(r * 0.35)
        draw.line([(ex1 - lw // 2, eye_y), (ex1 + lw // 2, eye_y)], fill=(20, 20, 30), width=3)
        draw.line([(ex2 - lw // 2, eye_y), (ex2 + lw // 2, eye_y)], fill=(20, 20, 30), width=3)
        return img

    def set_mood(self, mood):
        if self.animation_active:
            return
        moods = {
            "happy": self._mood_happy,
            "thinking": self._mood_thinking,
            "speaking": self._mood_speaking,
            "excited": self._anim_excited,
            "loving": self._anim_loving,
            "error": self._anim_error,
            "sleepy": self._mood_sleepy,
            "surprised": self._mood_surprised,
            "wave": self._anim_wave
        }
        fn = moods.get(mood, self._mood_happy)
        fn()

    def _mood_happy(self):
        img = self.base_image.copy()
        self._add_glow(img, (0, 255, 150, 40))
        self._display(img)

    def _mood_thinking(self):
        img = self.base_image.copy()
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.85)
        img = img.filter(ImageFilter.SMOOTH)
        self._display(img)

    def _mood_speaking(self):
        img = self.base_image.copy()
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        self._add_glow(img, (0, 200, 255, 50))
        self._display(img)

    def _mood_sleepy(self):
        img = self._draw_closed_eyes(self.base_image.copy())
        draw = ImageDraw.Draw(img)
        w, h = img.size
        for i, ch in enumerate("zZz"):
            draw.text((w - 25 - i * 10, 10 + i * 8), ch, fill=(150, 150, 255))
        self._display(img)

    def _mood_surprised(self):
        img = self.base_image.copy()
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.3)
        self._add_glow(img, (255, 200, 0, 60))
        self._display(img)

    def _add_glow(self, img, color):
        glow = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)
        w, h = img.size
        gdraw.ellipse([0, 0, w, h], fill=color)
        glow = glow.filter(ImageFilter.GaussianBlur(radius=15))
        return Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB') if img.mode != 'RGBA' \
            else Image.alpha_composite(img, glow)

    def _anim_excited(self, count=0):
        self.animation_active = True
        if count >= 8:
            self.animation_active = False
            self.show_normal()
            return
        scale = 1.12 if count % 2 == 0 else 0.95
        img = self.base_image.copy()
        new_w = int(self.width * scale)
        new_h = int(self.height * scale)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        canvas_w = int(self.canvas.cget("width"))
        canvas_h = int(self.canvas.cget("height"))
        pos = (canvas_w // 2 - new_w // 2, canvas_h // 2 - new_h // 2)
        self._display(img)
        if self.image_id:
            self.canvas.coords(self.image_id, canvas_w // 2, canvas_h // 2 + (5 if count % 2 else -5))
        self.canvas.after(80, lambda: self._anim_excited(count + 1))

    def _anim_loving(self, count=0):
        self.animation_active = True
        if count >= 10:
            self.animation_active = False
            self.show_normal()
            return
        bright = 1.0 + (0.15 if count % 2 else 0)
        img = self.base_image.copy()
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(bright)
        if count % 2:
            img = self._add_hearts(img, count)
        self._display(img)
        self.canvas.after(120, lambda: self._anim_loving(count + 1))

    def _add_hearts(self, img, n):
        draw = ImageDraw.Draw(img)
        w, h = img.size
        hearts = [
            (w - 20, 15, (255, 100, 150)),
            (10, h - 30, (255, 80, 130)),
            (w - 30, h - 20, (255, 120, 170))
        ]
        for (hx, hy, c) in hearts[:min(3, n // 2 + 1)]:
            draw.text((hx, hy), "❤", fill=c)
        return img

    def _anim_error(self, count=0):
        self.animation_active = True
        if count >= 10:
            self.animation_active = False
            self.show_normal()
            return
        offset = 8 if count % 2 == 0 else -8
        if self.image_id:
            self.canvas.move(self.image_id, offset, 0)
        if count == 0:
            img = self.base_image.copy()
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.8)
            self._display(img)
        self.canvas.after(60, lambda: self._anim_error(count + 1))

    def _anim_wave(self, count=0):
        self.animation_active = True
        if count >= 12:
            self.animation_active = False
            self.show_normal()
            return
        tilt = 5 if count % 4 < 2 else -5
        img = self.base_image.copy()
        img = img.rotate(tilt, Image.Resampling.BILINEAR, expand=False)
        self._display(img)
        self.canvas.after(100, lambda: self._anim_wave(count + 1))


class TaskExecutor:
    """Executes real system tasks - NO API KEYS NEEDED"""
    @staticmethod
    def execute(command_text):
        text = command_text.lower().strip()
        results = []
        executed = False

        # 1. System info / Time
        if any(w in text for w in ["time", "what time", "current time"]):
            now = datetime.now()
            results.append(("time", f"🕐 Current time: {now.strftime('%I:%M:%S %p')}"))
            executed = True
        if any(w in text for w in ["date", "today", "what day"]):
            now = datetime.now()
            results.append(("date", f"📅 Today is: {now.strftime('%A, %B %d, %Y')}"))
            executed = True
        if "day of week" in text:
            results.append(("day", f"📆 It's {datetime.now().strftime('%A')}!"))
            executed = True

        # 2. Math calculations
        calc_result = TaskExecutor._try_math(text)
        if calc_result:
            results.append(("math", f"🧮 {calc_result}"))
            executed = True

        # 3. Open applications (Windows)
        app_map = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "calc": "calc.exe",
            "paint": "mspaint.exe",
            "wordpad": "write.exe",
            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",
            "files": "explorer.exe",
            "command prompt": "cmd.exe",
            "cmd": "cmd.exe",
            "terminal": "cmd.exe",
            "powershell": "powershell.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",
            "settings": "ms-settings:",
            "browser": "chrome.exe",
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "firefox": "firefox.exe",
            "media player": "wmplayer.exe",
            "music": "wmplayer.exe",
            "camera": "microsoft.windows.camera:",
        }
        for key, exe in app_map.items():
            if f"open {key}" in text or f"start {key}" in text or f"launch {key}" in text:
                try:
                    if exe.startswith("ms-") or ":" in exe:
                        os.startfile(exe) if platform.system() == "Windows" else webbrowser.open(exe)
                    else:
                        subprocess.Popen(exe, shell=True)
                    results.append(("app", f"✅ Opened {key.title()}!"))
                except Exception as e:
                    results.append(("app", f"😿 Could not open {key}: {e}"))
                executed = True
                break

        # 4. Web search / open websites
        if any(w in text for w in ["search for", "google for", "look up", "search"]):
            query = text
            for sw in ["search for", "google for", "look up", "search"]:
                query = query.replace(sw, "")
            query = query.strip()
            if query:
                url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                webbrowser.open(url)
                results.append(("web", f"🔍 Searching Google for: '{query}'"))
                executed = True

        if "open youtube" in text or "go to youtube" in text:
            webbrowser.open("https://youtube.com")
            results.append(("web", "📺 Opening YouTube!"))
            executed = True
        if "open github" in text or "go to github" in text:
            webbrowser.open("https://github.com")
            results.append(("web", "💻 Opening GitHub!"))
            executed = True
        if ("open website" in text or "go to" in text or "visit" in text) and ("http" in text or ".com" in text or ".org" in text or ".net" in text):
            words = text.split()
            url = None
            for w in words:
                if "." in w and not w.endswith(("a", "the", "to", "for", "of", "in", "on", "at", "and", "is", "it")):
                    if not w.startswith("http"):
                        w = "https://" + w
                    url = w
                    break
            if url:
                webbrowser.open(url)
                results.append(("web", f"🌐 Opening {url}"))
                executed = True

        # 5. Weather (using wttr.in - free, no key)
        if any(w in text for w in ["weather", "temperature", "forecast"]):
            city = "current"
            if "in " in text:
                city = text.split("in ", 1)[1].strip().split()[0]
            elif "for " in text:
                city = text.split("for ", 1)[1].strip().split()[0]
            try:
                url = f"https://wttr.in/{city}?format=%C+%t+%w"
                with urllib.request.urlopen(url, timeout=5) as resp:
                    weather = resp.read().decode('utf-8').strip()
                results.append(("weather", f"🌤️ Weather in {city}: {weather}"))
            except:
                results.append(("weather", "🌤️ Weather: Unable to fetch (offline mode)"))
            executed = True

        # 6. File operations
        if "list files" in text or "show files" in text or "what's in this folder" in text or "current directory" in text:
            cwd = os.getcwd()
            files = os.listdir(cwd)
            file_list = "\n".join(f"- {f}" for f in files[:15])
            extra = f"\n... and {len(files) - 15} more" if len(files) > 15 else ""
            results.append(("files", f"📂 Files in:\n{cwd}\n\n{file_list}{extra}"))
            executed = True

        if "create file" in text or "make file" in text:
            name = "new_file.txt"
            words = text.split()
            for i, w in enumerate(words):
                if w in ["file", "named"] and i + 1 < len(words):
                    fname = words[i + 1].strip('"').strip("'")
                    if "." in fname:
                        name = fname
                    break
            try:
                Path(name).touch()
                results.append(("files", f"📄 Created file: {name}"))
            except Exception as e:
                results.append(("files", f"❌ Could not create: {e}"))
            executed = True

        if "create folder" in text or "make directory" in text or "new folder" in text:
            name = "new_folder"
            words = text.split()
            for i, w in enumerate(words):
                if w in ["folder", "directory", "named"] and i + 1 < len(words):
                    fname = words[i + 1].strip('"').strip("'")
                    name = fname
                    break
            try:
                Path(name).mkdir(exist_ok=True)
                results.append(("files", f"📁 Created folder: {name}"))
            except Exception as e:
                results.append(("files", f"❌ Could not create folder: {e}"))
            executed = True

        # 7. Jokes & fun
        if any(w in text for w in ["joke", "tell me a joke", "funny"]):
            jokes = [
                "Why don't cats play poker in the jungle? Too many cheetahs! 😹",
                "What do you call a cat that likes to bowl? A purr-fect game! 🎳",
                "Why did the cat sit on the computer? To keep an eye on the mouse! 🖱️",
                "What's a cat's favorite color? Purr-ple! 💜",
                "Why are cats so good at video games? They have nine lives! 🎮",
                "What do you call a cat that can sing? A purr-former! 🎤",
            ]
            results.append(("fun", f"😂 {random.choice(jokes)}"))
            executed = True

        if "quote" in text or "inspire me" in text or "motivation" in text:
            quotes = [
                "🌟 The secret of getting ahead is getting started. - Mark Twain",
                "🌟 Your time is limited, don't waste it living someone else's life. - Steve Jobs",
                "🌟 The only way to do great work is to love what you do. - Steve Jobs",
                "🌟 In the middle of difficulty lies opportunity. - Albert Einstein",
                "🌟 Believe you can and you're halfway there. - Theodore Roosevelt",
                "🌟 Every purr-fect achievement was once considered impossible. 🐱",
            ]
            results.append(("quote", random.choice(quotes)))
            executed = True

        if any(w in text for w in ["flip a coin", "heads or tails", "toss a coin"]):
            result = random.choice(["Heads!", "Tails!"])
            results.append(("fun", f"🪙 {result}"))
            executed = True

        if any(w in text for w in ["roll dice", "roll a die", "dice"]):
            n = random.randint(1, 6)
            results.append(("fun", f"🎲 Rolled a {n}!"))
            executed = True

        # 8. Conversational (fallback rule-based)
        if not executed:
            results.append(("chat", TaskExecutor._chat_response(text)))

        return results

    @staticmethod
    def _try_math(text):
        import re
        # Extract simple math expressions
        expr_patterns = [
            r'what is ([\d+\-*/().%\s]+)',
            r'calculate ([\d+\-*/().%\s]+)',
            r'solve ([\d+\-*/().%\s]+)',
            r'([\d]+\s*[+\-*/%]\s*[\d]+(?:\s*[+\-*/%]\s*[\d]+)*)',
        ]
        for pat in expr_patterns:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                expr = match.group(1).strip()
                try:
                    safe_chars = set("0123456789+-*/().% ")
                    if all(c in safe_chars for c in expr):
                        result = eval(expr)
                        return f"{expr} = {result}"
                except:
                    pass
        return None

    @staticmethod
    def _chat_response(text):
        t = text.lower()
        greetings = {
            "hi": "Meow! Hi there! 😺 How can I help you today?",
            "hello": "Hello! 🐱 I'm Siya! Ready to help with anything!",
            "hey": "Hey hey! 😸 What's on your mind?",
            "good morning": "Good morning! ☀️ Hope your day is purr-fect!",
            "good afternoon": "Good afternoon! 🌤️ What can I do for you?",
            "good evening": "Good evening! 🌙 Need any help tonight?",
        }
        for key, resp in greetings.items():
            if key in t:
                return resp

        if "how are you" in t:
            return "I'm doing purr-fectly! 😻 Thanks for asking! How about you?"

        if "your name" in t or "who are you" in t:
            return "I'm Siya! 🐱 Your floating reactive cat assistant! I'm here 24/7 to help with everything!"

        if "what can you do" in t or "help" in t or "capabilities" in t:
            return ("✨ I can do MANY things! ✨\n\n"
                    "📅 Time & Date: Ask 'what time is it'\n"
                    "🧮 Math: Ask 'what is 25 * 17'\n"
                    "🖥️ Open Apps: 'open notepad', 'open chrome', 'open calculator'\n"
                    "🔍 Web Search: 'search for python tutorials'\n"
                    "🌐 Visit Sites: 'open youtube.com', 'go to github'\n"
                    "🌤️ Weather: 'what is the weather in tokyo'\n"
                    "📁 Files: 'list files', 'create file notes.txt', 'new folder projects'\n"
                    "🎲 Fun: 'tell me a joke', 'flip a coin', 'roll dice', 'give me a quote'\n"
                    "✅ Tasks: 'add task buy groceries', 'show tasks'\n\n"
                    "Just ask! Meow! 😽")

        if "thank" in t:
            return "You're very welcome! 😻 Anytime you need me, I'm here! *purrs*"

        if "bye" in t or "goodbye" in t or "see you" in t:
            return "Bye bye! 👋 I'll be right here waiting! *waves paw* 🐾"

        if "love you" in t or "i love u" in t:
            return "Aww! I love you too! 💖 *happy purring* 😻💕"

        if "cat" in t:
            return "Did someone say CAT? That's ME! 🐱 Meow meow! 😸"

        if "hungry" in t:
            return "Are you hungry? 🍽️ Maybe open a recipe website with: 'search for easy recipes'!"

        if "tired" in t:
            return "Aww, time to rest! 😴 Remember to take breaks! Your cat cares about you! 💤"

        if "happy" in t:
            return "Yay! Your happiness makes me happy too! 🎉 *does happy bounce* 😸"

        if "sad" in t or "upset" in t or "depressed" in t:
            return "Oh no... 💔 Sending you BIG kitty hugs! 🤗 Want me to tell you a joke? Just ask! ❤️"

        # Default friendly responses
        defaults = [
            f"Meow! 😺 I heard: '{text}'. Let me help! Try asking 'what can you do' for my full list of powers!",
            f"🐱 Interesting! You said: '{text}'. I can open apps, do math, search web, and more! Ask 'help'!",
            f"😸 Got it! '{text}' - remember, I'm a cat of many talents! Math, apps, web, files... ask away!",
        ]
        return random.choice(defaults)


class FloatingCatUI:
    def __init__(self, root):
        self.root = root
        self.config = ConfigManager()
        self.task_mgr = TaskManager()
        self.executor = TaskExecutor()

        # Floating window setup
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        try:
            self.root.attributes('-alpha', self.config.get("opacity", 0.95))
        except:
            pass

        cat_size = self.config.get("cat_size", 100)
        self.cat_w = cat_size
        self.cat_h = cat_size
        self.expanded = False
        self.drag_data = {"x": 0, "y": 0}
        self.chat_w = 380
        self.chat_h = 480

        # Position window
        self._position_window()
        self.root.configure(bg="black")
        try:
            self.root.wm_attributes('-transparentcolor', 'black')
        except:
            self.root.configure(bg="#222")

        self._build_ui()
        self._start_idle_animations()
        self.cat.set_mood("wave")

    def _position_window(self):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        pos = self.config.get("position", {})
        px = pos.get("x")
        py = pos.get("y")
        if px is None or py is None:
            px = sw - self.cat_w - 40
            py = sh - self.cat_h - 100
        self.root.geometry(f"{self.cat_w}x{self.cat_h}+{px}+{py}")

    def _build_ui(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg="black", highlightthickness=0)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Cat canvas - always shown
        self.cat_canvas = tk.Canvas(
            self.main_frame, width=self.cat_w, height=self.cat_h,
            bg="black", highlightthickness=0, cursor="hand2"
        )
        self.cat_canvas.pack()

        self.cat = ExpressiveCat(self.cat_canvas, self.cat_w, self.cat_h)

        # Drag bindings
        for widget in [self.cat_canvas, self.main_frame]:
            widget.bind('<Button-1>', self._on_drag_start)
            widget.bind('<B1-Motion>', self._on_drag_move)
            widget.bind('<ButtonRelease-1>', self._on_drag_end)

        # Click to expand (single click without drag)
        self._drag_moved = False
        self.cat_canvas.bind('<ButtonRelease-1>', self._on_cat_click)

        # Context menu
        self._build_context_menu()

        # Chat panel (initially hidden)
        self.chat_frame = None

    def _build_context_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0, bg="#1a1a2e", fg="white",
                            activebackground="#00d4ff", activeforeground="#1a1a2e")
        self.menu.add_command(label="💬 Chat / Ask", command=self._toggle_chat)
        self.menu.add_command(label="✅ Add Task", command=self._quick_add_task)
        self.menu.add_command(label="📋 Show Tasks", command=self._show_tasks_popup)
        self.menu.add_separator()
        self.menu.add_command(label="🐱 Make Bigger", command=lambda: self._resize_cat(120))
        self.menu.add_command(label="🐾 Make Smaller", command=lambda: self._resize_cat(70))
        self.menu.add_separator()
        self.menu.add_command(label="⚙️ Help / Commands", command=self._show_help)
        self.menu.add_separator()
        self.menu.add_command(label="❌ Exit Siya", command=self._quit)
        self.cat_canvas.bind("<Button-3>", self._show_menu)

    def _show_menu(self, event):
        self._drag_moved = True
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def _on_drag_start(self, event):
        self._drag_moved = False
        self.drag_data["x"] = event.x_root - self.root.winfo_x()
        self.drag_data["y"] = event.y_root - self.root.winfo_y()

    def _on_drag_move(self, event):
        self._drag_moved = True
        x = event.x_root - self.drag_data["x"]
        y = event.y_root - self.drag_data["y"]
        gw = int(self.root.geometry().split('x')[0])
        self.root.geometry(f"+{x}+{y}")

    def _on_drag_end(self, event):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.config.set("position", {"x": x, "y": y})

    def _on_cat_click(self, event):
        if not self._drag_moved:
            self.cat.set_mood("wave")
            self._toggle_chat()
        self._drag_moved = False

    def _resize_cat(self, new_size):
        self.cat_w = new_size
        self.cat_h = new_size
        self.config.set("cat_size", new_size)
        self.cat_canvas.config(width=new_size, height=new_size)
        self.cat.width = new_size
        self.cat.height = new_size
        self.cat.load_image()
        if not self.expanded:
            self.root.geometry(f"{new_size}x{new_size}")
        else:
            self._update_expanded_geometry()

    def _start_idle_animations(self):
        if not self.config.get("auto_idle_animations", True):
            return

        def blink_loop():
            if not self.cat.animation_active and not self.expanded:
                self.cat._blink_state = True
                self.cat.show_normal()
                self.root.after(150, lambda: (setattr(self.cat, '_blink_state', False), self.cat.show_normal()))
            self.root.after(random.randint(4000, 8000), blink_loop)

        def idle_mood_loop():
            if not self.cat.animation_active and not self.expanded:
                moods = ["happy", "happy", "happy", None]
                m = random.choice(moods)
                if m:
                    self.cat.set_mood(m)
            self.root.after(random.randint(15000, 30000), idle_mood_loop)

        self.root.after(3000, blink_loop)
        self.root.after(10000, idle_mood_loop)

    def _toggle_chat(self):
        if self.expanded:
            self._collapse_chat()
        else:
            self._expand_chat()

    def _expand_chat(self):
        self.expanded = True
        self.cat.set_mood("excited")
        self._update_expanded_geometry()

        if self.chat_frame is None:
            self._build_chat_panel()

        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 4))
        self.text_entry.focus_set()

    def _update_expanded_geometry(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        total_w = max(self.cat_w, self.chat_w)
        total_h = self.cat_h + self.chat_h + 10
        if x + total_w > sw:
            x = sw - total_w - 10
        if y + total_h > sh:
            y = sh - total_h - 50
        self.root.geometry(f"{total_w}x{total_h}+{x}+{y}")

    def _collapse_chat(self):
        self.expanded = False
        if self.chat_frame:
            self.chat_frame.pack_forget()
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.root.geometry(f"{self.cat_w}x{self.cat_h}+{x}+{y}")
        self.cat.set_mood("happy")

    def _build_chat_panel(self):
        self.chat_frame = tk.Frame(self.main_frame, bg="#1a1a2e", bd=2, relief=tk.RAISED)

        # Header bar
        header = tk.Frame(self.chat_frame, bg="#16213e", height=30)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text="🐱 Siya Chat", font=("Arial", 9, "bold"),
                 bg="#16213e", fg="#00d4ff").pack(side=tk.LEFT, padx=8)

        tk.Button(header, text="_", font=("Arial", 8, "bold"),
                  bg="#e94560", fg="white", relief=tk.FLAT, cursor="hand2",
                  command=self._collapse_chat, width=2).pack(side=tk.RIGHT, padx=4)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame, wrap=tk.WORD, font=("Consolas", 9),
            bg="#0f3460", fg="#e9ecef", insertbackground="#00d4ff",
            relief=tk.FLAT, padx=6, pady=6, height=18
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.chat_display.config(state=tk.DISABLED)

        # Quick action buttons
        quick = tk.Frame(self.chat_frame, bg="#1a1a2e")
        quick.pack(fill=tk.X, padx=4, pady=(0, 2))

        quick_btns = [
            ("⏰ Time", lambda: self._send_text("what time is it")),
            ("📅 Date", lambda: self._send_text("what is today's date")),
            ("🧮 Calc", lambda: self._quick_calc()),
            ("🌤️ Weather", lambda: self._send_text("weather")),
            ("😂 Joke", lambda: self._send_text("tell me a joke")),
            ("❓ Help", lambda: self._send_text("help")),
        ]
        for label, cmd in quick_btns:
            tk.Button(quick, text=label, font=("Arial", 8, "bold"),
                      bg="#16213e", fg="#00d4ff", relief=tk.FLAT, cursor="hand2",
                      command=cmd, padx=4).pack(side=tk.LEFT, padx=1, pady=1)

        # Input row
        input_row = tk.Frame(self.chat_frame, bg="#1a1a2e")
        input_row.pack(fill=tk.X, padx=4, pady=4)

        self.text_entry = tk.Entry(
            input_row, font=("Arial", 10), bg="#0f3460", fg="white",
            insertbackground="#00d4ff", relief=tk.FLAT
        )
        self.text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4), ipady=4)
        self.text_entry.bind('<Return>', lambda e: self._on_send())
        self.text_entry.bind('<Shift-Return>', lambda e: None)

        tk.Button(input_row, text="Send", font=("Arial", 9, "bold"),
                  bg="#00d4ff", fg="#1a1a2e", relief=tk.FLAT, cursor="hand2",
                  command=self._on_send, padx=10).pack(side=tk.RIGHT, ipady=2)

        # Welcome
        self._add_msg("Siya", "Meow! 🐱 I'm your floating cat assistant! Click me or right-click for menu. Try: 'what can you do'")

    def _quick_calc(self):
        expr = simpledialog.askstring("Calculator", "Enter math expression (e.g. 12 * 17):", parent=self.root)
        if expr:
            self._send_text(f"calculate {expr}")

    def _quick_add_task(self):
        desc = simpledialog.askstring("Add Task", "Task description:", parent=self.root)
        if desc:
            t = self.task_mgr.add_task(desc)
            self.cat.set_mood("excited")
            messagebox.showinfo("Task Added", f"✅ Task #{t['id']} added:\n{desc}")
            self.root.after(2000, lambda: self.cat.set_mood("happy"))

    def _show_tasks_popup(self):
        pending = self.task_mgr.get_pending()
        top = tk.Toplevel(self.root)
        top.title("📋 Pending Tasks")
        top.geometry("350x400")
        top.configure(bg="#1a1a2e")
        top.attributes('-topmost', True)
        tk.Label(top, text=f"📋 Tasks ({len(pending)} pending)",
                 font=("Arial", 12, "bold"), bg="#1a1a2e", fg="#00d4ff").pack(pady=8)
        frame = tk.Frame(top, bg="#1a1a2e")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        if not pending:
            tk.Label(frame, text="🎉 All caught up! No pending tasks!",
                     font=("Arial", 10), bg="#1a1a2e", fg="#00ff88").pack(pady=20)
        else:
            for task in pending:
                row = tk.Frame(frame, bg="#0f3460", relief=tk.RAISED, bd=1)
                row.pack(fill=tk.X, pady=2)
                tk.Label(row, text=f"#{task['id']} {task['description']}",
                         font=("Arial", 9), bg="#0f3460", fg="white", anchor="w",
                         wraplength=250).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6, pady=6)
                def done(tid=task["id"]):
                    self.task_mgr.complete_task(tid)
                    top.destroy()
                    self.cat.set_mood("loving")
                    self.root.after(2000, lambda: self.cat.set_mood("happy"))
                    self._show_tasks_popup()
                tk.Button(row, text="✓", font=("Arial", 9, "bold"),
                          bg="#00ff88", fg="#1a1a2e", relief=tk.FLAT,
                          cursor="hand2", width=3, command=done).pack(side=tk.RIGHT, padx=4, pady=3)

    def _show_help(self):
        help_text = (
            "🐱 SIYA - Floating Cat Commands 🐱\n"
            "=" * 35 + "\n\n"
            "⏰ TIME & DATE\n"
            "  • what time is it\n"
            "  • what's today's date\n\n"
            "🧮 MATH\n"
            "  • what is 25 * 17\n"
            "  • calculate 15% of 200\n\n"
            "🖥️ OPEN APPS (Windows)\n"
            "  • open notepad / calculator / paint\n"
            "  • open chrome / edge / firefox\n"
            "  • open explorer / cmd / settings\n\n"
            "🔍 WEB\n"
            "  • search for python tutorials\n"
            "  • open youtube.com\n"
            "  • go to github.com\n\n"
            "🌤️ WEATHER\n"
            "  • weather\n"
            "  • weather in tokyo\n\n"
            "📁 FILES\n"
            "  • list files\n"
            "  • create file notes.txt\n"
            "  • new folder projects\n\n"
            "🎲 FUN\n"
            "  • tell me a joke\n"
            "  • flip a coin / roll dice\n"
            "  • give me a quote\n\n"
            "✅ TASKS\n"
            "  • add task [description]\n"
            "  • show tasks\n\n"
            "💡 Right-click cat for MENU!\n"
            "💡 Drag cat anywhere!\n"
            "💡 Click cat to open chat!"
        )
        top = tk.Toplevel(self.root)
        top.title("❓ Siya Help")
        top.geometry("420x550")
        top.configure(bg="#1a1a2e")
        top.attributes('-topmost', True)
        tk.Label(top, text="🐱 Siya Command Reference",
                 font=("Arial", 14, "bold"), bg="#1a1a2e", fg="#00d4ff").pack(pady=10)
        txt = scrolledtext.ScrolledText(top, font=("Consolas", 9),
                                        bg="#0f3460", fg="white", wrap=tk.WORD, padx=10, pady=10)
        txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        txt.insert(tk.END, help_text)
        txt.config(state=tk.DISABLED)

    def _send_text(self, text):
        if not self.expanded:
            self._expand_chat()
            self.root.after(100, lambda: self._send_text(text))
            return
        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, text)
        self._on_send()

    def _on_send(self):
        user_text = self.text_entry.get().strip()
        if not user_text:
            return
        self.text_entry.delete(0, tk.END)
        threading.Thread(target=self._process, args=(user_text,), daemon=True).start()

    def _process(self, user_text):
        self._add_msg("You", user_text)
        self.cat.set_mood("thinking")

        # Task commands
        user_lower = user_text.lower()
        if any(k in user_lower for k in ["add task", "create task", "new task", "remind me"]):
            for w in ["add task", "create task", "new task", "remind me to", "remind me"]:
                user_lower = user_lower.replace(w, "")
            desc = user_lower.strip()
            if desc:
                self.task_mgr.add_task(desc)
                self.root.after(0, lambda: self._add_msg("Siya", f"✅ Task added: '{desc}'"))
                self.cat.set_mood("excited")
            else:
                self.root.after(0, lambda: self._add_msg("Siya", "📝 What task would you like to add?"))
            self.root.after(3000, lambda: self.cat.set_mood("happy"))
            return

        if "show task" in user_lower or "my task" in user_lower or "pending task" in user_lower:
            pending = self.task_mgr.get_pending()
            if pending:
                msg = "📋 Pending Tasks:\n" + "\n".join(f"  #{t['id']}. {t['description']}" for t in pending)
            else:
                msg = "🎉 No pending tasks! All caught up!"
            self.root.after(0, lambda: self._add_msg("Siya", msg))
            self.cat.set_mood("happy")
            return

        if "complete task" in user_lower or "done task" in user_lower or "finish task" in user_lower:
            import re
            num_match = re.search(r'\d+', user_lower)
            if num_match:
                tid = int(num_match.group())
                if self.task_mgr.complete_task(tid):
                    self.root.after(0, lambda: self._add_msg("Siya", f"🎉 Task #{tid} completed! Great job!"))
                    self.cat.set_mood("loving")
                else:
                    self.root.after(0, lambda: self._add_msg("Siya", f"😿 Task #{tid} not found."))
                    self.cat.set_mood("error")
            else:
                self.root.after(0, lambda: self._add_msg("Siya", "Which task? Say: 'complete task 3'"))
            self.root.after(3000, lambda: self.cat.set_mood("happy"))
            return

        # Execute tasks
        results = self.executor.execute(user_text)
        types_seen = set()
        parts = []
        for rtype, rmsg in results:
            if rtype not in types_seen or rtype == "chat":
                parts.append(rmsg)
                types_seen.add(rtype)
        final = "\n\n".join(parts) if parts else "Meow! 😺"

        # Set mood based on result types
        mood_map = {"error": "error", "excited": "excited", "loving": "loving",
                    "fun": "excited", "quote": "loving", "math": "speaking",
                    "weather": "speaking", "app": "excited"}
        picked_mood = "speaking"
        for rt, _ in results:
            if rt in mood_map:
                picked_mood = mood_map[rt]
                break

        self.cat.set_mood(picked_mood)
        self.root.after(0, lambda: self._add_msg("Siya", final))
        self.root.after(3500, lambda: self.cat.set_mood("happy"))

    def _add_msg(self, sender, message):
        if not hasattr(self, 'chat_display'):
            return
        self.chat_display.config(state=tk.NORMAL)
        ts = datetime.now().strftime("%H:%M")
        if sender == "You":
            self.chat_display.insert(tk.END, f"\n[{ts}] 👤 You:\n", "u")
            self.chat_display.insert(tk.END, f"{message}\n", "um")
        else:
            self.chat_display.insert(tk.END, f"\n[{ts}] 🐱 Siya:\n", "s")
            self.chat_display.insert(tk.END, f"{message}\n", "sm")
        self.chat_display.tag_config("u", foreground="#00d4ff", font=("Arial", 9, "bold"))
        self.chat_display.tag_config("um", foreground="#ffffff")
        self.chat_display.tag_config("s", foreground="#00ff88", font=("Arial", 9, "bold"))
        self.chat_display.tag_config("sm", foreground="#ecf0f1")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def _quit(self):
        if messagebox.askyesno("Exit Siya", "Are you sure you want to exit? 🐱"):
            self.root.destroy()


def main():
    root = tk.Tk()
    app = FloatingCatUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
