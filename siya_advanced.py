"""
Siya Advanced - AI Cat Assistant with Task Management
Features: Voice, Text, GUI, Task Handling, Reminders
"""

import os
import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
from openai import OpenAI
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import pyttsx3
from datetime import datetime
import json
import webbrowser
from pathlib import Path

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SAMPLE_RATE = 16000
RECORD_SECONDS = 5


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
    
    def get_all_tasks(self):
        return self.tasks


class SiyaCatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐱 Siya Advanced - AI Cat Assistant")
        self.root.geometry("700x900")
        self.root.configure(bg="#1a1a2e")
        
        # Initialize components
        self.task_manager = TaskManager()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 175)
        self.tts_engine.setProperty('volume', 0.9)
        
        # States
        self.is_listening = False
        self.is_thinking = False
        self.is_speaking = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure notebook style
        style = ttk.Style()
        style.configure('TNotebook', background="#1a1a2e")
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # Create tabs
        self.chat_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.tasks_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        
        self.notebook.add(self.chat_frame, text="💬 Chat")
        self.notebook.add(self.tasks_frame, text="✅ Tasks")
        
        self.setup_chat_tab()
        self.setup_tasks_tab()
        
    def setup_chat_tab(self):
        # Header with cat face
        header_frame = tk.Frame(self.chat_frame, bg="#16213e", height=180)
        header_frame.pack(fill=tk.X, pady=10, padx=10)
        header_frame.pack_propagate(False)
        
        # Cat canvas
        self.cat_canvas = tk.Canvas(header_frame, bg="#16213e", height=160, highlightthickness=0)
        self.cat_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_cat_idle()
        
        # Status label
        self.status_label = tk.Label(
            self.chat_frame, 
            text="😺 Ready to help!",
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
        
        self.voice_button = tk.Button(
            button_frame,
            text="🎤 Speak",
            font=("Arial", 11, "bold"),
            bg="#00d4ff",
            fg="#1a1a2e",
            activebackground="#00a8cc",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_voice_input
        )
        self.voice_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        self.type_button = tk.Button(
            button_frame,
            text="⌨️ Type",
            font=("Arial", 11, "bold"),
            bg="#e94560",
            fg="#ffffff",
            activebackground="#c7354f",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_type_input
        )
        self.type_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
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
        self.add_message("Siya", "Meow! 🐱 I'm Siya, your advanced AI cat assistant! I can chat, manage tasks, search the web, and more!")
        
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
        
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.task_manager.add_task(task_text)
            self.task_entry.delete(0, tk.END)
            self.refresh_tasks()
            self.speak("Task added successfully!")
            
    def complete_task_handler(self, task_id):
        self.task_manager.complete_task(task_id)
        self.refresh_tasks()
        self.speak("Task completed! Great job!")
        
    def refresh_tasks(self):
        # Clear existing task widgets
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
        
    def draw_cat_idle(self):
        self.cat_canvas.delete("all")
        cat_art = """
        /\\_/\\
       ( o.o )
        > ^ <
       /|   |\\
      (_|   |_)
        """
        self.cat_canvas.create_text(
            self.cat_canvas.winfo_reqwidth() / 2 or 300, 80,
            text=cat_art,
            font=("Courier", 16, "bold"),
            fill="#00d4ff",
            justify=tk.CENTER
        )
        
    def draw_cat_listening(self):
        self.cat_canvas.delete("all")
        cat_art = """
        /\\_/\\
       ( ^.^ )
        > ♫ <
       /|   |\\
      (_|   |_)
        """
        self.cat_canvas.create_text(
            self.cat_canvas.winfo_reqwidth() / 2 or 300, 80,
            text=cat_art,
            font=("Courier", 16, "bold"),
            fill="#00ff88",
            justify=tk.CENTER
        )
        
    def draw_cat_thinking(self):
        self.cat_canvas.delete("all")
        cat_art = """
        /\\_/\\
       ( -.- )
        > ? <
       /|   |\\
      (_|   |_)
        """
        self.cat_canvas.create_text(
            self.cat_canvas.winfo_reqwidth() / 2 or 300, 80,
            text=cat_art,
            font=("Courier", 16, "bold"),
            fill="#ffaa00",
            justify=tk.CENTER
        )
        
    def draw_cat_speaking(self):
        self.cat_canvas.delete("all")
        cat_art = """
        /\\_/\\
       ( ^ω^ )
        > 💬 <
       /|   |\\
      (_|   |_)
        """
        self.cat_canvas.create_text(
            self.cat_canvas.winfo_reqwidth() / 2 or 300, 80,
            text=cat_art,
            font=("Courier", 16, "bold"),
            fill="#ff55ff",
            justify=tk.CENTER
        )
        
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
            
    def start_voice_input(self):
        if not self.is_listening:
            threading.Thread(target=self.voice_input_thread, daemon=True).start()
            
    def voice_input_thread(self):
        try:
            self.is_listening = True
            self.draw_cat_listening()
            self.update_status("🎤 Listening... Speak now!")
            self.voice_button.config(state=tk.DISABLED)
            
            audio_file = record_voice()
            
            self.draw_cat_thinking()
            self.update_status("🤔 Understanding...")
            
            user_text = transcribe_audio(audio_file)
            
            if os.path.exists(audio_file):
                os.remove(audio_file)
            
            self.process_input(user_text)
            
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            self.add_message("System", f"Error: {str(e)}")
        finally:
            self.is_listening = False
            self.voice_button.config(state=tk.NORMAL)
            self.draw_cat_idle()
            
    def process_input(self, user_text):
        try:
            self.add_message("You", user_text)
            
            self.draw_cat_thinking()
            self.update_status("🧠 Thinking...")
            
            # Check for task commands
            if any(keyword in user_text.lower() for keyword in ["add task", "create task", "new task", "remind me"]):
                task_desc = user_text.lower().replace("add task", "").replace("create task", "").replace("new task", "").replace("remind me to", "").replace("remind me", "").strip()
                if task_desc:
                    self.task_manager.add_task(task_desc)
                    answer = f"Got it! I've added '{task_desc}' to your task list. Check the Tasks tab to see it! 📝"
                    self.refresh_tasks()
                else:
                    answer = "Sure! What task would you like me to add?"
            else:
                answer = ask_siya(user_text)
            
            self.add_message("Siya", answer)
            
            self.draw_cat_speaking()
            self.update_status("💬 Speaking...")
            self.speak(answer)
            
            self.draw_cat_idle()
            self.update_status("😺 Ready!")
            
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            self.add_message("System", f"Error: {str(e)}")
            self.draw_cat_idle()
            
    def speak(self, text):
        try:
            # Remove emojis for better TTS
            clean_text = ''.join(char for char in text if ord(char) < 0x10000)
            self.tts_engine.say(clean_text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")


def record_voice():
    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    
    file_path = tempfile.mktemp(suffix=".wav")
    write(file_path, SAMPLE_RATE, audio)
    
    return file_path


def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text


def ask_siya(user_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are Siya, a helpful and friendly AI cat assistant! 🐱

You're capable, intelligent, and have a warm personality. You can help with:
- Answering questions and providing information
- Task management and organization
- Web searches (when needed for current info)
- Code help and debugging
- Writing and editing
- Math and calculations
- General advice and conversation
- Creative ideas and brainstorming

Keep responses concise for voice output (2-3 sentences unless detail is needed).
Add cat puns occasionally when appropriate.
Be encouraging and supportive!
Use emojis sparingly for personality."""
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )
    
    return response.choices[0].message.content


def main():
    root = tk.Tk()
    app = SiyaCatUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
