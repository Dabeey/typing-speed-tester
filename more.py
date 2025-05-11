import tkinter as tk
from tkinter import messagebox
import time
import random

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Sample texts for typing test
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Python is an interpreted, high-level and general-purpose programming language.",
            "To be or not to be, that is the question.",
            "The journey of a thousand miles begins with one step.",
            "Programming isn't about what you know; it's about what you can figure out.",
            "The only way to learn a new programming language is by writing programs in it.",
            "In the middle of difficulty lies opportunity.",
            "Simplicity is the ultimate sophistication.",
            "The best way to predict the future is to invent it.",
            "Code is like humor. When you have to explain it, it's bad."
        ]
        
        self.current_text = ""
        self.start_time = 0
        self.running = False
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Typing Speed Test", 
            font=("Helvetica", 24, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=20)
        
        # Sample text display
        self.sample_label = tk.Label(
            self.root, 
            text="", 
            font=("Helvetica", 14),
            wraplength=700,
            justify="left",
            bg="#f0f0f0"
        )
        self.sample_label.pack(pady=20)
        
        # User input text area
        self.user_input = tk.Text(
            self.root, 
            height=10, 
            width=80,
            font=("Helvetica", 12),
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.user_input.pack(pady=10)
        self.user_input.bind("<Key>", self.start_test)
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg="#f0f0f0")
        stats_frame.pack(pady=20)
        
        # Words per minute label
        self.wpm_label = tk.Label(
            stats_frame, 
            text="WPM: 0", 
            font=("Helvetica", 14),
            bg="#f0f0f0"
        )
        self.wpm_label.pack(side=tk.LEFT, padx=20)
        
        # Accuracy label
        self.accuracy_label = tk.Label(
            stats_frame, 
            text="Accuracy: 0%", 
            font=("Helvetica", 14),
            bg="#f0f0f0"
        )
        self.accuracy_label.pack(side=tk.LEFT, padx=20)
        
        # Timer label
        self.timer_label = tk.Label(
            stats_frame, 
            text="Time: 0s", 
            font=("Helvetica", 14),
            bg="#f0f0f0"
        )
        self.timer_label.pack(side=tk.LEFT, padx=20)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=20)
        
        # Start/Reset button
        self.start_button = tk.Button(
            buttons_frame, 
            text="Start New Test", 
            command=self.start_new_test,
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        quit_button = tk.Button(
            buttons_frame, 
            text="Quit", 
            command=self.root.quit,
            font=("Helvetica", 12),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=10
        )
        quit_button.pack(side=tk.LEFT, padx=10)
        
        # Initialize with a new test
        self.start_new_test()
    
    def start_new_test(self):
        self.current_text = random.choice(self.sample_texts)
        self.sample_label.config(text=self.current_text)
        self.user_input.delete("1.0", tk.END)
        self.user_input.config(state=tk.NORMAL)
        self.running = False
        self.start_time = 0
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 0%")
        self.timer_label.config(text="Time: 0s")
        self.user_input.focus()
    
    def start_test(self, event):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.update_timer()
    
    def update_timer(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {int(elapsed_time)}s")
            
            # Calculate WPM and accuracy
            typed_text = self.user_input.get("1.0", tk.END).strip()
            self.calculate_stats(typed_text)
            
            # Schedule next update
            self.root.after(1000, self.update_timer)
    
    def calculate_stats(self, typed_text):
        # Calculate time in minutes
        elapsed_time = (time.time() - self.start_time) / 60
        
        # Count words in original and typed text
        original_words = self.current_text.split()
        typed_words = typed_text.split()
        
        # Calculate WPM (words per minute)
        word_count = len(typed_words)
        wpm = int(word_count / elapsed_time) if elapsed_time > 0 else 0
        self.wpm_label.config(text=f"WPM: {wpm}")
        
        # Calculate accuracy
        correct_chars = 0
        min_length = min(len(self.current_text), len(typed_text))
        
        for i in range(min_length):
            if self.current_text[i] == typed_text[i]:
                correct_chars += 1
        
        accuracy = (correct_chars / len(self.current_text)) * 100 if len(self.current_text) > 0 else 0
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
        
        # Check if test is complete
        if len(typed_text) >= len(self.current_text):
            self.running = False
            self.show_results(wpm, accuracy)
    
    def show_results(self, wpm, accuracy):
        messagebox.showinfo(
            "Test Complete",
            f"Your typing speed: {wpm} WPM\nAccuracy: {accuracy:.1f}%"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()