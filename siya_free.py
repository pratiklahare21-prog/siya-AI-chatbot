"""
Siya Free - AI Cat Assistant with FREE AI API
No OpenAI credits needed! Uses Groq's free API
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import pyttsx3
from datetime import datetime
import json
from pathlib import Path
import requests

# Free Groq API (no credit card needed!)
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "gsk_your_free_api_key_here"  # Get from https://console.groq.com

# Or use local Ollama (completely free, runs on your PC)
USE_LOCAL_AI = True  # Set to True to use Ollama instead


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


class SiyaCatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐱 Siya Free - AI Cat Assistant")
        self.root.geometry("700x900")
        self.root.configure(bg="#1a1a2e")
        
        # Initialize components
        self.task_manager = TaskManager()
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 175)
            self.tts_engine.setProperty('volume', 0.9)
            self.tts_enabled = True
        except:
            self.tts_enabled = False
            print("TTS not available, text only mode")
        
        # Cat mood
        self.current_mood = "happy"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create notebook for tabs
        from tkinter import ttk
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.chat_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.tasks_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        
        self.notebook.add(self.chat_frame, text="💬 Chat")
        self.notebook.add(self.tasks_frame, text="✅ Tasks")
        
        self.setup_chat_tab()
        self.setup_tasks_tab()
        
    def setup_chat_tab(self):
        # Header with BIG emoji cat
        header_frame = tk.Frame(self.chat_frame, bg="#16213e", height=200)
        header_frame.pack(fill=tk.X, pady=10, padx=10)
        header_frame.pack_propagate(False)
        
        # Cat emoji display
        self.cat_label = tk.Label(
            header_frame,
            text="😺",
            font=("Segoe UI Emoji", 120),
            bg="#16213e",
            fg="#ffffff"
        )
        self.cat_label.pack(expand=True)
        
        # Status label
        self.status_label = tk.Label(
            self.chat_frame, 
            text="😺 Meow! I'm ready to help!",
            font=("Arial", 14, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        self.status_label.pack(pady=10)
        
        # Chat display
        chat_container = tk.Frame(self.chat_frame, bg="#1a1a2e")
        chat_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(
            chat_container, 
            text="💬 Conversation",
            font=("Arial", 11, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#0f3460",
            fg="#e9ecef",
            insertbackground="#00d4ff",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Control buttons
        button_frame = tk.Frame(self.chat_frame, bg="#1a1a2e")
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            button_frame,
            text="⌨️ Type Message",
            font=("Arial", 11, "bold"),
            bg="#00d4ff",
            fg="#1a1a2e",
            activebackground="#00a8cc",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_type_input
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=("Arial", 11, "bold"),
            bg="#6c757d",
            fg="#ffffff",
            activebackground="#5a6268",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_chat
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Text input frame
        self.text_input_frame = tk.Frame(self.chat_frame, bg="#1a1a2e")
        
        self.text_entry = tk.Entry(
            self.text_input_frame,
            font=("Arial", 11),
            bg="#0f3460",
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
            fg="#1a1a2e",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.send_text_input
        ).pack(side=tk.LEFT, padx=(0, 10), pady=5)
        
        # Initial greeting
        self.add_message("Siya", "Meow! 🐱 I'm Siya, your FREE AI cat assistant! No API costs! Type to chat with me!")
        
    def setup_tasks_tab(self):
        # Header
        header = tk.Frame(self.tasks_frame, bg="#1a1a2e")
        header.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            header,
            text="✅ Task Manager",
            font=("Arial", 16, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        ).pack(side=tk.LEFT)
        
        tk.Button(
            header,
            text="🔄 Refresh",
            font=("Arial", 10, "bold"),
            bg="#6c757d",
            fg="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.refresh_tasks
        ).pack(side=tk.RIGHT)
        
        # Add task section
        add_frame = tk.Frame(self.tasks_frame, bg="#16213e")
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            add_frame,
            text="Add New Task:",
            font=("Arial", 10, "bold"),
            bg="#16213e",
            fg="#ffffff"
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        task_input_frame = tk.Frame(add_frame, bg="#16213e")
        task_input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.task_entry = tk.Entry(
            task_input_frame,
            font=("Arial", 11),
            bg="#0f3460",
            fg="#ffffff",
            insertbackground="#00d4ff",
            relief=tk.FLAT
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        tk.Button(
            task_input_frame,
            text="+ Add Task",
            font=("Arial", 10, "bold"),
            bg="#00d4ff",
            fg="#1a1a2e",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.add_task
        ).pack(side=tk.LEFT)
        
        # Tasks list
        tk.Label(
            self.tasks_frame,
            text="Pending Tasks:",
            font=("Arial", 11, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Scrollable task list
        list_frame = tk.Frame(self.tasks_frame, bg="#1a1a2e")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tasks_canvas = tk.Canvas(list_frame, bg="#0f3460", highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.tasks_canvas.yview)
        self.tasks_inner_frame = tk.Frame(self.tasks_canvas, bg="#0f3460")
        
        self.tasks_inner_frame.bind(
            "<Configure>",
            lambda e: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        )
        
        self.tasks_canvas.create_window((0, 0), window=self.tasks_inner_frame, anchor="nw")
        self.tasks_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.tasks_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.refresh_tasks()
        
    def set_cat_mood(self, mood):
        """Change cat emoji based on mood"""
        moods = {
            "happy": "😺",
            "listening": "😸",
            "thinking": "🤔",
            "speaking": "😻",
            "excited": "😹",
            "loving": "😽",
            "sleepy": "😿",
            "surprised": "🙀",
            "grumpy": "😾"
        }
        self.current_mood = mood
        self.cat_label.config(text=moods.get(mood, "😺"))
        
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.task_manager.add_task(task_text)
            self.task_entry.delete(0, tk.END)
            self.refresh_tasks()
            self.set_cat_mood("excited")
            self.add_message("Siya", f"Task added: {task_text} ✅")
            self.root.after(2000, lambda: self.set_cat_mood("happy"))
            
    def complete_task_handler(self, task_id):
        self.task_manager.complete_task(task_id)
        self.refresh_tasks()
        self.set_cat_mood("loving")
        self.add_message("Siya", "Task completed! Great job! 🎉")
        self.root.after(2000, lambda: self.set_cat_mood("happy"))
        
    def refresh_tasks(self):
        for widget in self.tasks_inner_frame.winfo_children():
            widget.destroy()
        
        pending_tasks = self.task_manager.get_pending_tasks()
        
        if not pending_tasks:
            tk.Label(
                self.tasks_inner_frame,
                text="🎉 No pending tasks! You're all caught up!",
                font=("Arial", 11),
                bg="#0f3460",
                fg="#00ff88",
                pady=20
            ).pack()
        else:
            for task in pending_tasks:
                task_frame = tk.Frame(self.tasks_inner_frame, bg="#16213e", relief=tk.RAISED, bd=1)
                task_frame.pack(fill=tk.X, padx=5, pady=5)
                
                tk.Label(
                    task_frame,
                    text=f"#{task['id']} {task['description']}",
                    font=("Arial", 10),
                    bg="#16213e",
                    fg="#ffffff",
                    anchor="w"
                ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
                
                tk.Button(
                    task_frame,
                    text="✓ Done",
                    font=("Arial", 9, "bold"),
                    bg="#00ff88",
                    fg="#1a1a2e",
                    relief=tk.FLAT,
                    cursor="hand2",
                    command=lambda tid=task['id']: self.complete_task_handler(tid)
                ).pack(side=tk.RIGHT, padx=10, pady=5)
        
    def add_message(self, sender, message):
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
        self.chat_display.tag_config("siya_msg", foreground="#e9ecef")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def update_status(self, status_text):
        self.status_label.config(text=status_text)
        
    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.set_cat_mood("happy")
        self.add_message("Siya", "Chat cleared! Ready for a fresh conversation! 🐱")
        
    def show_type_input(self):
        if self.text_input_frame.winfo_manager():
            self.text_input_frame.pack_forget()
        else:
            self.text_input_frame.pack(fill=tk.X, pady=(0, 10))
            self.text_entry.focus()
            
    def send_text_input(self):
        user_text = self.text_entry.get().strip()
        if user_text:
            self.text_entry.delete(0, tk.END)
            self.text_input_frame.pack_forget()
            threading.Thread(target=self.process_input, args=(user_text,), daemon=True).start()
            
    def process_input(self, user_text):
        try:
            self.add_message("You", user_text)
            
            self.set_cat_mood("thinking")
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
                    self.set_cat_mood("excited")
                else:
                    answer = "Sure! What task would you like me to add?"
            else:
                answer = ask_siya_free(user_text)
            
            self.add_message("Siya", answer)
            
            self.set_cat_mood("speaking")
            self.update_status("💬 Meow!")
            
            self.root.after(3000, lambda: self.set_cat_mood("happy"))
            self.root.after(3000, lambda: self.update_status("😺 Ready to help!"))
            
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            self.add_message("System", f"Error: {str(e)}")
            self.set_cat_mood("surprised")
            self.root.after(3000, lambda: self.set_cat_mood("happy"))


def ask_siya_free(user_text):
    """Use FREE AI - either Ollama (local) or Groq (online)"""
    
    if USE_LOCAL_AI:
        # Use Ollama (completely free, runs on your PC)
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama2",
                    "prompt": f"You are Siya, a helpful and friendly AI cat assistant. Be concise and add cat personality. User: {user_text}\nSiya:",
                    "stream": False
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return "Meow! I couldn't connect to my brain. Is Ollama running? Start it with: ollama run llama2"
        except:
            return "😿 Meow! I need Ollama to be installed and running!\n\nInstall: https://ollama.com\nThen run: ollama run llama2\n\nOr set USE_LOCAL_AI = False to use Groq API instead!"
    
    else:
        # Use Groq (free online API, needs API key)
        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Siya, a helpful and friendly AI cat assistant! Be concise (2-3 sentences), warm, and add occasional cat personality."
                    },
                    {
                        "role": "user",
                        "content": user_text
                    }
                ]
            }
            
            response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"😿 Meow! API error: {response.status_code}\n\nGet a FREE Groq API key at: https://console.groq.com\nThen update GROQ_API_KEY in the code!"
        except Exception as e:
            return f"😿 Meow! Error: {str(e)}\n\nOption 1: Get free Groq API key at https://console.groq.com\nOption 2: Install Ollama and set USE_LOCAL_AI = True"


def main():
    root = tk.Tk()
    app = SiyaCatUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
