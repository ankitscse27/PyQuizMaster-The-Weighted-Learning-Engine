import customtkinter as ctk
from tkinter import messagebox
import random
import time
import json
import os

# --- 1. CONFIGURATION AND DATA ---
# Difficulty: GK=1 point, Science=2 points, CS=3 points
QUIZ_DATA = [
    # General Knowledge (GK) - 1 point each
    {"category": "GK", "difficulty": 1, "question": "What is the capital of Japan?", "options": ["Seoul", "Beijing", "Tokyo", "Bangkok"], "answer": "Tokyo"},
    {"category": "GK", "difficulty": 1, "question": "Who is known as the 'Iron Man of India'?", "options": ["Jawaharlal Nehru", "Sardar Patel", "B.R. Ambedkar", "Subhas Chandra Bose"], "answer": "Sardar Patel"},
    {"category": "GK", "difficulty": 1, "question": "Which continent is the largest by area?", "options": ["Africa", "Europe", "Asia", "North America"], "answer": "Asia"},
    {"category": "GK", "difficulty": 1, "question": "The famous rock 'Uluru' is located in which country?", "options": ["Australia", "Canada", "USA", "Brazil"], "answer": "Australia"},

    # Science (Physics, Chemistry, Biology) - 2 points each
    {"category": "Science", "difficulty": 2, "question": "What is the SI unit of electric current?", "options": ["Volt", "Ohm", "Ampere", "Watt"], "answer": "Ampere"},
    {"category": "Science", "difficulty": 2, "question": "Which gas is responsible for the greenhouse effect?", "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "answer": "Carbon Dioxide"},
    {"category": "Science", "difficulty": 2, "question": "The power house of the cell is called what?", "options": ["Nucleus", "Ribosome", "Mitochondria", "Cytoplasm"], "answer": "Mitochondria"},
    {"category": "Science", "difficulty": 2, "question": "What is the pH level of pure water at 25°C?", "options": ["0", "7", "14", "5"], "answer": "7"},
    {"category": "Science", "difficulty": 2, "question": "Concave mirrors are used in car headlights because they produce a...?", "options": ["Divergent beam", "Parallel beam", "Scattered beam", "Convergent beam"], "answer": "Parallel beam"},

    # Computer Science (CS) - 3 points each
    {"category": "CS", "difficulty": 3, "question": "Which of these is considered the 'brain' of the computer?", "options": ["RAM", "Monitor", "CPU", "Hard Disk"], "answer": "CPU"},
    {"category": "CS", "difficulty": 3, "question": "What does the acronym HTML stand for?", "options": ["Hyper Text Markup Language", "High-Tech Machine Learning", "Home Tool Management Link", "Hyperlink and Text Management"], "answer": "Hyper Text Markup Language"},
    {"category": "CS", "difficulty": 3, "question": "A KiloByte (KB) is equal to how many bytes?", "options": ["1000", "1024", "1048", "100"], "answer": "1024"},
    {"category": "CS", "difficulty": 3, "question": "Which company developed the Python language?", "options": ["Microsoft", "Google", "Facebook", "Centrum Wiskunde & Informatica (CWI)"], "answer": "Centrum Wiskunde & Informatica (CWI)"},
    {"category": "CS", "difficulty": 3, "question": "What is a 'bug' in computer science?", "options": ["A type of virus", "An error in a program", "A hardware component", "A coding style"], "answer": "An error in a program"},
]

ALL_CATEGORIES = list(set(q['category'] for q in QUIZ_DATA))

class Style:
    """Defines consistent styling variables for CTk."""
    MAIN_COLOR = "#3F51B5"      # Indigo (Primary Brand Color)
    ACCENT_COLOR = "#00BCD4"    # Cyan (Secondary/Accent Color)
    ERROR_COLOR = "#F44336"     # Red
    SUCCESS_COLOR = "#4CAF50"   # Green
    WARNING_COLOR = "#FFC107"   # Amber
    CATEGORY_COLORS = {
        "GK": "orange",
        "Science": "green",
        "CS": "red",
    }
    FONT_FAMILY = "Segoe UI"
    LARGE_FONT = (FONT_FAMILY, 18, "bold")
    MEDIUM_FONT = (FONT_FAMILY, 14)
    BUTTON_FONT = (FONT_FAMILY, 13, "bold")

# --- 2. MODEL/DATA PERSISTENCE ---

class QuizModel:
    """Manages the quiz data, state, scoring, and file persistence."""
    def __init__(self, file_path='quiz_results.json'):
        self.RESULTS_FILE = os.path.join(os.path.expanduser('~'), file_path)
        self.past_results = self._load_past_results()

    def _load_past_results(self):
        """Loads results from the JSON file."""
        if os.path.exists(self.RESULTS_FILE):
            try:
                with open(self.RESULTS_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_result(self, final_score, max_score, time_taken_seconds):
        """Saves the current result to the JSON file."""
        minutes = time_taken_seconds // 60
        seconds = time_taken_seconds % 60
        new_result = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "score": final_score,
            "max_score": max_score,
            "time_taken": f"{minutes:02d}m {seconds:02d}s"
        }
        self.past_results.append(new_result)
        self.past_results = self.past_results[-10:] # Keep only the last 10

        try:
            with open(self.RESULTS_FILE, 'w') as f:
                json.dump(self.past_results, f, indent=4)
        except IOError:
            messagebox.showerror("Error", f"Could not save results to {self.RESULTS_FILE}")
            
    def calculate_score(self, questions, user_answers):
        """Calculates score based on difficulty points."""
        final_score = 0
        correct_by_category = {cat: 0 for cat in ALL_CATEGORIES}
        total_by_category = {cat: 0 for cat in ALL_CATEGORIES}
        max_score = 0

        for i, q_data in enumerate(questions):
            category = q_data['category']
            difficulty = q_data['difficulty']
            total_by_category[category] += 1
            max_score += difficulty

            selected = user_answers.get(i)

            if selected == q_data['answer']:
                final_score += difficulty
                correct_by_category[category] += 1
        
        total_by_category = {k: v for k, v in total_by_category.items() if v > 0}
        
        return final_score, max_score, correct_by_category, total_by_category

# --- 3. CONTROLLER/MAIN APPLICATION ---

class QuizApp(ctk.CTk):
    
    # 🌟 NEW: Add GitHub Name Here
    GITHUB_AUTHOR = "ankitscse27" 

    def __init__(self):
        super().__init__()
        
        # 🌟 NEW: Include GitHub name in the window title
        self.title(f"🧠 Hybrid Advanced Quiz Pro | Creator: @{self.GITHUB_AUTHOR}")
        
        self.geometry("800x850")
        self.resizable(True, True)
        
        # Explicitly set light appearance for a better light interface
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Configuration (Defaults)
        self.config_total_questions = 10 if len(QUIZ_DATA) > 10 else len(QUIZ_DATA)
        self.config_categories = ALL_CATEGORIES

        # Model and State
        self.model = QuizModel()
        self.questions = []
        self.total_questions = 0
        self.current_question_index = 0
        self.user_answers = {}
        self.is_running = False
        self.start_time = 0
        self.time_elapsed = 0
        self._timer_job = None
        self.selected_option = ctk.StringVar()
        
        self.reset_button = None # Initialize reference

        # UI Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_header_frame()
        self._create_main_container()
        self._create_footer_frame()
        self._setup_keyboard_bindings()

        self._show_settings_window()

    # --- UI CREATION ---

    def _create_header_frame(self):
        """Creates the fixed header (score, timer, progress bar, menu)."""
        self.header_frame = ctk.CTkFrame(self, height=100, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="new", padx=20, pady=(20, 10))
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=0)

        self.score_label = ctk.CTkLabel(self.header_frame, text="Score: 0 Points", font=Style.MEDIUM_FONT, text_color=Style.MAIN_COLOR)
        self.score_label.grid(row=0, column=0, sticky='w', padx=20, pady=(10, 5))

        self.timer_label = ctk.CTkLabel(self.header_frame, text="Time: 00m 00s", font=Style.MEDIUM_FONT, text_color=Style.MAIN_COLOR)
        self.timer_label.grid(row=0, column=1, sticky='e', padx=20, pady=(10, 5))

        self.progress_bar = ctk.CTkProgressBar(self.header_frame, orientation="horizontal", height=15, corner_radius=10, fg_color=Style.MAIN_COLOR, progress_color=Style.ACCENT_COLOR)
        self.progress_bar.grid(row=1, column=0, columnspan=3, sticky='ew', padx=20, pady=(0, 10))
        self.progress_bar.set(0)

        self.settings_button = ctk.CTkButton(self.header_frame, text="⚙️", width=40, command=self._show_settings_window, fg_color="transparent", hover_color=Style.ACCENT_COLOR, text_color=Style.MAIN_COLOR)
        self.settings_button.grid(row=0, column=2, sticky='e', padx=10, pady=(10, 5))

    def _create_main_container(self):
        """Creates the main scrollable frame for questions."""
        self.main_container = ctk.CTkScrollableFrame(self, label_text="Question Area", label_font=Style.MEDIUM_FONT, corner_radius=10)
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.category_label = ctk.CTkLabel(self.main_container, text="", font=Style.MEDIUM_FONT, corner_radius=6, padx=10, pady=5)
        self.category_label.grid(row=0, column=0, pady=(0, 20), sticky='nw')

        self.q_num_label = ctk.CTkLabel(self.main_container, text="", font=Style.MEDIUM_FONT, anchor='w')
        self.q_num_label.grid(row=1, column=0, sticky='ew', pady=(0, 10))

        self.q_text_label = ctk.CTkLabel(self.main_container, text="Welcome! Use the settings button (⚙️) to configure and start your quiz.", font=Style.LARGE_FONT, wraplength=700, anchor='w', justify="left")
        self.q_text_label.grid(row=2, column=0, sticky='ew', pady=(10, 30))

        self.options_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.options_frame.grid(row=3, column=0, sticky='ew', pady=(10, 20))
        self.options_frame.grid_columnconfigure(0, weight=1)

    def _create_footer_frame(self):
        """Creates the fixed footer for navigation and feedback."""
        self.footer_frame = ctk.CTkFrame(self, height=50, corner_radius=0)
        self.footer_frame.grid(row=2, column=0, sticky="sew", padx=20, pady=(0, 20))
        self.footer_frame.grid_columnconfigure(0, weight=1)
        self.footer_frame.grid_columnconfigure(1, weight=0)
        self.footer_frame.grid_columnconfigure(2, weight=0)

        self.feedback_label = ctk.CTkLabel(self.footer_frame, text="", font=Style.MEDIUM_FONT)
        self.feedback_label.grid(row=0, column=0, sticky='w', padx=20)

        self.review_button = ctk.CTkButton(self.footer_frame, text="Review", command=self._create_review_window, font=Style.BUTTON_FONT, fg_color=Style.ACCENT_COLOR, hover_color=Style.MAIN_COLOR)
        self.review_button.grid(row=0, column=1, sticky='e', padx=(0, 10), pady=10)

        self.next_button = ctk.CTkButton(self.footer_frame, text="Next (Enter)", command=self._check_and_save_answer_and_finish, font=Style.BUTTON_FONT, fg_color=Style.MAIN_COLOR)
        self.next_button.grid(row=0, column=2, sticky='e', padx=20, pady=10)
        
        self.review_button.grid_remove()
        self.next_button.grid_remove()
        
        self.reset_button = ctk.CTkButton(self.footer_frame, text="START NEW QUIZ", command=self._show_settings_window, font=Style.BUTTON_FONT,
                                      fg_color=Style.SUCCESS_COLOR, hover_color=Style.MAIN_COLOR)

    def _setup_keyboard_bindings(self):
        """Sets up key bindings for faster interaction."""
        for i in range(1, 5):
            self.bind(str(i), lambda event, opt=i: self._select_option_via_key(opt))
        self.bind('<Return>', lambda event: self._check_and_save_answer_and_finish())

    # --- SETTINGS AND INITIALIZATION ---

    def _show_settings_window(self):
        """Opens a modal window for quiz configuration."""
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Quiz Settings")
        settings_window.geometry("450x450")
        settings_window.transient(self)
        settings_window.grab_set()

        frame = ctk.CTkFrame(settings_window)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # 1. Total Questions Slider
        ctk.CTkLabel(frame, text="Number of Questions:", font=Style.MEDIUM_FONT).pack(pady=(10, 5))
        
        max_q = len(QUIZ_DATA)
        self.q_slider_label = ctk.CTkLabel(frame, text=f"{self.config_total_questions} / {max_q}", text_color=Style.MAIN_COLOR)
        self.q_slider_label.pack(pady=5)
        
        q_slider = ctk.CTkSlider(frame, from_=5, to=max_q, number_of_steps=(max_q - 5), 
                                 command=lambda val: self.q_slider_label.configure(text=f"{int(val)} / {max_q}"))
        q_slider.set(self.config_total_questions)
        q_slider.pack(pady=5, padx=20, fill='x')

        # 2. Category Filter (Checkboxes)
        ctk.CTkLabel(frame, text="Select Categories:", font=Style.MEDIUM_FONT).pack(pady=(20, 5))
        
        cat_vars = {}
        for cat in ALL_CATEGORIES:
            var = ctk.BooleanVar(value=cat in self.config_categories)
            cat_vars[cat] = var
            ctk.CTkCheckBox(frame, text=cat, variable=var, fg_color=Style.CATEGORY_COLORS[cat], hover_color=Style.MAIN_COLOR, text_color=("black", "white")).pack(anchor='w', padx=20, pady=3)

        def apply_settings():
            self.config_total_questions = int(q_slider.get())
            self.config_categories = [cat for cat, var in cat_vars.items() if var.get()]
            
            if not self.config_categories:
                messagebox.showerror("Error", "Please select at least one category.")
                return

            settings_window.destroy()
            self._filter_and_start_quiz()

        ctk.CTkButton(frame, text="Start Quiz with Settings", command=apply_settings, font=Style.BUTTON_FONT, fg_color=Style.SUCCESS_COLOR).pack(pady=30)
        
        settings_window.protocol("WM_DELETE_WINDOW", settings_window.destroy)

    def _filter_and_start_quiz(self):
        """Filters questions based on settings and resets quiz state."""
        filtered_questions = [
            q for q in QUIZ_DATA 
            if q['category'] in self.config_categories
        ]
        
        if len(filtered_questions) < self.config_total_questions:
            self.config_total_questions = len(filtered_questions)
        
        random.shuffle(filtered_questions)
        self.questions = filtered_questions[:self.config_total_questions]
        self.total_questions = len(self.questions)

        # Reset state and start
        if self._timer_job is not None:
            self.after_cancel(self._timer_job)
        
        self.current_question_index = 0
        self.user_answers = {}
        self.is_running = True
        self.start_time = time.time()
        self.time_elapsed = 0
        
        self.progress_bar.set(0)

        self.review_button.grid()
        self.next_button.grid()
        
        self.reset_button.grid_remove()

        self._load_question()
        self._update_timer()

    # --- CORE QUIZ LOGIC AND UX ---

    def _update_timer(self):
        """Updates the timer label every second."""
        if self.is_running:
            self.time_elapsed = int(time.time() - self.start_time)
            minutes = self.time_elapsed // 60
            seconds = self.time_elapsed % 60
            self.timer_label.configure(text=f"Time: {minutes:02d}m {seconds:02d}s")
            self._timer_job = self.after(1000, self._update_timer)
        elif self._timer_job is not None:
             self.after_cancel(self._timer_job)

    def _load_question(self):
        """Loads the current question's data into the UI."""
        if self.current_question_index >= self.total_questions:
            self._show_results()
            return

        q_data = self.questions[self.current_question_index]
        current_answer = self.user_answers.get(self.current_question_index, "")
        self.selected_option.set(current_answer)

        self.q_num_label.configure(text=f"Question {self.current_question_index + 1} of {self.total_questions}: ({q_data['difficulty']} points)")
        self.q_text_label.configure(text=q_data["question"])
        
        # Progress is calculated as a float between 0 and 1
        progress_value = self.current_question_index / self.total_questions if self.total_questions > 0 else 0
        self.progress_bar.set(progress_value)
        
        self.feedback_label.configure(text="")

        category = q_data['category']
        cat_color = Style.CATEGORY_COLORS.get(category, "blue")
        self.category_label.configure(text=f"CATEGORY: {category.upper()}", fg_color=cat_color, text_color="white")

        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.option_wrappers = {}

        for i, option in enumerate(q_data["options"]):
            option_label = f"({i+1}) {option}"
            
            rb = ctk.CTkRadioButton(self.options_frame, text=option_label, variable=self.selected_option,
                                 value=option, font=Style.MEDIUM_FONT, command=self._update_selection_visuals,
                                 border_color=Style.MAIN_COLOR, border_width_checked=5, border_width_unchecked=2,
                                 radiobutton_height=20, radiobutton_width=20, corner_radius=10, hover_color=Style.ACCENT_COLOR,
                                 text_color=("black", "white"))
            rb.grid(row=i, column=0, sticky='ew', pady=8, padx=10)
            self.option_wrappers[option] = rb

        self._update_selection_visuals(initial_load=True)
        self._update_score_display()

        is_last_q = self.current_question_index == self.total_questions - 1
        if is_last_q:
            self.next_button.configure(text="Submit & View Results (Enter)", fg_color=Style.ERROR_COLOR)
        else:
            self.next_button.configure(text="Next Question (Enter)", fg_color=Style.MAIN_COLOR)

    def _update_selection_visuals(self, initial_load=False):
        """Highlights the currently selected option in real-time."""
        selected_value = self.selected_option.get()
        for option, rb in self.option_wrappers.items():
            if option == selected_value:
                rb.configure(text_color=Style.MAIN_COLOR, hover_color=Style.MAIN_COLOR)
            else:
                rb.configure(text_color=("black", "white"), hover_color=Style.ACCENT_COLOR)
        
        if not initial_load and selected_value:
             self.user_answers[self.current_question_index] = selected_value
             self._update_score_display()

    def _check_and_save_answer_and_finish(self):
        """Processes the answer, gives feedback, and moves on."""
        if not self.is_running: return

        current_q_index = self.current_question_index
        q_data = self.questions[current_q_index]
        selected = self.selected_option.get()
        
        self.user_answers[current_q_index] = selected
        
        is_last_q = current_q_index == self.total_questions - 1
        if not selected and not is_last_q:
            if not messagebox.askyesno("Confirm Skip", "You have not selected an option. Skip this question?"):
                return

        self.next_button.configure(state="disabled")
        self.review_button.configure(state="disabled")
        for rb in self.option_wrappers.values():
            rb.configure(state="disabled")

        if selected == q_data['answer']:
            feedback_text = f"✅ Correct! Earned {q_data['difficulty']} points."
            feedback_color = Style.SUCCESS_COLOR
        elif selected and selected != "":
            feedback_text = f"❌ Incorrect. Correct was: {q_data['answer']}."
            feedback_color = Style.ERROR_COLOR
        else:
            feedback_text = "⚠️ Question Skipped."
            feedback_color = Style.WARNING_COLOR

        self.feedback_label.configure(text=feedback_text, text_color=feedback_color)

        for option_value, rb in self.option_wrappers.items():
            if option_value == q_data['answer']:
                rb.configure(border_color=Style.SUCCESS_COLOR, text_color=Style.SUCCESS_COLOR)
            elif option_value == selected and selected != q_data['answer']:
                rb.configure(border_color=Style.ERROR_COLOR, text_color=Style.ERROR_COLOR)
            else:
                 rb.configure(text_color=("black", "white"), border_color="gray")

        self.after(1500, self._proceed_to_next)
    
    def _proceed_to_next(self):
        """Proceeds to the next question after visual feedback delay."""
        self.current_question_index += 1

        self.next_button.configure(state="normal")
        self.review_button.configure(state="normal")

        if self.current_question_index < self.total_questions:
            self._load_question()
        else:
            self._show_results()
            
    # --- RESULT AND REVIEW WINDOWS (Logic remains robust) ---

    def _update_score_display(self):
        """Calculates and updates the displayed score."""
        current_score, max_score, _, _ = self.model.calculate_score(self.questions, self.user_answers)
        self.score_label.configure(text=f"Score: {current_score} / {max_score} Points")

    def _show_results(self):
        """Calculates final score, saves, and displays detailed results."""
        if not self.is_running: return

        self.is_running = False
        self._update_timer()

        final_score, max_score, correct_by_category, total_by_category = self.model.calculate_score(self.questions, self.user_answers)

        self.model.save_result(final_score, max_score, self.time_elapsed)
        self.model.past_results = self.model._load_past_results()

        self.next_button.grid_remove()
        self.review_button.grid_remove()
        self.feedback_label.configure(text="")

        for widget in self.options_frame.winfo_children():
            widget.destroy()

        self.q_text_label.configure(text=f"Quiz Complete! Your Final Score: {final_score}/{max_score} Points")
        self.q_num_label.configure(text="Summary:")
        self.category_label.configure(text="RESULTS", fg_color=Style.ACCENT_COLOR, text_color="white")
        self.progress_bar.set(1.0)
        
        self._create_results_window(final_score, max_score, self.time_elapsed, correct_by_category, total_by_category)


    def _create_results_window(self, final_score, max_score, time_elapsed, correct_by_category, total_by_category):
        """Creates the detailed results window."""
        results_window = ctk.CTkToplevel(self)
        results_window.title("Detailed Quiz Results")
        results_window.geometry("700x750")
        results_window.focus_set()
        results_window.transient(self)
        results_window.grab_set()

        scroll_container = ctk.CTkScrollableFrame(results_window, label_text="Results Analysis", label_font=Style.LARGE_FONT)
        scroll_container.pack(fill='both', expand=True, padx=20, pady=20)
        scroll_container.grid_columnconfigure(0, weight=1)

        minutes = time_elapsed // 60
        seconds = time_elapsed % 60
        score_color = Style.SUCCESS_COLOR if final_score > max_score * 0.7 else Style.ERROR_COLOR

        ctk.CTkLabel(scroll_container, text=f"Total Score: {final_score} / {max_score} Points", font=(Style.FONT_FAMILY, 20, "bold"), text_color=score_color).pack(pady=(10, 5), fill='x')
        ctk.CTkLabel(scroll_container, text=f"Time Taken: {minutes:02d}m {seconds:02d}s", font=Style.MEDIUM_FONT).pack(pady=(0, 20), fill='x')

        ctk.CTkLabel(scroll_container, text="Category Breakdown", font=Style.LARGE_FONT).pack(pady=(10, 5), fill='x')

        for category in ALL_CATEGORIES:
            total = total_by_category.get(category, 0)
            correct = correct_by_category.get(category, 0)
            if total > 0:
                cat_color = Style.CATEGORY_COLORS.get(category, "blue")
                ctk.CTkLabel(scroll_container, text=f"• {category}: {correct} / {total} Correct", font=Style.MEDIUM_FONT, text_color=cat_color).pack(anchor='w', padx=10, pady=2)

        incorrect_questions = [
            {"number": i + 1, "q": q, "ans": self.user_answers.get(i)}
            for i, q in enumerate(self.questions)
            if self.user_answers.get(i) != q['answer']
        ]

        if incorrect_questions:
            ctk.CTkLabel(scroll_container, text="\nMistakes Review", font=Style.LARGE_FONT, text_color=Style.ERROR_COLOR).pack(pady=(20, 5), fill='x')

            for item in incorrect_questions:
                review_frame = ctk.CTkFrame(scroll_container, fg_color=("gray90", "gray20"), corner_radius=10)
                review_frame.pack(fill='x', padx=10, pady=5)
                
                q_text = f"Q{item['number']} ({item['q']['category']} - {item['q']['difficulty']}pts): {item['q']['question']}"
                ctk.CTkLabel(review_frame, text=q_text, font=Style.MEDIUM_FONT, justify="left", wraplength=600).pack(fill='x', padx=10, pady=(5, 0))

                ctk.CTkLabel(review_frame, text=f"Your Answer: {item['ans'] if item['ans'] else 'N/A (Skipped)'}", font=Style.MEDIUM_FONT, text_color=Style.ERROR_COLOR, anchor='w').pack(fill='x', padx=10)

                ctk.CTkLabel(review_frame, text=f"Correct Answer: {item['q']['answer']}", font=Style.MEDIUM_FONT, text_color=Style.SUCCESS_COLOR, anchor='w').pack(fill='x', padx=10, pady=(0, 5))

        ctk.CTkLabel(scroll_container, text="\nPast Results (Last 10)", font=Style.LARGE_FONT, text_color=Style.MAIN_COLOR).pack(pady=(20, 5), fill='x')

        for result in reversed(self.model.past_results):
            score_ratio = f"{result['score']}/{result['max_score']}"
            ctk.CTkLabel(scroll_container, text=f"Date: {result['timestamp']} | Score: {score_ratio} | Time: {result['time_taken']}", font=Style.MEDIUM_FONT).pack(anchor='w', padx=10, pady=2)
            
        # 🌟 NEW: Display GitHub name at the bottom of the results window
        ctk.CTkLabel(scroll_container, text=f"\nApplication Creator: @{self.GITHUB_AUTHOR}", font=Style.MEDIUM_FONT, text_color="gray").pack(pady=(20, 5), fill='x')

        self.reset_button.configure(command=lambda: [results_window.destroy(), self._show_settings_window()])
        self.reset_button.grid(row=0, column=0, columnspan=3, sticky='n', padx=20, pady=10)

        results_window.protocol("WM_DELETE_WINDOW", lambda: self.reset_button.grid(row=0, column=0, columnspan=3, sticky='n', padx=20, pady=10))


    def _create_review_window(self):
        """Creates a modal window for reviewing all question statuses and jumping."""
        review_window = ctk.CTkToplevel(self)
        review_window.title("Quiz Review & Navigation")
        review_window.geometry("500x550")
        review_window.focus_set()
        review_window.transient(self)
        review_window.grab_set()

        main_frame = ctk.CTkScrollableFrame(review_window, label_text="Question Status", label_font=Style.MEDIUM_FONT)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        
        for i, q_data in enumerate(self.questions):
            q_num = i + 1
            selected = self.user_answers.get(i, "")
            is_answered = selected != ""
            is_current = i == self.current_question_index

            if is_current:
                bg_color = Style.MAIN_COLOR
                fg_color = "white"
                status_text = "➡ CURRENT"
            elif is_answered:
                bg_color = Style.SUCCESS_COLOR
                fg_color = "white"
                status_text = "✅ ANSWERED"
            else:
                bg_color = "gray"
                fg_color = "black"
                status_text = "❓ UNANSWERED"

            q_button = ctk.CTkButton(main_frame,
                                 text=f"Q{q_num} | {q_data['category']} ({q_data['difficulty']} pts) | {status_text}",
                                 command=lambda index=i, win=review_window: self.jump_to_question(index, win),
                                 font=(Style.FONT_FAMILY, 11, "bold"),
                                 fg_color=bg_color,
                                 text_color=fg_color,
                                 hover_color=Style.ACCENT_COLOR if not is_current else Style.MAIN_COLOR,
                                 corner_radius=8,
                                 anchor='w')
            q_button.grid(row=i, column=0, sticky='ew', padx=5, pady=3)
            
        ctk.CTkButton(review_window, text="Close", command=review_window.destroy, font=Style.BUTTON_FONT, fg_color=Style.ERROR_COLOR).pack(pady=10)


    def jump_to_question(self, index, review_window):
        """Jumps the quiz to the specified question index from the review window."""
        review_window.destroy()
        if 0 <= index < self.total_questions:
            self.current_question_index = index
            self._load_question()
            
    def _select_option_via_key(self, option_index):
        """Selects the option corresponding to the key pressed."""
        if not self.is_running or self.current_question_index >= self.total_questions:
            return

        q_data = self.questions[self.current_question_index]
        if 0 <= option_index - 1 < len(q_data['options']):
            selected_value = q_data['options'][option_index - 1]
            self.selected_option.set(selected_value)
            self._update_selection_visuals()

# --- 4. APPLICATION STARTUP ---
if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()