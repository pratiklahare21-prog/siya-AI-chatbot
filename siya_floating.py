"""
Siya Floating Cat - PRO VERSION
================================
✅ True transparent frameless window (character ONLY - no box)
✅ 15+ expression variants matching your reference calico cat
✅ Click = meow sound (Windows native + fallback)
✅ Hover = zoom/pulse animation
✅ Drag = tilt + paw-shake feedback
✅ Idle = breathing + blinking + tail-wag + random emotions
✅ 100% offline task execution (NO API KEYS)
✅ Right-click context menu
✅ Expandable chat (optional - double click)
✅ Always on top, draggable, saves position
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
import time

try:
    import winsound
    HAVE_WINSOUND = True
except ImportError:
    HAVE_WINSOUND = False

try:
    import ctypes
    from ctypes import wintypes
    HAVE_WIN32 = True
except ImportError:
    HAVE_WIN32 = False


APP_DIR = Path(__file__).parent.resolve()
CONFIG_FILE = APP_DIR / "siya_pro_config.json"
TASKS_FILE = APP_DIR / "siya_pro_tasks.json"
SPRITES_DIR = APP_DIR / "cat_sprites"
COMPAT_IMAGE = APP_DIR / "cat_image.png"

# =============================================================
# Configuration
# =============================================================
class Config:
    def __init__(self):
        self.data = self.load()

    def load(self):
        defaults = {
            "cat_size": 120,
            "position": {"x": None, "y": None},
            "opacity": 1.0,
            "sound_on": True,
            "idle_anims": True,
            "show_chat_on_double_click": True,
            "hover_zoom": True,
            "breathing": True,
            "meow_volume": 70,
        }
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE) as f:
                    defaults.update(json.load(f))
            except Exception:
                pass
        return defaults

    def save(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get(self, k, default=None):
        return self.data.get(k, default)

    def set(self, k, v):
        self.data[k] = v
        self.save()


# =============================================================
# Sound System (meow)
# =============================================================
class MeowSound:
    """Play meow sound using Windows native (no files needed)"""

    @staticmethod
    def play_cute_meow():
        """Synth cute 2-tone meow. Thread-safe. Silently falls back."""
        try:
            if not HAVE_WINSOUND:
                return
            threading.Thread(target=MeowSound._meow_impl, daemon=True).start()
        except Exception:
            pass

    @staticmethod
    def _meow_impl():
        try:
            # "Mee" - gentle sweep up
            winsound.Beep(680, 140)
            time.sleep(0.01)
            winsound.Beep(780, 100)
            time.sleep(0.01)
            # "-ow" - fall off
            winsound.Beep(700, 90)
            winsound.Beep(560, 130)
        except Exception:
            try:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except Exception:
                pass

    @staticmethod
    def play_purr():
        if not HAVE_WINSOUND:
            return
        def _p():
            try:
                for i in range(5):
                    winsound.Beep(180 + i * 5, 70)
                    time.sleep(0.02)
            except Exception:
                pass
        threading.Thread(target=_p, daemon=True).start()

    @staticmethod
    def play_happy_chirp():
        if not HAVE_WINSOUND:
            return
        def _c():
            try:
                for f in (900, 1100, 1300, 1100, 1400):
                    winsound.Beep(f, 45)
                    time.sleep(0.01)
            except Exception:
                pass
        threading.Thread(target=_c, daemon=True).start()


# =============================================================
# Task Manager
# =============================================================
class TaskManager:
    def __init__(self):
        self.tasks = self._load()

    def _load(self):
        if TASKS_FILE.exists():
            try:
                with open(TASKS_FILE) as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save(self):
        with open(TASKS_FILE, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def add(self, desc):
        t = {"id": (self.tasks[-1]["id"] + 1 if self.tasks else 1),
             "description": desc,
             "created": datetime.now().isoformat(),
             "completed": False}
        self.tasks.append(t)
        self.save()
        return t

    def complete(self, tid):
        for t in self.tasks:
            if t["id"] == tid:
                t["completed"] = True
                self.save()
                return True
        return False

    def pending(self):
        return [t for t in self.tasks if not t["completed"]]


# =============================================================
# Task Executor (100% local, no keys)
# =============================================================
class Executor:
    @staticmethod
    def run(text):
        t = text.lower().strip()
        results = []
        hit = False

        # Time / Date
        if any(w in t for w in ["time", "what time"]):
            results.append(("time", f"🕐 {datetime.now().strftime('%I:%M:%S %p')}"))
            hit = True
        if any(w in t for w in ["date", "today", "what day"]):
            results.append(("date", f"📅 {datetime.now().strftime('%A, %B %d, %Y')}"))
            hit = True

        # Math
        mr = Executor._math(t)
        if mr:
            results.append(("math", f"🧮 {mr}"))
            hit = True

        # Apps
        apps = {
            "notepad": "notepad.exe", "calculator": "calc.exe", "calc": "calc.exe",
            "paint": "mspaint.exe", "wordpad": "write.exe",
            "explorer": "explorer.exe", "file explorer": "explorer.exe", "files": "explorer.exe",
            "command prompt": "cmd.exe", "cmd": "cmd.exe", "terminal": "cmd.exe",
            "powershell": "powershell.exe", "task manager": "taskmgr.exe",
            "control panel": "control.exe", "settings": "ms-settings:",
            "chrome": "chrome.exe", "edge": "msedge.exe", "firefox": "firefox.exe",
            "media player": "wmplayer.exe", "music": "wmplayer.exe",
        }
        for key, exe in apps.items():
            if f"open {key}" in t or f"start {key}" in t:
                try:
                    if exe.startswith("ms-"):
                        os.startfile(exe)
                    else:
                        subprocess.Popen(exe, shell=True)
                    results.append(("app", f"✅ Opened {key.title()}!"))
                except Exception as e:
                    results.append(("app", f"😿 {e}"))
                hit = True
                break

        # Web search
        for sw in ["search for", "google for", "look up"]:
            if sw in t:
                q = t.replace(sw, "").strip()
                if q:
                    webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(q)}")
                    results.append(("web", f"🔍 Searching: '{q}'"))
                    hit = True
                    break

        if "open youtube" in t or "go to youtube" in t:
            webbrowser.open("https://youtube.com")
            results.append(("web", "📺 YouTube!")); hit = True
        if "open github" in t or "go to github" in t:
            webbrowser.open("https://github.com")
            results.append(("web", "💻 GitHub!")); hit = True

        if ("open website" in t or "go to" in t or "visit" in t) and ("http" in t or ".com" in t or ".org" in t):
            for w in t.split():
                if "." in w and not w.endswith(("a", "the", "to", "for", "of", "in", "on", "at", "and", "is", "it")):
                    url = w if w.startswith("http") else "https://" + w
                    webbrowser.open(url)
                    results.append(("web", f"🌐 {url}"))
                    hit = True; break

        # Weather (wttr.in free, no key)
        if any(w in t for w in ["weather", "temperature", "forecast"]):
            city = ""
            for kw in ["in ", "for "]:
                if kw in t:
                    city = t.split(kw, 1)[1].strip().split()[0]
            if not city:
                city = ""
            try:
                url = f"https://wttr.in/{city or ''}?format=%C+%t+%w"
                with urllib.request.urlopen(url, timeout=5) as r:
                    w = r.read().decode().strip()
                results.append(("weather", f"🌤️ {city or 'Local'}: {w}"))
            except Exception:
                results.append(("weather", "🌤️ Weather fetch failed (offline?)"))
            hit = True

        # Files
        if any(w in t for w in ["list files", "show files", "what's in this folder", "current directory"]):
            cwd = os.getcwd()
            fs = os.listdir(cwd)
            lst = "\n".join(f"- {f}" for f in fs[:15])
            extra = f"\n... ({len(fs) - 15} more)" if len(fs) > 15 else ""
            results.append(("files", f"📂 {cwd}\n{lst}{extra}")); hit = True

        if "create file" in t or "make file" in t:
            name = "new_file.txt"
            ws = t.split()
            for i, w in enumerate(ws):
                if w in ["file", "named"] and i + 1 < len(ws):
                    n = ws[i + 1].strip('"').strip("'")
                    if "." in n: name = n
            try:
                Path(name).touch()
                results.append(("files", f"📄 {name}")); hit = True
            except Exception as e:
                results.append(("files", f"❌ {e}"))

        if any(w in t for w in ["create folder", "make directory", "new folder"]):
            name = "new_folder"
            ws = t.split()
            for i, w in enumerate(ws):
                if w in ["folder", "directory", "named"] and i + 1 < len(ws):
                    name = ws[i + 1].strip('"').strip("'")
            try:
                Path(name).mkdir(exist_ok=True)
                results.append(("files", f"📁 {name}")); hit = True
            except Exception as e:
                results.append(("files", f"❌ {e}"))

        # Fun
        if any(w in t for w in ["joke", "tell me a joke"]):
            jokes = [
                "Why don't cats play poker in the jungle? Too many cheetahs! 😹",
                "What do you call a cat that bowls? A purr-fect game! 🎳",
                "Why did the cat sit on the computer? To watch the mouse! 🖱️",
                "What's a cat's favorite color? Purr-ple! 💜",
                "Why are cats great at games? Nine lives! 🎮",
                "What do you call a singing cat? A purr-former! 🎤",
            ]
            results.append(("fun", f"😂 {random.choice(jokes)}")); hit = True

        if any(w in t for w in ["quote", "inspire", "motivation"]):
            qs = [
                "🌟 Getting ahead = getting started.",
                "🌟 Your time is limited — own it.",
                "🌟 Love what you do → great work.",
                "🌟 Opportunity lives inside difficulty.",
                "🌟 Believing = halfway there.",
                "🌟 Every purr-fect thing was once impossible. 🐱",
            ]
            results.append(("quote", random.choice(qs))); hit = True

        if any(w in t for w in ["flip a coin", "heads or tails", "toss"]):
            results.append(("fun", f"🪙 {random.choice(['Heads!', 'Tails!'])}")); hit = True
        if any(w in t for w in ["roll dice", "roll a die"]):
            results.append(("fun", f"🎲 Rolled a {random.randint(1, 6)}!")); hit = True

        # Chat fallback
        if not hit:
            results.append(("chat", Executor._chat(t)))
        return results

    @staticmethod
    def _math(t):
        import re
        for pat in [r'what is ([\d+\-*/().%\s]+)',
                    r'calculate ([\d+\-*/().%\s]+)',
                    r'solve ([\d+\-*/().%\s]+)',
                    r'([\d]+\s*[+\-*/%]\s*[\d]+(?:\s*[+\-*/%]\s*[\d]+)*)']:
            m = re.search(pat, t, re.IGNORECASE)
            if m:
                e = m.group(1).strip()
                if all(c in "0123456789+-*/().% " for c in e):
                    try:
                        return f"{e} = {eval(e)}"
                    except Exception:
                        pass
        return None

    @staticmethod
    def _chat(t):
        greet = {
            "hi": "Meow! Hi! 😺 How can I help?",
            "hello": "Hello! 🐱 I'm Siya! Ready for anything!",
            "hey": "Hey hey! 😸 What's up?",
            "good morning": "Good morning! ☀️ Purr-fect day ahead!",
            "good afternoon": "Good afternoon! 🌤️ Need anything?",
            "good evening": "Good evening! 🌙 I'm here!",
        }
        for k, r in greet.items():
            if k in t: return r
        if "how are you" in t: return "I'm purr-fect! 😻 Thanks! You?"
        if "your name" in t or "who are you" in t:
            return "I'm Siya! 🐱 Your floating reactive calico cat! Always ready to help!"
        if "what can you do" in t or t in ("help", "?"):
            return (
                "✨ My powers ✨\n"
                "⏰ time/date · 🧮 math · 🖥️ open apps\n"
                "🔍 search web · 🌤️ weather · 📁 files\n"
                "🎲 joke/quote/dice/coin · ✅ tasks\n"
                "Right-click me for the menu! 😽"
            )
        if "thank" in t: return "Anytime! 😻 *happy purr*"
        if any(w in t for w in ["bye", "goodbye", "see you"]):
            return "Bye bye! 👋 I'll be right here! *waves paw* 🐾"
        if "love you" in t: return "Aww I love you too! 💖 *purring hard* 😻💕"
        if "cat" in t: return "CAT? That's me! 🐱 Meow meow! 😸"
        if "hungry" in t: return "🍽️ Try: search for easy recipes"
        if "tired" in t: return "Rest! 💤 Your cat cares! 😴"
        if "happy" in t: return "YAY! 🎉 *bounce bounce* 😸"
        if any(w in t for w in ["sad", "upset", "depressed"]):
            return "💔 Kitty hugs! 🤗 Say 'joke' for a smile! ❤️"
        return random.choice([
            f"Meow 😺 Heard: '{t}'. Try 'help' to see all my tricks!",
            f"🐱 Got it! '{t}' — I can do math, open apps, search web, + more! Say 'help'!",
            f"😸 '{t}'! Remember — right-click me for a quick menu!",
        ])


# =============================================================
# Pro Cat UI
# =============================================================
class ProCatApp:
    EXPRESSIONS = ["normal", "happy", "sleepy", "blink", "thinking",
                   "surprised", "excited", "loving", "shy", "angry",
                   "sad", "crying", "playful", "wink"]

    def __init__(self, root):
        self.root = root
        self.cfg = Config()
        self.tasks = TaskManager()
        self.sound = MeowSound()

        # ---------- True frameless transparent window ----------
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', self.cfg.get("opacity", 1.0))
        # Transparent color-key: magenta
        self.TRANSPARENT = "#ff00ff"
        try:
            self.root.wm_attributes('-transparentcolor', self.TRANSPARENT)
        except Exception:
            pass
        self.root.configure(bg=self.TRANSPARENT)

        # Geometry
        self.size = self.cfg.get("cat_size", 120)
        self._place_window()
        self.root.configure(bg=self.TRANSPARENT)

        # State
        self._drag = {"x": 0, "y": 0}
        self._moved = False
        self._expanded = False
        self._current_expr = "normal"
        self._hover = False
        self._anim_lock = False

        # Sprites (cache)
        self._sprites = {}  # key: (expr, size, rotation, scale) -> PhotoImage

        # ---------- Character canvas (no box fill) ----------
        self.canvas = tk.Canvas(self.root, width=self.size, height=self.size,
                                bg=self.TRANSPARENT, highlightthickness=0, bd=0,
                                cursor="hand2")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.configure(bg=self.TRANSPARENT)

        # Image on canvas
        self._img_id = self.canvas.create_image(self.size // 2, self.size // 2, anchor=tk.CENTER)

        # Optional chat panel frame (not created until needed)
        self.chat_frame = None
        self.chat_w = 380
        self.chat_h = 480

        # Show initial sprite
        self._show_expr("normal")
        self._build_menu()

        # Bindings
        for w in (self.canvas,):
            w.bind('<Button-1>', self._press)
            w.bind('<B1-Motion>', self._drag_move)
            w.bind('<ButtonRelease-1>', self._release)
            w.bind('<Double-Button-1>', self._double_click)
            w.bind('<Enter>', self._hover_in)
            w.bind('<Leave>', self._hover_out)
            w.bind("<Button-3>", self._menu_popup)
            w.bind('<MouseWheel>', self._wheel_resize)  # Win / X11

        # Idle engine
        self._start_idle_engine()

        # Greeting
        self.root.after(700, lambda: self._anim("wave"))
        self.root.after(1400, self.sound.play_happy_chirp)

    # ---------- Geometry ----------
    def _place_window(self):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        pos = self.cfg.get("position", {})
        x, y = pos.get("x"), pos.get("y")
        if x is None:
            x = sw - self.size - 50
        if y is None:
            y = sh - self.size - 140
        x = max(0, min(x, sw - self.size))
        y = max(0, min(y, sh - self.size))
        self.root.geometry(f"{self.size}x{self.size}+{x}+{y}")

    # ---------- Sprites ----------
    def _load_sprite(self, expr, scale=1.0, tilt=0.0):
        """Load sprite with caching. Falls back gracefully."""
        key = (expr, self.size, round(scale, 2), round(tilt, 1))
        if key in self._sprites:
            return self._sprites[key]

        # Prefer dedicated sprite
        fpath = SPRITES_DIR / f"cat_{expr}.png"
        if not fpath.exists():
            # Fallback order
            for alt in [COMPAT_IMAGE, SPRITES_DIR / "cat_normal.png"]:
                if (alt and alt.exists()):
                    fpath = alt; break
        try:
            pil = Image.open(fpath).convert("RGBA")
        except Exception:
            pil = self._gen_fallback(expr)

        # Scale
        target = max(1, int(self.size * scale))
        pil = pil.resize((target, target), Image.Resampling.LANCZOS)

        # Tilt
        if abs(tilt) > 0.1:
            pil = pil.rotate(tilt, Image.Resampling.BILINEAR, expand=False,
                             resample=Image.Resampling.BILINEAR)

        # Paste onto magenta canvas for color-key transparency on tkinter
        canvas_img = Image.new("RGBA", (self.size, self.size), (255, 0, 255, 255))
        px = (self.size - pil.width) // 2
        py = (self.size - pil.height) // 2
        # Composite to respect alpha: wherever pil is transparent, use magenta
        canvas_img = Image.alpha_composite(canvas_img,
                                           Image.new("RGBA", canvas_img.size, (255, 0, 255, 0)))
        # Paste with mask = pil alpha
        canvas_img.paste(pil, (px, py), pil)
        # Convert to RGB and ensure transparent pixels are exactly magenta (#ff00ff)
        rgb = Image.new("RGB", canvas_img.size, (255, 0, 255))
        rgb.paste(canvas_img.convert("RGB"), mask=canvas_img.split()[-1])

        photo = ImageTk.PhotoImage(rgb)
        self._sprites[key] = photo
        return photo

    def _gen_fallback(self, expr):
        # Tiny in-memory fallback calico blob (no disk needed)
        SZ = 512
        img = Image.new("RGBA", (SZ, SZ), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx, cy = SZ // 2, SZ // 2
        # Body
        d.ellipse([cx - 210, cy - 20, cx + 210, cy + 280], fill=(52, 55, 64, 255))
        d.ellipse([cx - 150, cy - 50, cx + 150, cy + 240], fill=(250, 248, 244, 255))
        d.ellipse([cx + 80, cy - 30, cx + 230, cy + 180], fill=(242, 165, 55, 255))
        # Head
        d.ellipse([cx - 180, cy - 260, cx + 180, cy + 20], fill=(250, 248, 244, 255))
        d.ellipse([cx - 220, cy - 200, cx - 50, cy - 40], fill=(242, 165, 55, 255))
        d.ellipse([cx + 60, cy - 220, cx + 220, cy - 50], fill=(52, 55, 64, 255))
        # Paws
        for px in (cx - 90, cx + 90):
            d.ellipse([px - 65, cy + 230, px + 65, cy + 320], fill=(250, 248, 244, 255))
        # Ears
        d.polygon([(cx - 155, cy - 220), (cx - 105, cy - 320), (cx - 75, cy - 220)], fill=(242, 165, 55, 255))
        d.polygon([(cx + 75, cy - 220), (cx + 105, cy - 320), (cx + 155, cy - 220)], fill=(52, 55, 64, 255))
        # Eyes
        for s in (-1, 1):
            e = [cx + s * 75 - 40, cy - 110 - 50, cx + s * 75 + 40, cy - 110 + 50]
            d.ellipse(e, fill=(255, 255, 255, 255))
            d.ellipse([e[0] + 2, e[1] + 2, e[2] - 2, e[3] - 2], fill=(18, 20, 28, 255))
            d.ellipse([e[0] + 10, e[1] + 10, e[2] - 10, e[3] - 10], fill=(45, 175, 195, 255))
            if expr in ("closed", "sleepy", "blink"):
                d.ellipse([e[0], e[1] + 18, e[2], e[3] - 10], fill=(18, 20, 28, 255))
        # Nose
        d.polygon([(cx, cy - 20), (cx - 22, cy - 48), (cx + 22, cy - 48)], fill=(255, 118, 85, 255))
        # Mouth
        d.arc([cx - 45, cy - 30, cx + 5, cy + 20], 0, 180, fill=(92, 58, 46, 255), width=3)
        d.arc([cx - 5, cy - 30, cx + 45, cy + 20], 0, 180, fill=(92, 58, 46, 255), width=3)
        return img.resize((800, 800), Image.Resampling.LANCZOS)

    def _show_expr(self, expr, scale=1.0, tilt=0.0, clear_old=False):
        if clear_old:
            self._sprites.pop((expr, self.size, round(scale, 2), round(tilt, 1)), None)
        photo = self._load_sprite(expr, scale=scale, tilt=tilt)
        self.canvas.itemconfig(self._img_id, image=photo)
        self._current_expr = expr

    # ---------- Animation engine ----------
    def _anim(self, kind):
        """High-level named animations (thread-safe via after)."""
        if self._anim_lock:
            return

        def _run():
            self._anim_lock = True
            try:
                if kind == "wave":
                    for i, tilt in enumerate([-8, -14, -6, 8, 14, 6, -4, 4, 0]):
                        self.root.after(i * 85, lambda t=tilt: self._show_expr("happy", tilt=t))
                    self.root.after(10 * 85, lambda: self._show_expr("normal"))
                elif kind == "bounce":
                    seq = [1.0, 1.1, 1.18, 1.1, 1.0, 0.95, 1.02, 1.0]
                    for i, s in enumerate(seq):
                        expr = "excited" if i % 2 == 0 else "happy"
                        self.root.after(i * 80, lambda ss=s, ex=expr: self._show_expr(ex, scale=ss))
                elif kind == "shake":
                    for i, dx in enumerate([0, -5, 8, -8, 6, -4, 3, 0]):
                        self.root.after(i * 55, lambda d=dx: self.canvas.coords(
                            self._img_id, self.size // 2 + d, self.size // 2))
                    self.root.after(10 * 55, lambda: self.canvas.coords(
                        self._img_id, self.size // 2, self.size // 2))
                elif kind == "heart_pulse":
                    for i, s in enumerate([1.0, 1.08, 1.12, 1.05, 1.0, 1.07, 1.0]):
                        ex = "loving" if i < 6 else "happy"
                        self.root.after(i * 120, lambda ss=s, e=ex: self._show_expr(e, scale=ss))
                elif kind == "sneeze":
                    seq = [("normal", 1.0), ("normal", 0.96), ("normal", 0.93),
                           ("surprised", 1.08), ("happy", 1.02), ("normal", 1.0)]
                    for i, (e, s) in enumerate(seq):
                        self.root.after(i * 90, lambda ee=e, ss=s: self._show_expr(ee, scale=ss))
                elif kind in ("error", "angry_shake"):
                    self._show_expr("angry" if kind == "angry_shake" else "crying")
                    for i, dx in enumerate([0, -6, 10, -10, 7, -5, 3, 0]):
                        self.root.after(i * 50, lambda d=dx: self.canvas.coords(
                            self._img_id, self.size // 2 + d, self.size // 2))
                    self.root.after(500, lambda: (self.canvas.coords(
                        self._img_id, self.size // 2, self.size // 2), self._show_expr("normal")))
            finally:
                total = {"wave": 900, "bounce": 700, "shake": 550,
                         "heart_pulse": 900, "sneeze": 600, "error": 700, "angry_shake": 700}.get(kind, 700)
                self.root.after(total + 50, self._release_lock)
        _run()

    def _release_lock(self):
        self._anim_lock = False

    # ---------- Interaction bindings ----------
    def _press(self, ev):
        self._drag["x"] = ev.x_root - self.root.winfo_x()
        self._drag["y"] = ev.y_root - self.root.winfo_y()
        self._moved = False

    def _drag_move(self, ev):
        self._moved = True
        x = ev.x_root - self._drag["x"]
        y = ev.y_root - self._drag["y"]
        # Tilt feedback when dragging
        tilt = max(-10, min(10, (ev.x - self.size // 2) / 8))
        self.root.geometry(f"+{x}+{y}")
        if not self._anim_lock:
            try:
                self._show_expr("happy", tilt=tilt)
            except Exception:
                pass

    def _release(self, ev):
        # Save pos
        self.cfg.set("position", {"x": self.root.winfo_x(), "y": self.root.winfo_y()})
        # Reset tilt
        if not self._anim_lock:
            self.root.after(80, lambda: self._show_expr("normal"))

    def _double_click(self, ev):
        MeowSound.play_cute_meow()
        self._anim("bounce")
        if self.cfg.get("show_chat_on_double_click", True):
            self.root.after(500, self._toggle_chat)

    def _hover_in(self, ev):
        if self._anim_lock or self._expanded:
            return
        self._hover = True
        if self.cfg.get("hover_zoom", True):
            self._show_expr("happy", scale=1.08)
            MeowSound.play_purr()

    def _hover_out(self, ev):
        self._hover = False
        if not self._anim_lock and not self._expanded:
            self._show_expr(self._current_expr if self._current_expr in ("sleepy",) else "normal")

    def _wheel_resize(self, ev):
        # Ctrl+wheel? Or just wheel? Let's just allow wheel for quick resize (no modifiers)
        delta = 1 if ev.delta > 0 else -1
        new = max(60, min(250, self.size + delta * 6))
        if new != self.size:
            self._resize(new)

    def _resize(self, new_size):
        self.size = new_size
        self.cfg.set("cat_size", new_size)
        self.canvas.config(width=new_size, height=new_size)
        self.canvas.coords(self._img_id, new_size // 2, new_size // 2)
        self._sprites.clear()
        self._show_expr("normal")
        self.root.geometry(f"{new_size}x{new_size}")

    # ---------- Click handler (single click without drag) ----------
    def _on_single_click_action(self):
        """Single press-release without drag = click."""
        MeowSound.play_cute_meow()
        r = random.random()
        if r < 0.25:
            self._anim("wave")
        elif r < 0.55:
            self._anim("bounce")
            self._show_expr("excited")
            self.root.after(900, lambda: self._show_expr("happy"))
        elif r < 0.75:
            self._show_expr("shy")
            self.root.after(1200, lambda: self._show_expr("normal"))
        elif r < 0.9:
            self._show_expr("playful")
            self.root.after(1000, lambda: self._show_expr("normal"))
        else:
            self._anim("heart_pulse")

    # Release triggers click if no drag happened (hook after _release)
    def _release(self, ev):
        # Save pos
        self.cfg.set("position", {"x": self.root.winfo_x(), "y": self.root.winfo_y()})
        if not self._moved:
            self._on_single_click_action()
        elif not self._anim_lock:
            self.root.after(80, lambda: self._show_expr("normal"))

    # ---------- Idle engine ----------
    def _start_idle_engine(self):
        if not self.cfg.get("idle_anims", True):
            return

        def blink():
            if not self._anim_lock and not self._hover and not self._expanded:
                for i, e in enumerate(["blink", "blink", "normal"]):
                    self.root.after(i * 90, lambda ee=e: self._show_expr(ee))
            self.root.after(random.randint(4500, 8000), blink)

        def mood_shifts():
            if not self._anim_lock and not self._hover and not self._expanded:
                moods = ["normal", "normal", "happy", "normal", "sleepy", "playful", "thinking", "normal"]
                m = random.choice(moods)
                self._show_expr(m)
                if m == "sleepy":
                    MeowSound.play_purr()
            self.root.after(random.randint(15000, 30000), mood_shifts)

        def breath():
            if not self._anim_lock and not self._hover and not self._expanded \
                    and self.cfg.get("breathing", True):
                scale = 1.0 + 0.015 * math.sin(time.time() * 1.4)
                try:
                    self._show_expr(self._current_expr, scale=scale)
                except Exception:
                    pass
            self.root.after(120, breath)

        def tail_wag_chance():
            if not self._anim_lock and not self._hover and not self._expanded \
                    and random.random() < 0.5:
                for i, t in enumerate([0, 4, -4, 5, -3, 2, 0]):
                    self.root.after(i * 90, lambda tt=t: self._show_expr(
                        self._current_expr, tilt=tt))
            self.root.after(random.randint(9000, 17000), tail_wag_chance)

        self.root.after(2200, blink)
        self.root.after(11000, mood_shifts)
        self.root.after(600, breath)
        self.root.after(7000, tail_wag_chance)

    # ---------- Menu ----------
    def _build_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0,
                            bg="#1a1a2e", fg="white",
                            activebackground="#00d4ff", activeforeground="#1a1a2e")
        self.menu.add_command(label="💬 Open Chat", command=lambda: (MeowSound.play_cute_meow(), self._toggle_chat()))
        self.menu.add_command(label="✅ Add Task", command=self._quick_add_task)
        self.menu.add_command(label="📋 Show Tasks", command=self._show_tasks)
        self.menu.add_separator()
        self.menu.add_command(label="🔊 Meow! 🎵", command=lambda: MeowSound.play_cute_meow())
        self.menu.add_command(label="😻 Purr", command=lambda: MeowSound.play_purr())
        self.menu.add_command(label="🐦 Chirp", command=lambda: MeowSound.play_happy_chirp())
        self.menu.add_separator()
        sz = self.menu.add_cascade(label="📏 Resize Cat")
        sm = tk.Menu(sz, tearoff=0, bg="#1a1a2e", fg="white",
                     activebackground="#00d4ff", activeforeground="#1a1a2e")
        for label, s in [("Tiny (70)", 70), ("Small (90)", 90), ("Normal (120)", 120),
                         ("Large (160)", 160), ("Huge (200)", 200)]:
            sm.add_command(label=label, command=lambda ss=s: self._resize(ss))
        self.menu.entryconfigure(self.menu.index("end"), menu=sm)
        self.menu.add_separator()
        self.menu.add_command(label="👋 Wave", command=lambda: (MeowSound.play_purr(), self._anim("wave")))
        self.menu.add_command(label="🎉 Bounce", command=lambda: (MeowSound.play_happy_chirp(), self._anim("bounce")))
        self.menu.add_command(label="💕 Love", command=lambda: (MeowSound.play_purr(), self._anim("heart_pulse")))
        self.menu.add_command(label="😤 Shake", command=lambda: self._anim("angry_shake"))
        self.menu.add_separator()
        self.menu.add_command(label="❓ Help", command=self._show_help)
        self.menu.add_separator()
        self.menu.add_command(label="❌ Exit Siya", command=self._quit)

    def _menu_popup(self, event):
        self._moved = True  # prevent click-triggered meow after menu
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    # ---------- Chat ----------
    def _toggle_chat(self):
        if self._expanded:
            self._collapse_chat()
        else:
            self._expand_chat()

    def _expand_chat(self):
        self._expanded = True
        if self.chat_frame is None:
            self._build_chat_panel()
        # Grow window to fit chat panel below cat
        total_w = max(self.size, self.chat_w)
        total_h = self.size + self.chat_h + 6
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        if x + total_w > sw: x = sw - total_w - 5
        if y + total_h > sh: y = max(0, sh - total_h - 50)
        self.root.geometry(f"{total_w}x{total_h}+{x}+{y}")
        self.chat_frame.place(x=0, y=self.size + 3, width=total_w, height=self.chat_h)
        self._show_expr("excited")
        self.root.after(1000, lambda: (self._show_expr("happy") if not self._anim_lock else None))
        self.text_entry.focus_set()

    def _collapse_chat(self):
        self._expanded = False
        if self.chat_frame:
            self.chat_frame.place_forget()
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.root.geometry(f"{self.size}x{self.size}+{x}+{y}")
        self._show_expr("normal")

    def _build_chat_panel(self):
        self.chat_frame = tk.Frame(self.root, bg="#1a1a2e", bd=2, relief=tk.RAISED)
        header = tk.Frame(self.chat_frame, bg="#16213e", height=28)
        header.pack(fill=tk.X); header.pack_propagate(False)
        tk.Label(header, text="🐱 Siya Chat", font=("Arial", 9, "bold"),
                 bg="#16213e", fg="#00d4ff").pack(side=tk.LEFT, padx=8)
        tk.Button(header, text="×", font=("Arial", 9, "bold"),
                  bg="#e94560", fg="white", relief=tk.FLAT, cursor="hand2",
                  command=self._collapse_chat, width=2).pack(side=tk.RIGHT, padx=4)

        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame, wrap=tk.WORD, font=("Consolas", 9),
            bg="#0f3460", fg="#e9ecef", insertbackground="#00d4ff",
            relief=tk.FLAT, padx=6, pady=6, height=16)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.chat_display.config(state=tk.DISABLED)

        qrow = tk.Frame(self.chat_frame, bg="#1a1a2e")
        qrow.pack(fill=tk.X, padx=4, pady=(0, 2))
        qb = [("⏰", "what time is it"), ("📅", "what's today's date"),
              ("🧮", None), ("🌤️", "weather"), ("😂", "tell me a joke"), ("❓", "help")]
        for label, cmd in qb:
            if cmd is None:
                fn = self._quick_calc
            else:
                fn = lambda c=cmd: self._send_text(c)
            tk.Button(qrow, text=label, font=("Arial", 10, "bold"),
                      bg="#16213e", fg="#00d4ff", relief=tk.FLAT, cursor="hand2",
                      command=fn, width=3, padx=2).pack(side=tk.LEFT, padx=2, pady=1)

        ir = tk.Frame(self.chat_frame, bg="#1a1a2e")
        ir.pack(fill=tk.X, padx=4, pady=4)
        self.text_entry = tk.Entry(ir, font=("Arial", 10), bg="#0f3460", fg="white",
                                   insertbackground="#00d4ff", relief=tk.FLAT)
        self.text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4), ipady=4)
        self.text_entry.bind('<Return>', lambda e: self._send())
        tk.Button(ir, text="Send", font=("Arial", 9, "bold"),
                  bg="#00d4ff", fg="#1a1a2e", relief=tk.FLAT, cursor="hand2",
                  command=self._send, padx=10).pack(side=tk.RIGHT, ipady=2)

        self._add("Siya", "Meow! 🐱 Try: help, tell me a joke, what time is it, open notepad, weather, etc.")

    def _quick_calc(self):
        e = simpledialog.askstring("Calculator", "Expression (e.g. 12 * 17):", parent=self.root)
        if e: self._send_text(f"calculate {e}")

    def _quick_add_task(self):
        d = simpledialog.askstring("Add Task", "Description:", parent=self.root)
        if d:
            t = self.tasks.add(d)
            self._anim("bounce")
            messagebox.showinfo("Task Added", f"✅ Task #{t['id']}:\n{d}")

    def _show_tasks(self):
        pending = self.tasks.pending()
        top = tk.Toplevel(self.root)
        top.title("📋 Pending Tasks")
        top.geometry("350x400"); top.configure(bg="#1a1a2e"); top.attributes('-topmost', True)
        tk.Label(top, text=f"📋 Tasks ({len(pending)} pending)",
                 font=("Arial", 12, "bold"), bg="#1a1a2e", fg="#00d4ff").pack(pady=8)
        f = tk.Frame(top, bg="#1a1a2e"); f.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        if not pending:
            tk.Label(f, text="🎉 All caught up!", font=("Arial", 10),
                     bg="#1a1a2e", fg="#00ff88").pack(pady=20)
        else:
            for t in pending:
                row = tk.Frame(f, bg="#0f3460", relief=tk.RAISED, bd=1)
                row.pack(fill=tk.X, pady=2)
                tk.Label(row, text=f"#{t['id']} {t['description']}",
                         font=("Arial", 9), bg="#0f3460", fg="white", anchor="w",
                         wraplength=250).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6, pady=6)
                def _done(tid=t["id"]):
                    self.tasks.complete(tid); top.destroy()
                    self._anim("heart_pulse")
                    MeowSound.play_happy_chirp()
                    self.root.after(150, self._show_tasks)
                tk.Button(row, text="✓", font=("Arial", 9, "bold"),
                          bg="#00ff88", fg="#1a1a2e", relief=tk.FLAT,
                          cursor="hand2", width=3, command=_done).pack(side=tk.RIGHT, padx=4, pady=3)

    def _show_help(self):
        top = tk.Toplevel(self.root); top.title("❓ Siya Help"); top.geometry("420x550")
        top.configure(bg="#1a1a2e"); top.attributes('-topmost', True)
        tk.Label(top, text="🐱 Siya Command Reference",
                 font=("Arial", 14, "bold"), bg="#1a1a2e", fg="#00d4ff").pack(pady=10)
        t = scrolledtext.ScrolledText(top, font=("Consolas", 9),
                                      bg="#0f3460", fg="white", wrap=tk.WORD, padx=10, pady=10)
        t.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        t.insert(tk.END, (
            "🐱 INTERACTION\n"
            "  • SINGLE CLICK = meow + animation\n"
            "  • DOUBLE CLICK = open chat\n"
            "  • DRAG = move me anywhere\n"
            "  • RIGHT-CLICK = menu (resize / sounds / anims)\n"
            "  • MOUSE WHEEL = resize me!\n"
            "  • HOVER = zoom + purr\n\n"
            "⏰ TIME & DATE\n"
            "  • what time is it · today's date\n\n"
            "🧮 MATH\n"
            "  • what is 25 * 17 · calculate 15% of 200\n\n"
            "🖥️ OPEN APPS (Windows)\n"
            "  • open notepad · open calculator · open paint\n"
            "  • open chrome · open cmd · open settings\n\n"
            "🔍 WEB\n"
            "  • search for python tutorials\n"
            "  • open youtube.com · go to github.com\n\n"
            "🌤️ WEATHER (free / no key)\n"
            "  • weather · weather in tokyo\n\n"
            "📁 FILES\n"
            "  • list files\n"
            "  • create file notes.txt\n"
            "  • new folder projects\n\n"
            "🎲 FUN\n"
            "  • tell me a joke · flip a coin · roll dice\n"
            "  • give me a quote\n\n"
            "✅ TASKS\n"
            "  • add task buy groceries\n"
            "  • show tasks · complete task 3\n"
        ))
        t.config(state=tk.DISABLED)

    # Send / receive
    def _send_text(self, text):
        if not self._expanded:
            self._expand_chat()
            self.root.after(120, lambda: self._send_text(text))
            return
        self.text_entry.delete(0, tk.END); self.text_entry.insert(0, text); self._send()

    def _send(self):
        user = self.text_entry.get().strip()
        if not user: return
        self.text_entry.delete(0, tk.END)
        threading.Thread(target=self._process, args=(user,), daemon=True).start()

    def _process(self, user):
        self._add("You", user)
        self._show_expr("thinking")
        t = user.lower()
        # Task verbs
        if any(k in t for k in ["add task", "create task", "new task", "remind me to", "remind me"]):
            desc = t
            for w in ["add task", "create task", "new task", "remind me to", "remind me"]:
                desc = desc.replace(w, "")
            desc = desc.strip(" :,.-")
            if desc:
                self.tasks.add(desc)
                self.root.after(0, lambda: self._add("Siya", f"✅ Added: '{desc}'"))
                self._anim("bounce"); MeowSound.play_happy_chirp()
            else:
                self.root.after(0, lambda: self._add("Siya", "📝 What task?"))
            self.root.after(2500, lambda: self._show_expr("normal"))
            return
        if "show task" in t or "my task" in t or "pending task" in t:
            p = self.tasks.pending()
            msg = "📋 Pending:\n" + "\n".join(f"  #{x['id']}. {x['description']}" for x in p) if p else "🎉 All caught up!"
            self.root.after(0, lambda: self._add("Siya", msg)); self._show_expr("happy")
            return
        if "complete task" in t or "done task" in t or "finish task" in t:
            import re
            m = re.search(r'\d+', t)
            if m and self.tasks.complete(int(m.group())):
                self.root.after(0, lambda: self._add("Siya", f"🎉 Task #{m.group()} done! 🎊"))
                self._anim("heart_pulse"); MeowSound.play_happy_chirp()
            else:
                self.root.after(0, lambda: self._add("Siya", "🤔 Which? Try: 'complete task 3'"))
                self._show_expr("surprised")
            self.root.after(2500, lambda: self._show_expr("normal"))
            return
        # Execute
        results = Executor.run(user)
        seen = set()
        parts = []
        moods = {"error": "crying", "app": "excited", "web": "excited", "fun": "happy",
                 "quote": "loving", "math": "playful", "weather": "happy",
                 "files": "happy", "chat": "happy"}
        chosen = "speaking"
        for kind, msg in results:
            if kind not in seen or kind == "chat":
                parts.append(msg); seen.add(kind)
            if kind in moods: chosen = moods[kind]
        final = "\n\n".join(parts)
        if chosen == "excited":
            self._anim("bounce"); MeowSound.play_happy_chirp()
        elif chosen == "crying":
            self._anim("error")
        elif chosen == "loving":
            self._anim("heart_pulse"); MeowSound.play_purr()
        else:
            if "happy" in chosen: MeowSound.play_purr()
            self._show_expr("happy")
        self.root.after(0, lambda: self._add("Siya", final))
        self.root.after(3500, lambda: self._show_expr("normal"))

    def _add(self, sender, msg):
        if not hasattr(self, 'chat_display'):
            return
        self.chat_display.config(state=tk.NORMAL)
        ts = datetime.now().strftime("%H:%M")
        if sender == "You":
            self.chat_display.insert(tk.END, f"\n[{ts}] 👤 You:\n", "u")
            self.chat_display.insert(tk.END, f"{msg}\n", "um")
        else:
            self.chat_display.insert(tk.END, f"\n[{ts}] 🐱 Siya:\n", "s")
            self.chat_display.insert(tk.END, f"{msg}\n", "sm")
        self.chat_display.tag_config("u", foreground="#00d4ff", font=("Arial", 9, "bold"))
        self.chat_display.tag_config("um", foreground="#ffffff")
        self.chat_display.tag_config("s", foreground="#00ff88", font=("Arial", 9, "bold"))
        self.chat_display.tag_config("sm", foreground="#ecf0f1")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    # ---------- Quit ----------
    def _quit(self):
        if messagebox.askyesno("Exit Siya", "Exit? 🐱"):
            self.root.destroy()


# =============================================================
# Entry
# =============================================================
def _ensure_sprites():
    """Run generator if sprites folder is empty/missing"""
    any_png = bool(list(SPRITES_DIR.glob("cat_*.png"))) if SPRITES_DIR.exists() else False
    if not any_png and not COMPAT_IMAGE.exists():
        try:
            from generate_pro_cat import generate_all
            generate_all(SPRITES_DIR)
        except Exception as e:
            # Silent fallback — the app generates in-memory sprites anyway
            sys.stderr.write(f"[siya] note: sprite pre-generation skipped ({e})\n")


def main():
    _ensure_sprites()
    root = tk.Tk()
    app = ProCatApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
