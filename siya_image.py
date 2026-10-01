"""
Siya with Animated Cat Image Interface
Features: Image-based cat with reactive animations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageDraw
import threading
from datetime import datetime
import json
from pathlib import Path
import requests
import io

CONFIG_FILE = Path("siya_config.json")


class ConfigManager:
    """Manages app configuration"""
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.config = self.load_config()
    
    def load_config(self):
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "use_local_ai": True,
            "groq_api_key": "",
            "ollama_model": "llama2",
            "ollama_url": "http://localhost:11434"
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
    """Manages tasks and reminders"""
    def __init__(self):
        self.tasks_file = Path("siya_tasks.json")
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_tasks(self):
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, task_description):
        task = {
            "id": len(self.tasks) + 1,
            "description": task_description,
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
    
    def get_pending_tasks(self):
        return [t for t in self.tasks if not t["completed"]]


class AnimatedCatImage:
    """Handles cat image loading and animations"""
    def __init__(self, canvas, width=300, height=300):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.base_image = None
        self.current_image = None
        self.image_id = None
        self.animation_active = False
        
        # Load or create cat image
        self.load_cat_image()
    
    def load_cat_image(self):
        """Load the cat image from file or create placeholder"""
        image_path = Path("cat_image.png")
        
        if image_path.exists():
            # Load existing image
            self.base_image = Image.open(image_path)
        else:
            # Create a cute placeholder cat
            self.base_image = self.create_placeholder_cat()
            self.base_image.save(image_path)
        
        # Resize to fit
        self.base_image = self.base_image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        self.show_image(self.base_image)
    
    def create_placeholder_cat(self):
        """Create a cute placeholder cat image"""
        img = Image.new('RGB', (400, 400), color='#4a5568')
        draw = ImageDraw.Draw(img)
        
        # Draw cat face
        # Head (circle)
        draw.ellipse([100, 80, 300, 280], fill='#f39c12', outline='#e67e22', width=3)
        
        # Ears (triangles)
        draw.polygon([120, 100, 150, 50, 180, 100], fill='#f39c12', outline='#e67e22')
        draw.polygon([220, 100, 250, 50, 280, 100], fill='#f39c12', outline='#e67e22')
        
        # Inner ears
        draw.polygon([130, 95, 150, 65, 170, 95], fill='#ffeaa7')
        draw.polygon([230, 95, 250, 65, 270, 95], fill='#ffeaa7')
        
        # Eyes (big and cute)
        draw.ellipse([140, 150, 180, 200], fill='#2d3436', outline='#000000', width=2)
        draw.ellipse([220, 150, 260, 200], fill='#2d3436', outline='#000000', width=2)
        
        # Eye highlights
        draw.ellipse([155, 160, 170, 180], fill='#ffffff')
        draw.ellipse([235, 160, 250, 180], fill='#ffffff')
        
        # Nose
        draw.polygon([200, 210, 190, 225, 210, 225], fill='#e74c3c')
        
        # Mouth (cute smile)
        draw.arc([170, 215, 230, 250], 0, 180, fill='#2d3436', width=3)
        
        # Whiskers
        for y in [200, 215, 230]:
            # Left whiskers
            draw.line([100, y, 140, y], fill='#2d3436', width=2)
            # Right whiskers
            draw.line([260, y, 300, y], fill='#2d3436', width=2)
        
        # Body
        draw.ellipse([120, 260, 280, 380], fill='#f39c12', outline='#e67e22', width=3)
        
        # Chest/belly (white)
        draw.ellipse([160, 280, 240, 370], fill='#ffeaa7')
        
        return img
    
    def show_image(self, image):
        """Display image on canvas"""
        self.current_photo = ImageTk.PhotoImage(image)
        
        if self.image_id:
            self.canvas.itemconfig(self.image_id, image=self.current_photo)
        else:
            self.image_id = self.canvas.create_image(
                self.width // 2, 
                self.height // 2, 
                image=self.current_photo
            )
    
    def set_mood(self, mood):
        """Change cat appearance based on mood"""
        if self.animation_active:
            return
        
        if mood == "happy":
            self.show_normal()
        elif mood == "thinking":
            self.show_thinking()
        elif mood == "speaking":
            self.show_speaking()
        elif mood == "excited":
            self.show_excited()
        elif mood == "loving":
            self.show_loving()
        elif mood == "error":
            self.show_error()
    
    def show_normal(self):
        """Normal happy cat"""
        self.show_image(self.base_image)
    
    def show_thinking(self):
        """Thinking effect - slightly darker"""
        img = self.base_image.copy()
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.9)
        self.show_image(img)
    
    def show_speaking(self):
        """Speaking effect - slight glow"""
        img = self.base_image.copy()
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        self.show_image(img)
    
    def show_excited(self):
        """Excited effect - bounce animation"""
        self.animation_active = True
        self.bounce_animation()
    
    def show_loving(self):
        """Loving effect - pulse animation"""
        self.animation_active = True
        self.pulse_animation()
    
    def show_error(self):
        """Error effect - shake animation"""
        self.animation_active = True
        self.shake_animation()
    
    def bounce_animation(self, count=0):
        """Bounce animation"""
        if count >= 6:
            self.animation_active = False
            self.show_normal()
            return
        
        # Alternate between slightly smaller and larger
        scale = 1.05 if count % 2 == 0 else 0.95
        img = self.base_image.copy()
        new_size = (int(self.width * scale), int(self.height * scale))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        self.show_image(img)
        
        self.canvas.after(100, lambda: self.bounce_animation(count + 1))
    
    def pulse_animation(self, count=0):
        """Pulse animation"""
        if count >= 8:
            self.animation_active = False
            self.show_normal()
            return
        
        # Pulse brightness
        brightness = 1.0 + (0.1 * (count % 2))
        img = self.base_image.copy()
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)
        self.show_image(img)
        
        self.canvas.after(150, lambda: self.pulse_animation(count + 1))
    
    def shake_animation(self, count=0):
        """Shake animation"""
        if count >= 8:
            self.animation_active = False
            self.show_normal()
            return
        
        # Move left and right
        offset = 10 if count % 2 == 0 else -10
        self.canvas.move(self.image_id, offset, 0)
        
        self.canvas.after(50, lambda: self.shake_animation(count + 1))


class SiyaCatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐱 Siya - Animated Cat Assistant")
        self.root.geometry("700x900")
        self.root.configure(bg="#2d3436")
        
        # Initialize components
        self.config_manager = ConfigManager()
        self.task_manager = TaskManager()
        
        # Check configuration
        if not self.config_manager.get("groq_api_key") and not self.config_manager.get("use_local_ai"):
            self.show_welcome_screen()
        else:
            self.setup_ui()
    
    def show_welcome_screen(self):
        """Show welcome screen on first run"""
        welcome_frame = tk.Frame(self.root, bg="#2d3436")
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            welcome_frame,
            text="🐱 Welcome to Siya!",
            font=("Arial", 24, "bold"),
            bg="#2d3436",
            fg="#00d4ff"
        ).pack(pady=20)
        
        tk.Label(
            welcome_frame,
            text="Your Animated AI Cat Assistant",
            font=("Arial", 14),
            bg="#2d3436",
            fg="#ffffff"
        ).pack(pady=5)
        
        # Options
        options_frame = tk.Frame(welcome_frame, bg="#34495e", relief=tk.RAISED, bd=2)
        options_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        tk.Label(
            options_frame,
            text="Choose Your AI Engine:",
            font=("Arial", 16, "bold"),
            bg="#34495e",
            fg="#00d4ff"
        ).pack(pady=15)
        
        # Ollama option
        ollama_frame = tk.LabelFrame(
            options_frame,
            text="Option 1: Ollama (Recommended)",
            font=("Arial", 12, "bold"),
            bg="#2c3e50",
            fg="#00ff88",
            relief=tk.GROOVE,
            bd=2
        )
        ollama_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            ollama_frame,
            text="✅ 100% FREE forever\n✅ Runs locally (private)\n✅ No internet needed\n✅ Unlimited usage",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ffffff",
            justify=tk.LEFT
        ).pack(padx=10, pady=10)
        
        tk.Button(
            ollama_frame,
            text="Use Ollama",
            font=("Arial", 11, "bold"),
            bg="#00ff88",
            fg="#2d3436",
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.configure_ollama(welcome_frame)
        ).pack(pady=10)
        
        # Groq option
        groq_frame = tk.LabelFrame(
            options_frame,
            text="Option 2: Groq API",
            font=("Arial", 12, "bold"),
            bg="#2c3e50",
            fg="#00d4ff",
            relief=tk.GROOVE,
            bd=2
        )
        groq_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            groq_frame,
            text="✅ 100% FREE (no credit card)\n✅ Quick setup\n✅ Cloud-based\n✅ 14,400 requests/day",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ffffff",
            justify=tk.LEFT
        ).pack(padx=10, pady=10)
        
        tk.Button(
            groq_frame,
            text="Use Groq API",
            font=("Arial", 11, "bold"),
            bg="#00d4ff",
            fg="#2d3436",
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.configure_groq(welcome_frame)
        ).pack(pady=10)
    
    def configure_ollama(self, welcome_frame):
        """Configure Ollama"""
        self.config_manager.set("use_local_ai", True)
        self.config_manager.set("ollama_model", "llama2")
        welcome_frame.destroy()
        self.setup_ui()
    
    def configure_groq(self, welcome_frame):
        """Configure Groq API"""
        api_key = tk.simpledialog.askstring(
            "Groq API Key",
            "Enter your Groq API key:\n(Get it from https://console.groq.com)",
            parent=self.root
        )
        
        if api_key and api_key.startswith("gsk_"):
            self.config_manager.set("use_local_ai", False)
            self.config_manager.set("groq_api_key", api_key)
            welcome_frame.destroy()
            self.setup_ui()
        else:
            messagebox.showerror("Invalid Key", "Please enter a valid Groq API key (starts with 'gsk_')")
    
    def setup_ui(self):
        """Setup main UI"""
        # Create notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabs
        self.chat_frame = tk.Frame(self.notebook, bg="#2d3436")
        self.tasks_frame = tk.Frame(self.notebook, bg="#2d3436")
        self.settings_frame = tk.Frame(self.notebook, bg="#2d3436")
        
        self.notebook.add(self.chat_frame, text="💬 Chat")
        self.notebook.add(self.tasks_frame, text="✅ Tasks")
        self.notebook.add(self.settings_frame, text="⚙️ Settings")
        
        self.setup_chat_tab()
        self.setup_tasks_tab()
        self.setup_settings_tab()
    
    def setup_chat_tab(self):
        """Setup chat tab with animated cat"""
        # Cat image area
        cat_frame = tk.Frame(self.chat_frame, bg="#34495e", height=320)
        cat_frame.pack(fill=tk.X, pady=10, padx=10)
        cat_frame.pack_propagate(False)
        
        # Canvas for cat image
        self.cat_canvas = tk.Canvas(
            cat_frame,
            width=300,
            height=300,
            bg="#34495e",
            highlightthickness=0
        )
        self.cat_canvas.pack(pady=10)
        
        # Initialize animated cat
        self.animated_cat = AnimatedCatImage(self.cat_canvas, 300, 300)
        
        # Status label
        self.status_label = tk.Label(
            self.chat_frame,
            text="😺 Meow! Ready to chat!",
            font=("Arial", 14, "bold"),
            bg="#2d3436",
            fg="#00d4ff"
        )
        self.status_label.pack(pady=10)
        
        # Chat display
        chat_container = tk.Frame(self.chat_frame, bg="#2d3436")
        chat_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(
            chat_container,
            text="💬 Conversation",
            font=("Arial", 11, "bold"),
            bg="#2d3436",
            fg="#ffffff"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#34495e",
            fg="#ecf0f1",
            insertbackground="#00d4ff",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Control buttons
        button_frame = tk.Frame(self.chat_frame, bg="#2d3436")
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            button_frame,
            text="⌨️ Type Message",
            font=("Arial", 11, "bold"),
            bg="#00d4ff",
            fg="#2d3436",
            activebackground="#00a8cc",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_type_input
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=("Arial", 11, "bold"),
            bg="#95a5a6",
            fg="#ffffff",
            activebackground="#7f8c8d",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_chat
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Text input frame
        self.text_input_frame = tk.Frame(self.chat_frame, bg="#2d3436")
        
        self.text_entry = tk.Entry(
            self.text_input_frame,
            font=("Arial", 11),
            bg="#34495e",
            fg="#ffffff",
            insertbackground="#00d4ff",
            relief=tk.FLAT
        )
        self.text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5), pady=5)
        self.text_entry.bind('<Return>', lambda e: self.send_text_input())
        
        tk.Button(
            self.text_input_frame,
            text="Send",
            font=("Arial", 10, "bold"),
            bg="#00d4ff",
            fg="#2d3436",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.send_text_input
        ).pack(side=tk.LEFT, padx=(0, 10), pady=5)
        
        # Welcome message
        self.add_message("Siya", "Meow! 🐱 I'm Siya, your animated AI cat assistant! Type a message to chat with me!")
    
    def setup_tasks_tab(self):
        """Setup tasks tab"""
        # Header
        header = tk.Frame(self.tasks_frame, bg="#2d3436")
        header.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            header,
            text="✅ Task Manager",
            font=("Arial", 16, "bold"),
            bg="#2d3436",
            fg="#00d4ff"
        ).pack(side=tk.LEFT)
        
        tk.Button(
            header,
            text="🔄 Refresh",
            font=("Arial", 10, "bold"),
            bg="#95a5a6",
            fg="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.refresh_tasks
        ).pack(side=tk.RIGHT)
        
        # Add task
        add_frame = tk.Frame(self.tasks_frame, bg="#34495e")
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            add_frame,
            text="Add New Task:",
            font=("Arial", 10, "bold"),
            bg="#34495e",
            fg="#ffffff"
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        task_input_frame = tk.Frame(add_frame, bg="#34495e")
        task_input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.task_entry = tk.Entry(
            task_input_frame,
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#ffffff",
            insertbackground="#00d4ff",
            relief=tk.FLAT
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        tk.Button(
            task_input_frame,
            text="+ Add",
            font=("Arial", 10, "bold"),
            bg="#00d4ff",
            fg="#2d3436",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.add_task
        ).pack(side=tk.LEFT)
        
        # Tasks list
        tk.Label(
            self.tasks_frame,
            text="Pending Tasks:",
            font=("Arial", 11, "bold"),
            bg="#2d3436",
            fg="#ffffff"
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        list_frame = tk.Frame(self.tasks_frame, bg="#2d3436")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tasks_canvas = tk.Canvas(list_frame, bg="#34495e", highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.tasks_canvas.yview)
        self.tasks_inner_frame = tk.Frame(self.tasks_canvas, bg="#34495e")
        
        self.tasks_inner_frame.bind(
            "<Configure>",
            lambda e: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        )
        
        self.tasks_canvas.create_window((0, 0), window=self.tasks_inner_frame, anchor="nw")
        self.tasks_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.tasks_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.refresh_tasks()
    
    def setup_settings_tab(self):
        """Setup settings tab"""
        tk.Label(
            self.settings_frame,
            text="⚙️ Settings",
            font=("Arial", 16, "bold"),
            bg="#2d3436",
            fg="#00d4ff"
        ).pack(pady=20)
        
        use_local = self.config_manager.get("use_local_ai", True)
        
        info_frame = tk.Frame(self.settings_frame, bg="#34495e", relief=tk.RAISED, bd=2)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        if use_local:
            engine_text = f"🏠 Ollama (Local)\nModel: {self.config_manager.get('ollama_model', 'llama2')}"
        else:
            engine_text = "☁️ Groq API (Cloud)"
        
        tk.Label(
            info_frame,
            text=f"Current Engine:\n{engine_text}",
            font=("Arial", 11),
            bg="#34495e",
            fg="#ffffff",
            justify=tk.CENTER
        ).pack(padx=20, pady=15)
        
        tk.Button(
            self.settings_frame,
            text="Change AI Engine",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.change_engine
        ).pack(pady=20)
    
    def change_engine(self):
        """Change AI engine"""
        if messagebox.askyesno("Change Engine", "This will restart Siya. Continue?"):
            for widget in self.root.winfo_children():
                widget.destroy()
            self.show_welcome_screen()
    
    def add_task(self):
        """Add a task"""
        task_text = self.task_entry.get().strip()
        if task_text:
            self.task_manager.add_task(task_text)
            self.task_entry.delete(0, tk.END)
            self.refresh_tasks()
            self.animated_cat.set_mood("excited")
            self.add_message("Siya", f"Task added: {task_text} ✅")
            self.root.after(2000, lambda: self.animated_cat.set_mood("happy"))
    
    def complete_task_handler(self, task_id):
        """Complete a task"""
        self.task_manager.complete_task(task_id)
        self.refresh_tasks()
        self.animated_cat.set_mood("loving")
        self.add_message("Siya", "Task completed! Great job! 🎉")
        self.root.after(2000, lambda: self.animated_cat.set_mood("happy"))
    
    def refresh_tasks(self):
        """Refresh tasks list"""
        for widget in self.tasks_inner_frame.winfo_children():
            widget.destroy()
        
        pending_tasks = self.task_manager.get_pending_tasks()
        
        if not pending_tasks:
            tk.Label(
                self.tasks_inner_frame,
                text="🎉 No pending tasks! You're all caught up!",
                font=("Arial", 11),
                bg="#34495e",
                fg="#00ff88",
                pady=20
            ).pack()
        else:
            for task in pending_tasks:
                task_frame = tk.Frame(self.tasks_inner_frame, bg="#2c3e50", relief=tk.RAISED, bd=1)
                task_frame.pack(fill=tk.X, padx=5, pady=5)
                
                tk.Label(
                    task_frame,
                    text=f"#{task['id']} {task['description']}",
                    font=("Arial", 10),
                    bg="#2c3e50",
                    fg="#ffffff",
                    anchor="w"
                ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
                
                tk.Button(
                    task_frame,
                    text="✓",
                    font=("Arial", 12, "bold"),
                    bg="#00ff88",
                    fg="#2d3436",
                    relief=tk.FLAT,
                    cursor="hand2",
                    width=3,
                    command=lambda tid=task['id']: self.complete_task_handler(tid)
                ).pack(side=tk.RIGHT, padx=10, pady=5)
    
    def add_message(self, sender, message):
        """Add message to chat"""
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if sender == "You":
            self.chat_display.insert(tk.END, f"\n[{timestamp}] 👤 You:\n", "user")
            self.chat_display.insert(tk.END, f"{message}\n", "user_msg")
        else:
            self.chat_display.insert(tk.END, f"\n[{timestamp}] 🐱 Siya:\n", "siya")
            self.chat_display.insert(tk.END, f"{message}\n", "siya_msg")
        
        self.chat_display.tag_config("user", foreground="#00d4ff", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("user_msg", foreground="#ffffff")
        self.chat_display.tag_config("siya", foreground="#00ff88", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("siya_msg", foreground="#ecf0f1")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def update_status(self, status_text):
        """Update status label"""
        self.status_label.config(text=status_text)
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.animated_cat.set_mood("happy")
        self.add_message("Siya", "Chat cleared! Ready for a fresh conversation! 🐱")
    
    def show_type_input(self):
        """Show/hide text input"""
        if self.text_input_frame.winfo_manager():
            self.text_input_frame.pack_forget()
        else:
            self.text_input_frame.pack(fill=tk.X, pady=(0, 10))
            self.text_entry.focus()
    
    def send_text_input(self):
        """Send text message"""
        user_text = self.text_entry.get().strip()
        if user_text:
            self.text_entry.delete(0, tk.END)
            self.text_input_frame.pack_forget()
            threading.Thread(target=self.process_input, args=(user_text,), daemon=True).start()
    
    def process_input(self, user_text):
        """Process user input"""
        try:
            self.add_message("You", user_text)
            
            self.animated_cat.set_mood("thinking")
            self.update_status("🤔 Thinking...")
            
            # Check for task commands
            if any(keyword in user_text.lower() for keyword in ["add task", "create task", "new task", "remind me"]):
                task_desc = user_text.lower()
                for word in ["add task", "create task", "new task", "remind me to", "remind me"]:
                    task_desc = task_desc.replace(word, "")
                task_desc = task_desc.strip()
                if task_desc:
                    self.task_manager.add_task(task_desc)
                    answer = f"Got it! Task added: '{task_desc}' 📝"
                    self.refresh_tasks()
                    self.animated_cat.set_mood("excited")
                else:
                    answer = "Sure! What task would you like me to add?"
            else:
                answer = ask_siya_free(user_text, self.config_manager)
            
            self.add_message("Siya", answer)
            
            self.animated_cat.set_mood("speaking")
            self.update_status("💬 Meow!")
            
            self.root.after(3000, lambda: self.animated_cat.set_mood("happy"))
            self.root.after(3000, lambda: self.update_status("😺 Ready to help!"))
            
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            self.add_message("System", f"Error: {str(e)}")
            self.animated_cat.set_mood("error")
            self.root.after(3000, lambda: self.animated_cat.set_mood("happy"))


def ask_siya_free(user_text, config):
    """Get AI response"""
    use_local_ai = config.get("use_local_ai", True)
    
    if use_local_ai:
        try:
            model = config.get("ollama_model", "llama2")
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": f"You are Siya, a helpful and friendly AI cat assistant. Be concise and add cat personality. User: {user_text}\nSiya:",
                    "stream": False
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return "Meow! I couldn't connect. Is Ollama running?\n\n💡 Start: ollama run " + model
        except:
            return "😿 Meow! I need Ollama!\n\nInstall: https://ollama.com\nRun: ollama run llama2"
    else:
        try:
            api_key = config.get("groq_api_key", "")
            if not api_key:
                return "😿 No API key! Go to ⚙️ Settings."
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are Siya, a helpful AI cat assistant! Be concise and friendly."},
                    {"role": "user", "content": user_text}
                ]
            }
            
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"😿 API error! Check ⚙️ Settings."
        except Exception as e:
            return f"😿 Error: {str(e)}"


def main():
    root = tk.Tk()
    app = SiyaCatUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
