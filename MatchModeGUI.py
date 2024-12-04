import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import random

class MatchingMode:

    def __init__(self, questions_dict):
        self.questions_dict = questions_dict 
        self.score = 0

    def setup_matching(self, window, parent):
        questions = list(self.questions_dict.keys())
        answers = [answer[0] for answer in self.questions_dict.values()]
        self.original_answers = answers.copy()
        random.shuffle(questions)
        random.shuffle(answers)

        self.correct_answers = {question: self.questions_dict[question][0] for question in questions}

        # Clear previous widgets if any
        for widget in window.winfo_children():
            widget.destroy()

        self.user_choices = {question: tk.StringVar(window) for question in questions}

        # Frame for questions
        questions_frame = ttk.Frame(window)
        questions_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame for answers
        answers_frame = ttk.Frame(window)
        answers_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Display questions
        for idx, question in enumerate(questions, 1):
            ttk.Label(questions_frame, text=f"{idx}. {question}", wraplength=200).pack(anchor="w", padx=5, pady=5)
            ttk.OptionMenu(questions_frame, self.user_choices[question], "", *answers).pack(fill=tk.X, padx=5, pady=5)
            self.user_choices[question].set("")  # Clear the selection

        # Shuffle answers for visual variety
        random.shuffle(answers)

        # Display answers
        for idx, answer in enumerate(answers, 1):
            ttk.Label(answers_frame, text=f"{idx}. {answer}", wraplength=200).pack(anchor="w", padx=5, pady=5)

        # Submit Button
        ttk.Button(window, text="Submit Answers", command=lambda: self.check_answers(window, parent)).pack(pady=20)

    def check_answers(self, window, parent):
        for question, var in self.user_choices.items():
            selected_answer = var.get()
            if selected_answer:
                self.user_choices[question] = selected_answer

        for question, user_answer in self.user_choices.items():
            if user_answer == self.correct_answers[question]:
                self.score += 1

        messagebox.showinfo("Score", f"Your final score is: {self.score} out of {len(self.questions_dict)}")
        window.destroy()

        # Optionally, provide feedback on which answers were correct or incorrect
        self.show_feedback(parent)

    def show_feedback(self, parent):
        feedback_window = tk.Toplevel(parent)
        feedback_window.title("Feedback")
        feedback_window.geometry("600x300")

        feedback_text = tk.Text(feedback_window, wrap=tk.WORD)
        feedback_text.pack(expand=True, fill=tk.BOTH)

        for question in self.user_choices:
            feedback = f"{question}\nYour Answer: {self.user_choices[question]}\nCorrect Answer: {self.correct_answers[question]}\n"
            feedback_text.insert(tk.END, feedback)
            if self.user_choices[question] == self.correct_answers[question]:
                feedback_text.tag_add("correct", "end-1c linestart", "end-1c lineend")
                feedback_text.tag_config("correct", foreground="green")
            else:
                feedback_text.tag_add("incorrect", "end-1c linestart", "end-1c lineend")
                feedback_text.tag_config("incorrect", foreground="red")

        feedback_text.config(state=tk.DISABLED)

        # Button to close feedback window
        ttk.Button(feedback_window, text="Close", command=feedback_window.destroy).pack(pady=10)

    def check_answers(self, window, parent):
        for question, var in self.answer_vars:
            selected_answer = var.get().split('. ', 1)[1]  # Remove the number prefix
            self.user_choices[question] = selected_answer

        for question, user_answer in self.user_choices.items():
            if user_answer == self.correct_answers[question]:
                self.score += 1

        messagebox.showinfo("Score", f"Your final score is: {self.score} out of {len(self.questions_dict)}")
        window.destroy()


class StudySet:
    def __init__(self):
        self.studyset_dict = {}
        self.filename = None

    def import_study_set(self, filename):
        try:
            with open(filename, 'r') as file:
                self.studyset_dict = json.load(file)
            self.filename = filename
            return True
        except Exception:
            messagebox.showerror("Error", "Could not load the file. Check if the file exists and is a valid JSON.")
            return False

    def create_study_set(self):
        question = ""
        while True:
            question = simpledialog.askstring("Create Study Set", "Input the question (or 'exit' to finish):")
            if question and question.lower() == "exit":
                break
            if question:
                answers = []
                while True:
                    answer = simpledialog.askstring("Create Study Set", "Input an answer (or 'exit' to move to next question):")
                    if answer == "exit":
                        break
                    if answer:
                        answers.append(answer)
                if answers:
                    self.studyset_dict[question] = answers

    def edit_study_set(self):
        if not self.studyset_dict:
            messagebox.showinfo("Info", "No study set loaded or created.")
            return

        while True:
            choice = simpledialog.askstring("Edit Study Set", "Enter 'Q' to edit a question, 'A' to edit an answer, or 'exit' to stop editing:").upper()
            if choice == 'EXIT':
                break
            elif choice == 'Q':
                question = simpledialog.askstring("Edit Study Set", "Enter the question to edit:")
                if question in self.studyset_dict:
                    new_question = simpledialog.askstring("Edit Study Set", "Enter new question:")
                    self.studyset_dict[new_question] = self.studyset_dict.pop(question)
                else:
                    messagebox.showinfo("Info", "Question not found.")
            elif choice == 'A':
                question = simpledialog.askstring("Edit Study Set", "Enter the question to edit its answer:")
                if question in self.studyset_dict:
                    answers = []
                    while True:
                        answer = simpledialog.askstring("Edit Study Set", "Enter new answer (or 'exit' to finish):")
                        if answer == "exit":
                            break
                        if answer:
                            answers.append(answer)
                    if answers:
                        self.studyset_dict[question] = answers
                else:
                    messagebox.showinfo("Info", "Question not found.")

    def delete_study_set(self):
        if not self.studyset_dict:
            messagebox.showinfo("Info", "No study set loaded or created.")
            return

        while True:
            action = simpledialog.askstring("Delete", "Enter 'card' to delete a card, 'deck' to clear the deck, or 'exit' to stop:").lower()
            if action == "exit":
                break
            elif action == "card":
                question = simpledialog.askstring("Delete Card", "Enter the question of the card to delete:")
                if question in self.studyset_dict:
                    del self.studyset_dict[question]
                else:
                    messagebox.showinfo("Info", "Question not found.")
            elif action == "deck":
                self.studyset_dict.clear()
                messagebox.showinfo("Info", "Deck cleared.")
                break

        if self.filename:
            self.save_study_set()

    def save_study_set(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if self.filename:
            with open(self.filename, "w") as f:
                json.dump(self.studyset_dict, f)

class QuizApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Quiz Application")
        self.geometry("600x400")
        self.study_set = StudySet()
        self.create_widgets()

    def create_widgets(self):
        self.load_button = ttk.Button(self, text="Load Study Set", command=self.load_quiz)
        self.load_button.pack(pady=10)

        self.create_button = ttk.Button(self, text="Create New Study Set", command=self.create_study_set)
        self.create_button.pack(pady=10)

        self.edit_button = ttk.Button(self, text="Edit Study Set", command=self.edit_study_set)
        self.edit_button.pack(pady=10)

        self.delete_button = ttk.Button(self, text="Delete from Study Set", command=self.delete_study_set)
        self.delete_button.pack(pady=10)

        self.start_quiz_button = ttk.Button(self, text="Start Quiz", command=self.start_quiz)
        self.start_quiz_button.pack(pady=10)

        self.start_matching_button = ttk.Button(self, text="Start Matching Mode", command=self.start_matching)
        self.start_matching_button.pack(pady=10)

    def load_quiz(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            if self.study_set.import_study_set(filename):
                messagebox.showinfo("Success", "Quiz loaded successfully!")

    def create_study_set(self):
        self.study_set.create_study_set()
        self.study_set.save_study_set()

    def edit_study_set(self):
        self.study_set.edit_study_set()
        self.study_set.save_study_set()

    def delete_study_set(self):
        self.study_set.delete_study_set()

    def start_quiz(self):
        if not self.study_set.studyset_dict:
            messagebox.showwarning("Warning", "No study set available. Please load or create one first.")
            return

        self.quiz_window = tk.Toplevel(self)
        self.quiz_window.title("Quiz Mode")
        self.quiz_window.geometry("600x400")
        self.score = 0
        self.questions = list(self.study_set.studyset_dict.items())
        random.shuffle(self.questions)
        self.current_question_index = 0
        self.show_question()

    def show_question(self):
        if self.current_question_index < len(self.questions):
            question, correct_answer = self.questions[self.current_question_index]
            answers = [correct_answer[0]]  # Add correct answer
            all_answers = [ans for q, ans in self.study_set.studyset_dict.items() if q != question]

            # Ensure we have at least 3 options for multiple choice
            while len(answers) < 4:
                if all_answers:
                    answers.append(random.choice(all_answers)[0])
                else:
                    # If there aren't enough unique answers, just repeat some
                    answers.append(random.choice(list(self.study_set.studyset_dict.values()))[0])

            random.shuffle(answers)

            for widget in self.quiz_window.winfo_children():
                widget.destroy()

            ttk.Label(self.quiz_window, text=question, wraplength=350, justify="center").pack(pady=20)

            self.var = tk.StringVar()
            for answer in answers:
                ttk.Radiobutton(self.quiz_window, text=answer, variable=self.var, value=answer).pack(pady=5)

            ttk.Button(self.quiz_window, text="Submit", command=self.check_answer).pack(pady=20)

        else:
            self.end_quiz()

    def check_answer(self):
        question, correct_answer = self.questions[self.current_question_index]
        user_answer = self.var.get()
        
        if user_answer == correct_answer[0]:
            self.score += 1

        self.current_question_index += 1
        self.show_question()
        
    def end_quiz(self):
        messagebox.showinfo("Quiz Complete", f"Your score: {self.score}/{len(self.questions)}")
        self.quiz_window.destroy()

    def start_matching(self):
        if not self.study_set.studyset_dict:
            messagebox.showwarning("Warning", "No study set available. Please load or create one first.")
            return

        self.matching_window = tk.Toplevel(self)
        self.matching_window.title("Matching Mode")
        self.matching_window.geometry("600x400")
        self.matching_score = 0
        self.matching_mode = MatchingMode(self.study_set.studyset_dict)
        self.matching_mode.setup_matching(self.matching_window, self)

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()