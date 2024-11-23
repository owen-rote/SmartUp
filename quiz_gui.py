import tkinter as tk
from tkinter import messagebox
import json
import random
import os
from tkinter import ttk  # Import ttk for styled widgets

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Application")

        self.score = 0
        self.questions = []
        self.selected_answers = []  # Keep track of selected answers
        self.incorrect_answer_pool = [
            "Berlin", "Madrid", "Rome", "London", "New York", "Austen", "Dickens", "Hemingway", "10", "3", "5", "Yellow"
        ]

        # UI Elements
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.main_frame, text="Welcome to the Quiz Application!", font=("Arial", 16))
        self.title_label.pack()

        self.choose_deck_button = tk.Button(self.main_frame, text="Choose Quiz Deck", command=self.choose_deck)
        self.choose_deck_button.pack(pady=10)

        self.back_button = tk.Button(self.main_frame, text="Back", state=tk.DISABLED, command=self.go_back)
        self.back_button.pack(pady=10)

        self.deck_buttons = []  # Track dynamically created deck buttons

        # Create and configure the custom scrollbar style
        self.style = ttk.Style()
        self.style.configure("Custom.Vertical.TScrollbar", 
                             gripcount=0, 
                             thickness=8, 
                             background="#888888", 
                             troughcolor="#f0f0f0", 
                             arrowcolor="#666666", 
                             sliderlength=40)

    def choose_deck(self):
        """Scan directory for JSON files and show them to the user for selection."""
        json_files = [f for f in os.listdir() if f.endswith(".json")]

        if not json_files:
            messagebox.showerror("Error", "No JSON files found in the current directory.")
            return

        # Clear current content
        self.clear_frame()

        self.title_label = tk.Label(self.main_frame, text="Select a quiz deck:", font=("Arial", 14))
        self.title_label.pack(pady=10)

        # List all JSON files as buttons
        for deck in json_files:
            button = tk.Button(self.main_frame, text=deck, width=30, command=lambda f=deck: self.load_quiz(f))
            button.pack(pady=5)
            self.deck_buttons.append(button)

    def load_quiz(self, deck_name):
        """Load the chosen quiz deck from a JSON file."""
        if os.path.isfile(deck_name):
            with open(deck_name, 'r') as file:
                try:
                    self.questions_dict = json.load(file)

                    # Convert dictionary into list of questions
                    self.questions = []
                    for question, correct_answers in self.questions_dict.items():
                        self.questions.append({"question": question, "answer": correct_answers[0]})

                    # Enable the back button after deck is loaded
                    self.back_button.config(state=tk.NORMAL)

                    # Disable deck selection UI
                    self.title_label.config(state=tk.DISABLED)
                    for widget in self.main_frame.winfo_children():
                        if isinstance(widget, tk.Button) and widget not in self.deck_buttons:
                            widget.config(state=tk.DISABLED)

                    # After loading, show the quiz options
                    self.show_quiz_options()

                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Invalid JSON format in the file.")
                    return
        else:
            messagebox.showerror("Error", f"File '{deck_name}' not found. Please try again.")
            return

    def show_quiz_options(self):
        """Enable quiz options (submit and back buttons) after deck is loaded."""
        self.selected_answers = [None] * len(self.questions)  # Initialize list based on the number of questions

        # Clear current screen content
        self.clear_frame()

        # Create a frame for the quiz content and scrollbar
        quiz_frame = tk.Frame(self.main_frame)
        quiz_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Create a canvas for scrolling
        self.canvas = tk.Canvas(quiz_frame)
        self.canvas.pack(side=tk.LEFT, pady=5, fill=tk.BOTH, expand=True)

        # Create the custom scrollbar
        self.scrollbar = ttk.Scrollbar(quiz_frame, orient="vertical", command=self.canvas.yview, style="Custom.Vertical.TScrollbar")
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Create a frame within the canvas that will hold the question content
        self.question_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.question_frame, anchor="nw")

        # Add each question with its answer choices
        for idx, question_data in enumerate(self.questions):
            question = question_data['question']
            correct_answer = question_data['answer']

            # Create label for question inside the scrollable frame
            question_label = tk.Label(self.question_frame, text=f"Q{idx + 1}: {question}", font=("Arial", 12), width=50)
            question_label.pack(pady=5)

            # Create list of answer choices (correct answer and random wrong ones)
            choices = [correct_answer] + random.sample(self.incorrect_answer_pool, 3)
            random.shuffle(choices)

            # Add answer choices with dots and labels
            self.create_answer_choices(idx, choices)

        # Add the Submit button after all questions
        self.submit_button = tk.Button(self.question_frame, text="Submit", command=self.submit_quiz)
        self.submit_button.pack(pady=10)

        # Update scroll region after adding all items
        self.question_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_answer_choices(self, idx, choices):
        """Create a dot and answer text for each choice."""
        # Create a frame for this set of answer choices
        answer_frame = tk.Frame(self.question_frame)
        answer_frame.pack(pady=5, anchor='w')

        # Create a list of answer choices with dots
        for choice in choices:
            # Create a frame for this answer choice
            choice_frame = tk.Frame(answer_frame)
            choice_frame.pack(side=tk.LEFT, padx=10)

            # Create the dot (circle) for this answer choice
            answer_canvas = tk.Canvas(choice_frame, width=20, height=20)
            answer_canvas.create_oval(5, 5, 15, 15, outline="black", width=2)
            answer_canvas.pack(side=tk.LEFT, padx=5)

            # Create a label for the answer text
            answer_label = tk.Label(choice_frame, text=choice, font=("Arial", 10))
            answer_label.pack(side=tk.LEFT, padx=5)

            # Store each canvas and its corresponding answer
            answer_canvas.choice = choice  # Attach the answer to the canvas

            # Bind the dot (circle) to the selection action
            answer_canvas.bind("<Button-1>", lambda event, canvas=answer_canvas, idx=idx: self.select_answer(canvas, idx))

    def select_answer(self, canvas, idx):
        """Highlight the selected dot and store the answer."""
        selected_answer = canvas.choice

        # Color the selected dot
        canvas.create_oval(5, 5, 15, 15, fill="lightblue", outline="black", width=2)

        # Store the selected answer
        self.selected_answers[idx] = selected_answer

        # Reset other dots to default (uncolored)
        for child in self.question_frame.winfo_children():
            if isinstance(child, tk.Frame):
                for canvas in child.winfo_children():
                    if isinstance(canvas, tk.Canvas) and canvas != event.widget:
                        canvas.create_oval(5, 5, 15, 15, outline="black", width=2)  # Reset circle color

    def submit_quiz(self):
        """Grade the quiz and show results."""
        correct_count = 0

        for idx, selected_answer in enumerate(self.selected_answers):
            correct_answer = self.questions[idx]['answer']
            if selected_answer == correct_answer:
                correct_count += 1
            else:
                messagebox.showinfo("Incorrect", f"Q{idx + 1}: Correct answer was '{correct_answer}'")

        # Show final score
        messagebox.showinfo("Quiz Finished", f"You scored {correct_count} out of {len(self.questions)}")

        # Optionally, restart the quiz
        self.restart_quiz()

    def restart_quiz(self):
        """Restart the quiz process."""
        self.score = 0
        self.selected_answers = []

        # Reset UI for deck selection
        self.clear_frame()
        self.title_label = tk.Label(self.main_frame, text="Welcome to the Quiz Application!", font=("Arial", 16))
        self.title_label.pack()

        self.choose_deck_button = tk.Button(self.main_frame, text="Choose Quiz Deck", command=self.choose_deck)
        self.choose_deck_button.pack(pady=10)

    def go_back(self):
        """Go back to the deck selection screen."""
        self.restart_quiz()

    def clear_frame(self):
        """Clear the current screen content."""
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

