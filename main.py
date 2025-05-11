import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import time
import random
import json
import os
from datetime import datetime

class TypingSpeedTestPro:
    """
    TYPING SPEED TEST PRO
    Copyright © 2025 Dabeey. All Rights Reserved.
    ™ Dabeey - Your Favorite Backend Girl
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test Pro™")
        self.root.geometry("900x700")
        
        # Copyright and trademark information
        self.copyright_notice = "© 2025 Dabeey. All Rights Reserved."
        self.trademark = "Typing Speed Test Pro™"
        self.company = "Dabeey"
        self.signature = "Your Favorite Backend Girl"
        
        # Sample texts for different difficulty levels
        self.sample_texts = {
            "easy": [
                "The quick brown fox jumps over the lazy dog.",
                "Python is a popular programming language.",
                "Practice makes perfect.",
                "The early bird catches the worm."
            ],
            "medium": [
                "Python is an interpreted, high-level, general-purpose programming language.",
                "The journey of a thousand miles begins with a single step.",
                "Programming isn't about what you know; it's about what you can figure out.",
                "In the middle of difficulty lies opportunity."
            ],
            "hard": [
                "The Zen of Python states that 'Beautiful is better than ugly. Explicit is better than implicit.'",
                "Computer science is no more about computers than astronomy is about telescopes.",
                "The best way to predict the future is to invent it. The future is something which everyone reaches at the rate of sixty minutes an hour.",
                "Any fool can write code that a computer can understand. Good programmers write code that humans can understand."
            ]
        }
        
        # Initialize variables
        self.current_text = ""
        self.start_time = 0
        self.running = False
        self.difficulty = tk.StringVar(value="medium")
        self.history = []
        self.high_scores = {"easy": [], "medium": [], "hard": []}
        
        # Brand colors
        self.brand_colors = {
            "bg_color": "#2E3440",
            "text_bg": "#3B4252",
            "fg_color": "#ECEFF4",
            "accent_color": "#88C0D0",
            "button_color": "#5E81AC",
            "error_color": "#BF616A",
            "brand_color": "#FFA500"  # Orange as brand color
        }
        
        # Setup UI
        self.setup_ui()
        
        # Load scores
        self.load_scores()
        
        # Start with a new test
        self.start_new_test()
        
        # Add branding
        self.add_branding()

    def add_branding(self):
        """Add copyright and branding to main window"""
        footer = tk.Frame(self.root, bg=self.brand_colors["bg_color"])
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        tk.Label(
            footer,
            text=f"{self.trademark} | {self.copyright_notice} | {self.company}",
            font=("Helvetica", 8),
            bg=self.brand_colors["bg_color"],
            fg=self.brand_colors["fg_color"]
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            footer,
            text=f"Created by: {self.signature}",
            font=("Helvetica", 8, "italic"),
            bg=self.brand_colors["bg_color"],
            fg=self.brand_colors["brand_color"]
        ).pack(side=tk.RIGHT, padx=10)

    def add_window_branding(self, window):
        """Add branding to secondary windows"""
        footer = tk.Frame(window, bg=self.brand_colors["bg_color"])
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        tk.Label(
            footer,
            text=f"{self.trademark} | {self.copyright_notice}",
            font=("Helvetica", 8),
            bg=self.brand_colors["bg_color"],
            fg=self.brand_colors["fg_color"]
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            footer,
            text=self.company,
            font=("Helvetica", 8, "italic"),
            bg=self.brand_colors["bg_color"],
            fg=self.brand_colors["brand_color"]
        ).pack(side=tk.RIGHT, padx=10)

    def setup_ui(self):
        """Set up the user interface"""
        # Configure root window
        self.root.configure(bg=self.brand_colors["bg_color"])
        
        # Brand header
        header = tk.Frame(self.root, bg=self.brand_colors["brand_color"])
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=self.trademark,
            font=("Helvetica", 24, "bold"),
            bg=self.brand_colors["brand_color"],
            fg="black"
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        # Difficulty selector
        diff_frame = tk.Frame(header, bg=self.brand_colors["brand_color"])
        diff_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(
            diff_frame,
            text="Difficulty:",
            font=("Helvetica", 11),
            bg=self.brand_colors["brand_color"],
            fg="black"
        ).pack(side=tk.LEFT)
        
        for level in ["easy", "medium", "hard"]:
            rb = tk.Radiobutton(
                diff_frame,
                text=level.capitalize(),
                variable=self.difficulty,
                value=level,
                font=("Helvetica", 10),
                bg=self.brand_colors["brand_color"],
                fg="black",
                selectcolor=self.brand_colors["brand_color"],
                activebackground=self.brand_colors["brand_color"],
                activeforeground="black",
                highlightthickness=0,
                command=self.start_new_test
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # Instructions
        tk.Label(
            self.root,
            text="Type the text below as quickly and accurately as possible:",
            font=("Helvetica", 11),
            bg=self.brand_colors["bg_color"],
            fg=self.brand_colors["fg_color"]
        ).pack()
        
        # Sample text display with frame
        sample_frame = tk.Frame(self.root, bg=self.brand_colors["bg_color"])
        sample_frame.pack(pady=(10, 5), padx=20, fill=tk.X)
        
        self.sample_label = tk.Label(
            sample_frame, 
            text="", 
            font=("Helvetica", 14),
            wraplength=800,
            justify="left",
            bg=self.brand_colors["text_bg"],
            fg=self.brand_colors["fg_color"],
            padx=15,
            pady=15,
            relief=tk.SUNKEN
        )
        self.sample_label.pack(fill=tk.X)
        
        # User input text area with scrollbar
        input_frame = tk.Frame(self.root, bg=self.brand_colors["bg_color"])
        input_frame.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(input_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.user_input = tk.Text(
            input_frame, 
            height=10, 
            width=80,
            font=("Helvetica", 12),
            wrap=tk.WORD,
            bg=self.brand_colors["text_bg"],
            fg=self.brand_colors["fg_color"],
            insertbackground=self.brand_colors["fg_color"],
            selectbackground=self.brand_colors["accent_color"],
            yscrollcommand=scrollbar.set,
            padx=10,
            pady=10
        )
        self.user_input.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.user_input.yview)
        
        self.user_input.bind("<Key>", self.on_key_press)
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg=self.brand_colors["bg_color"])
        stats_frame.pack(pady=15, fill=tk.X)
        
        stats = [
            ("WPM", "wpm_label", "0"),
            ("Accuracy", "accuracy_label", "0%"),
            ("Time", "timer_label", "0s"),
            ("Chars", "chars_label", "0/0"),
            ("Errors", "errors_label", "0")
        ]
        
        for text, attr, value in stats:
            frame = tk.Frame(stats_frame, bg=self.brand_colors["bg_color"])
            frame.pack(side=tk.LEFT, expand=True)
            
            tk.Label(
                frame,
                text=text,
                font=("Helvetica", 11),
                bg=self.brand_colors["bg_color"],
                fg=self.brand_colors["fg_color"]
            ).pack()
            
            label = tk.Label(
                frame,
                text=value,
                font=("Helvetica", 14, "bold"),
                bg=self.brand_colors["bg_color"],
                fg=self.brand_colors["accent_color"]
            )
            label.pack()
            setattr(self, attr, label)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg=self.brand_colors["bg_color"])
        buttons_frame.pack(pady=(10, 20))
        
        button_config = {
            "font": ("Helvetica", 12),
            "padx": 25,
            "pady": 8,
            "borderwidth": 0,
            "highlightthickness": 0,
            "fg": self.brand_colors["fg_color"]
        }
        
        self.start_button = tk.Button(
            buttons_frame, 
            text="Start New Test", 
            command=self.start_new_test,
            bg=self.brand_colors["button_color"],
            activebackground=self.brand_colors["accent_color"],
            **button_config
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            buttons_frame, 
            text="View History", 
            command=self.show_history,
            bg=self.brand_colors["button_color"],
            activebackground=self.brand_colors["accent_color"],
            **button_config
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            buttons_frame, 
            text="High Scores", 
            command=self.show_high_scores,
            bg=self.brand_colors["button_color"],
            activebackground=self.brand_colors["accent_color"],
            **button_config
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            buttons_frame, 
            text="Export Results", 
            command=self.export_results,
            bg=self.brand_colors["button_color"],
            activebackground=self.brand_colors["accent_color"],
            **button_config
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            buttons_frame, 
            text="About", 
            command=self.show_about,
            bg=self.brand_colors["brand_color"],
            activebackground="#FFD700",
            # fg="black",
            **button_config
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            buttons_frame, 
            text="Quit", 
            command=self.quit_app,
            bg="#BF616A",
            activebackground="#D08770",
            **button_config
        ).pack(side=tk.LEFT, padx=10)

    def show_about(self):
        """Show about dialog with copyright information"""
        about_text = (
            f"{self.trademark}\n\n"
            f"Version 1.0\n\n"
            f"{self.copyright_notice}\n"
            f"Developed by {self.signature}\n"
            f"{self.company}\n\n"
            "This software is protected by copyright law and international treaties."
        )
        
        messagebox.showinfo(
            f"About {self.trademark}",
            about_text
        )

    def load_scores(self):
        """Load saved scores from file"""
        if os.path.exists("typing_scores.json"):
            try:
                with open("typing_scores.json", "r") as f:
                    data = json.load(f)
                    self.history = data.get("history", [])
                    self.high_scores = data.get("high_scores", {"easy": [], "medium": [], "hard": []})
            except:
                self.history = []
                self.high_scores = {"easy": [], "medium": [], "hard": []}

    def save_scores(self):
        """Save scores to file"""
        data = {
            "history": self.history,
            "high_scores": self.high_scores
        }
        with open("typing_scores.json", "w") as f:
            json.dump(data, f)

    def start_new_test(self):
        """Start a new typing test"""
        self.current_text = random.choice(self.sample_texts[self.difficulty.get()])
        self.sample_label.config(text=self.current_text)
        self.user_input.delete("1.0", tk.END)
        self.user_input.config(state=tk.NORMAL)
        self.running = False
        self.start_time = 0
        self.wpm_label.config(text="0")
        self.accuracy_label.config(text="0%")
        self.timer_label.config(text="0s")
        self.chars_label.config(text="0/0")
        self.errors_label.config(text="0")
        self.user_input.focus()
        self.user_input.tag_remove("error", "1.0", tk.END)

    def on_key_press(self, event):
        """Handle key press events"""
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.update_timer()

        # Update stats immediately for responsive feedback
        self.update_stats()

        # Highlight errors in real-time
        self.highlight_errors()

        # Automatically stop if the text matches exactly
        typed_text = self.user_input.get("1.0", tk.END).strip()
        if typed_text == self.current_text:
            self.running = False
            elapsed_time = (time.time() - self.start_time) / 60
            wpm = int(len(typed_text.split()) / elapsed_time) if elapsed_time > 0 else 0
            char_accuracy = (len(self.current_text) / len(self.current_text) * 100) if self.current_text else 0
            word_accuracy = 100  # Since the text matches exactly
            self.save_result(wpm, char_accuracy, word_accuracy)
            self.show_results(wpm, char_accuracy, word_accuracy)


    def update_timer(self):
        """Update the timer display"""
        if self.running:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"{int(elapsed_time)}s")
            self.root.after(1000, self.update_timer)

    def update_stats(self):
        """Calculate and update all statistics"""
        typed_text = self.user_input.get("1.0", tk.END).strip()
        elapsed_time = (time.time() - self.start_time) / 60 if self.start_time > 0 else 0
        
        # Character-level statistics
        original_chars = len(self.current_text)
        typed_chars = len(typed_text)
        min_length = min(original_chars, typed_chars)
        
        correct_chars = sum(
            1 for i in range(min_length) 
            if self.current_text[i] == typed_text[i]
        )
        error_count = min_length - correct_chars
        
        # Word-level statistics
        original_words = self.current_text.split()
        typed_words = typed_text.split()
        
        # Calculate WPM (words per minute)
        wpm = int(len(typed_words) / elapsed_time) if elapsed_time > 0 else 0
        
        # Calculate accuracy
        char_accuracy = (correct_chars / original_chars * 100) if original_chars > 0 else 0
        
        # Update all displays
        self.wpm_label.config(text=f"{wpm}")
        self.accuracy_label.config(text=f"{char_accuracy:.1f}%")
        self.chars_label.config(text=f"{correct_chars}/{original_chars}")
        self.errors_label.config(text=f"{error_count}")
        
        # Check if test is complete
        if len(typed_text) >= len(self.current_text):
            self.running = False
            word_accuracy = (sum(1 for i in range(min(len(original_words), len(typed_words))) 
                            if original_words[i] == typed_words[i]) / len(original_words) * 100 
                            if original_words else 0)
            
            self.save_result(wpm, char_accuracy, word_accuracy)
            self.show_results(wpm, char_accuracy, word_accuracy)

    def highlight_errors(self):
        """Highlight incorrect characters in real-time"""
        typed_text = self.user_input.get("1.0", tk.END)
        self.user_input.tag_remove("error", "1.0", tk.END)
        
        for i in range(min(len(typed_text), len(self.current_text))):
            if typed_text[i] != self.current_text[i]:
                line = typed_text.count('\n', 0, i) + 1
                col = i - typed_text.rfind('\n', 0, i) - 1 if '\n' in typed_text[:i] else i
                self.user_input.tag_add("error", f"{line}.{col}")
        
        self.user_input.tag_config("error", foreground=self.brand_colors["error_color"])

    def save_result(self, wpm, char_accuracy, word_accuracy):
        """Save the current test result"""
        result = {
            "wpm": wpm,
            "char_accuracy": f"{char_accuracy:.1f}%",
            "word_accuracy": f"{word_accuracy:.1f}%",
            "difficulty": self.difficulty.get(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        # Add to history
        self.history.append(result)
        
        # Add to high scores
        difficulty = self.difficulty.get()
        self.high_scores[difficulty].append(result)
        self.high_scores[difficulty].sort(key=lambda x: x["wpm"], reverse=True)
        self.high_scores[difficulty] = self.high_scores[difficulty][:10]
        
        self.save_scores()

    def show_results(self, wpm, char_accuracy, word_accuracy):
        """Show the test results"""
        messagebox.showinfo(
            f"Test Complete - {self.trademark}",
            f"Your typing speed: {wpm} WPM\n"
            f"Character Accuracy: {char_accuracy:.1f}%\n"
            f"Word Accuracy: {word_accuracy:.1f}%\n"
            f"Difficulty: {self.difficulty.get().capitalize()}\n\n"
            f"{self.copyright_notice}"
        )

    def show_history(self):
        """Display test history"""
        history_window = tk.Toplevel(self.root)
        history_window.title(f"Test History - {self.trademark}")
        history_window.geometry("600x500")
        history_window.configure(bg=self.brand_colors["bg_color"])
        self.add_window_branding(history_window)
        
        if not self.history:
            tk.Label(
                history_window,
                text="No history yet! Complete some tests first.",
                font=("Helvetica", 12),
                bg=self.brand_colors["bg_color"],
                fg=self.brand_colors["fg_color"]
            ).pack(pady=50)
            return
        
        # Title
        tk.Label(
            history_window,
            text="Test History",
            font=("Helvetica", 18, "bold"),
            bg=self.brand_colors["bg_color"],
            fg=self.brand_colors["accent_color"]
        ).pack(pady=10)
        
        # Scrollable frame
        canvas = tk.Canvas(history_window, bg=self.brand_colors["bg_color"])
        scrollbar = tk.Scrollbar(history_window, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.brand_colors["bg_color"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display history in reverse order (newest first)
        for test in reversed(self.history):
            frame = tk.Frame(
                scrollable_frame,
                bg=self.brand_colors["text_bg"],
                padx=10,
                pady=10,
                relief=tk.RAISED,
                bd=1
            )
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Main info
            info_frame = tk.Frame(frame, bg=self.brand_colors["text_bg"])
            info_frame.pack(fill=tk.X)
            
            tk.Label(
                info_frame,
                text=f"{test['wpm']} WPM",
                font=("Helvetica", 14, "bold"),
                bg=self.brand_colors["text_bg"],
                fg=self.brand_colors["accent_color"]
            ).pack(side=tk.LEFT)
            
            tk.Label(
                info_frame,
                text=f"{test['char_accuracy']} Accuracy",
                font=("Helvetica", 12),
                bg=self.brand_colors["text_bg"],
                fg=self.brand_colors["fg_color"]
            ).pack(side=tk.LEFT, padx=20)
            
            # Meta info
            meta_frame = tk.Frame(frame, bg=self.brand_colors["text_bg"])
            meta_frame.pack(fill=tk.X)
            
            tk.Label(
                meta_frame,
                text=f"Difficulty: {test['difficulty'].capitalize()}",
                font=("Helvetica", 10),
                bg=self.brand_colors["text_bg"],
                fg=self.brand_colors["fg_color"]
            ).pack(side=tk.LEFT)
            
            tk.Label(
                meta_frame,
                text=f"Date: {test['date']}",
                font=("Helvetica", 10),
                bg=self.brand_colors["text_bg"],
                fg=self.brand_colors["fg_color"]
            ).pack(side=tk.RIGHT)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_high_scores(self):
        """Display high scores"""
        high_scores_window = tk.Toplevel(self.root)
        high_scores_window.title(f"High Scores - {self.trademark}")
        high_scores_window.geometry("600x500")
        high_scores_window.configure(bg=self.brand_colors["bg_color"])
        self.add_window_branding(high_scores_window)
        
        # Title
        tk.Label(
            high_scores_window,
            text="High Scores",
            font=("Helvetica", 18, "bold"),
            bg=self.brand_colors["bg_color"],
            fg=self.brand_colors["accent_color"]
        ).pack(pady=10)
        
        # Notebook for different difficulties
        notebook = ttk.Notebook(high_scores_window)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create a tab for each difficulty level
        for difficulty in ["easy", "medium", "hard"]:
            frame = tk.Frame(notebook, bg=self.brand_colors["bg_color"])
            notebook.add(frame, text=difficulty.capitalize())
            
            if not self.high_scores[difficulty]:
                tk.Label(
                    frame,
                    text=f"No high scores yet for {difficulty} level!",
                    font=("Helvetica", 12),
                    bg=self.brand_colors["bg_color"],
                    fg=self.brand_colors["fg_color"]
                ).pack(pady=50)
                continue
            
            # Create a table-like display
            headers = ["Rank", "WPM", "Accuracy", "Date"]
            for col, header in enumerate(headers):
                tk.Label(
                    frame,
                    text=header,
                    font=("Helvetica", 12, "bold"),
                    bg=self.brand_colors["bg_color"],
                    fg=self.brand_colors["accent_color"],
                    width=15
                ).grid(row=0, column=col, padx=5, pady=5)
            
            for row, score in enumerate(self.high_scores[difficulty], 1):
                tk.Label(
                    frame,
                    text=str(row),
                    font=("Helvetica", 11),
                    bg=self.brand_colors["bg_color"],
                    fg=self.brand_colors["fg_color"],
                    width=15
                ).grid(row=row, column=0, padx=5, pady=2)
                
                tk.Label(
                    frame,
                    text=str(score["wpm"]),
                    font=("Helvetica", 11),
                    bg=self.brand_colors["bg_color"],
                    fg=self.brand_colors["fg_color"],
                    width=15
                ).grid(row=row, column=1, padx=5, pady=2)
                
                tk.Label(
                    frame,
                    text=score["char_accuracy"],
                    font=("Helvetica", 11),
                    bg=self.brand_colors["bg_color"],
                    fg=self.brand_colors["fg_color"],
                    width=15
                ).grid(row=row, column=2, padx=5, pady=2)
                
                tk.Label(
                    frame,
                    text=score["date"],
                    font=("Helvetica", 11),
                    bg=self.brand_colors["bg_color"],
                    fg=self.brand_colors["fg_color"],
                    width=15
                ).grid(row=row, column=3, padx=5, pady=2)

    def export_results(self):
        """Export results to a file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")],
            title=f"Export Results - {self.trademark}"
        )
        
        if not filename:
            return
        
        if filename.endswith(".json"):
            data = {
                "history": self.history,
                "high_scores": self.high_scores,
                "metadata": {
                    "application": self.trademark,
                    "copyright": self.copyright_notice,
                    "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
            }
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
        else:
            with open(filename, "w") as f:
                f.write(f"{self.trademark} - Results Export\n")
                f.write(f"{self.copyright_notice}\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                f.write("="*50 + "\n\n")
                
                f.write("High Scores:\n")
                for difficulty in ["easy", "medium", "hard"]:
                    f.write(f"\n{difficulty.capitalize()}:\n")
                    for i, score in enumerate(self.high_scores[difficulty], 1):
                        f.write(f"{i}. {score['wpm']} WPM ({score['char_accuracy']}) on {score['date']}\n")
                
                f.write("\n\nFull History:\n")
                for test in self.history:
                    f.write(f"\n{test['wpm']} WPM ({test['char_accuracy']}) - {test['difficulty']} on {test['date']}\n")
        
        messagebox.showinfo(
            "Export Complete",
            f"Results exported to {filename}\n\n{self.copyright_notice}"
        )

    def quit_app(self):
        """Save scores and quit the application"""
        self.save_scores()
        self.root.quit()

def show_splash(root):
    """Show splash screen with copyright"""
    splash = tk.Toplevel(root)
    splash.title("Loading...")
    splash.geometry("400x200")
    splash.configure(bg="#2E3440")
    
    # Center the splash screen
    root.update_idletasks()
    width = 400
    height = 200
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    splash.geometry(f"{width}x{height}+{x}+{y}")
    
    # Splash content
    tk.Label(
        splash,
        text="Typing Speed Test Pro™",
        font=("Helvetica", 20, "bold"),
        bg="#2E3440",
        fg="#88C0D0"
    ).pack(pady=30)
    
    tk.Label(
        splash,
        text="Loading application...",
        font=("Helvetica", 12),
        bg="#2E3440",
        fg="#ECEFF4"
    ).pack()
    
    tk.Label(
        splash,
        text="© 2025 Dabeey. All Rights Reserved.",
        font=("Helvetica", 8),
        bg="#2E3440",
        fg="#D8DEE9"
    ).pack(side=tk.BOTTOM, pady=10)
    
    return splash

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main window until splash is done
    
    # Show splash screen
    splash = show_splash(root)
    root.update()
    
    # Simulate loading
    time.sleep(2)
    splash.destroy()
    
    # Show main window
    root.deiconify()
    app = TypingSpeedTestPro(root)
    
    # Center main window
    root.update_idletasks()
    width = 900
    height = 700
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()