import os
import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
from openai import OpenAI
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import pyttsx3
from datetime import datetime
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SAMPLE_RATE = 16000
RECORD_SECONDS = 5


class SiyaCatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐱 Siya - Your AI Cat Assistant")
        self.root.geometry("600x800")
        self.root.configure(bg="#1a1a2e")
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 175)
        self.tts_engine.setProperty('volume', 0.9)
        
        # Animation states
        self.is_listening = False
        self.is_thinking = False
        self.is_speaking = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header with cat face
        header_frame = tk.Frame(self.root, bg="#16213e", height=200)
        header_frame.pack(fill=tk.X, pady=10, padx=10)
        header_frame.pack_propagate(False)
        
        # Cat ASCII art display
        self.cat_canvas = tk.Canvas(header_frame, bg="#16213e", height=180, highlightthickness=0)
        self.cat_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.draw_cat_idle()
        
        # Status label
        self.status_label = tk.Label(
            self.root, 
            text="😺 Ready to help!",
            font=("Arial", 14, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        self.status_label.pack(pady=10)
        
        # Chat display area
        chat_frame = tk.Frame(self.root, bg="#1a1a2e")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(
            chat_frame, 
            text="💬 Conversation",
            font=("Arial", 12, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        ).pack(anchor=tk.W)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#0f3460",
            fg="#e9ecef",
            insertbackground="#00d4ff",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=5)
        self.chat_display.config(state=tk.DISABLED)
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg="#1a1a2e")
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.voice_button = tk.Button(
            button_frame,
            text="🎤 Hold to Speak",
            font=("Arial", 12, "bold"),
            bg="#00d4ff",
            fg="#1a1a2e",
            activebackground="#00a8cc",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_voice_input
        )
        self.voice_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.type_button = tk.Button(
            button_frame,
            text="⌨️ Type Message",
            font=("Arial", 12, "bold"),
            bg="#e94560",
            fg="#ffffff",
            activebackground="#c7354f",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_type_input
        )
        self.type_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Text input frame (hidden by default)
        self.text_input_frame = tk.Frame(self.root, bg="#1a1a2e")
        
        self.text_entry = tk.Entry(
            self.text_input_frame,
            font=("Arial", 11),
            bg="#0f3460",
            fg="#ffffff",
            insertbackground="#00d4ff",
            relief=tk.FLAT
        )
        self.text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5))
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
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Initial greeting
        self.add_message("Siya", "Meow! 🐱 I'm Siya, your AI cat assistant! Press the microphone button or type to talk with me!")
        
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
            300, 90,
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
            300, 90,
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
            300, 90,
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
            300, 90,
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
        
        # Configure tags
        self.chat_display.tag_config("user", foreground="#00d4ff", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("user_msg", foreground="#ffffff")
        self.chat_display.tag_config("siya", foreground="#00ff88", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("siya_msg", foreground="#e9ecef")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def update_status(self, status_text):
        self.status_label.config(text=status_text)
        
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
            self.update_status("🤔 Understanding your words...")
            
            user_text = transcribe_audio(audio_file)
            
            if os.path.exists(audio_file):
                os.remove(audio_file)
            
            self.process_input(user_text)
            
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            self.add_message("System", f"Error occurred: {str(e)}")
        finally:
            self.is_listening = False
            self.voice_button.config(state=tk.NORMAL)
            self.draw_cat_idle()
            
    def process_input(self, user_text):
        try:
            self.add_message("You", user_text)
            
            self.draw_cat_thinking()
            self.update_status("🧠 Thinking...")
            
            answer = ask_siya(user_text)
            
            self.add_message("Siya", answer)
            
            # Speak the response
            self.draw_cat_speaking()
            self.update_status("💬 Speaking...")
            self.speak(answer)
            
            self.draw_cat_idle()
            self.update_status("😺 Ready to help!")
            
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            self.add_message("System", f"Error: {str(e)}")
            self.draw_cat_idle()
            
    def speak(self, text):
        try:
            self.tts_engine.say(text)
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

You have a playful cat personality but are very capable at helping with:
- Answering questions
- Providing information  
- Helping with tasks
- Web searches (when needed)
- Giving advice
- Having friendly conversations

Be concise since your responses will be spoken aloud.
Add occasional cat puns and cat-themed responses when appropriate.
Be warm, helpful, and encouraging!"""
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