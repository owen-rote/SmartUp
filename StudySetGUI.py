import json
import tkinter as tk
from tkinter import messagebox, simpledialog
import random


class StudySet:
    """Class to store and operate on a set of question and answer pairs"""

    def __init__(self) -> None:
        self.studyset_dict = {}

    def import_studyset(self, filename: str) -> None:
        """Imports StudySet dictionary from an existing file."""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                if not all(isinstance(k, str) and isinstance(v, list) for k, v in data.items()):
                    raise ValueError("Invalid format. File must contain a dictionary of {str: [strs]}.")
                self.studyset_dict = data
        except Exception as e:
            messagebox.showerror("Import Error", f"Error importing file: {e}")

    def save_studyset(self, filename: str) -> None:
        """Saves current StudySet dictionary to the given filename."""
        try:
            with open(filename, "w") as f:
                json.dump(self.studyset_dict, f)
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving file: {e}")

    def add_question(self, question: str, answers: list) -> str:
        """Adds a question and its answers to the study set."""
        if not question or not answers:
            return "Question or answers cannot be empty."
        self.studyset_dict[question] = answers
        return "Question added successfully."

    def edit_question(self, old_question: str, new_question: str, new_answers: list) -> str:
        """Edits a question and/or its answers."""
        if old_question not in self.studyset_dict:
            return "Question not found."
        del self.studyset_dict[old_question]
        self.studyset_dict[new_question] = new_answers
        return "Question edited successfully."

    def delete_question(self, question: str) -> str:
        """Deletes a question from the study set."""
        if question in self.studyset_dict:
            del self.studyset_dict[question]
            return "Question deleted successfully."
        return "Question not found."


class StudySetGUI:
    """GUI Application to manage StudySet operations."""

    def __init__(self, root, study_set: StudySet):
        self.study_set = study_set

        root.title("Study Set Manager")
        root.geometry("600x400")

        # Buttons for operations
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.import_button = tk.Button(self.frame, text="Import StudySet", command=self.import_studyset)
        self.import_button.grid(row=0, column=0, padx=5)

        self.save_button = tk.Button(self.frame, text="Save StudySet", command=self.save_studyset)
        self.save_button.grid(row=0, column=1, padx=5)

        self.add_button = tk.Button(self.frame, text="Add Question", command=self.add_question)
        self.add_button.grid(row=0, column=2, padx=5)

        self.edit_button = tk.Button(self.frame, text="Edit Question", command=self.edit_question)
        self.edit_button.grid(row=0, column=3, padx=5)

        self.delete_button = tk.Button(self.frame, text="Delete Question", command=self.delete_question)
        self.delete_button.grid(row=0, column=4, padx=5)

        self.quiz_button = tk.Button(self.frame, text="Start Quiz", command=self.start_quiz)
        self.quiz_button.grid(row=0, column=5, padx=5)

        # Listbox to display questions
        self.questions_listbox = tk.Listbox(root, width=80, height=15)
        self.questions_listbox.pack(pady=20)

        self.refresh_questions()

    def import_studyset(self):
        """Imports a StudySet from a file."""
        filename = simpledialog.askstring("Import StudySet", "Enter the filename to import:")
        if filename:
            self.study_set.import_studyset(filename)
            messagebox.showinfo("Import StudySet", "StudySet imported successfully.")
            self.refresh_questions()

    def save_studyset(self):
        """Saves the current StudySet to a file."""
        filename = simpledialog.askstring("Save StudySet", "Enter the filename to save to:")
        if filename:
            self.study_set.save_studyset(filename)
            messagebox.showinfo("Save StudySet", "StudySet saved successfully.")

    def add_question(self):
        """Adds a question to the StudySet."""
        question = simpledialog.askstring("Add Question", "Enter the question:")
        if question:
            answers = []
            while True:
                answer = simpledialog.askstring("Add Answer", "Enter an answer (or leave blank to finish):")
                if not answer:
                    break
                answers.append(answer)
            result = self.study_set.add_question(question, answers)
            messagebox.showinfo("Add Question", result)
            self.refresh_questions()

    def edit_question(self):
        """Edits an existing question and its answers."""
        old_question = self.get_selected_question()
        if not old_question:
            messagebox.showerror("Error", "No question selected.")
            return

        new_question = simpledialog.askstring("Edit Question", "Enter the new question:", initialvalue=old_question)
        if not new_question:
            new_question = old_question

        new_answers = []
        while True:
            answer = simpledialog.askstring("Edit Answer", "Enter a new answer (or leave blank to finish):")
            if not answer:
                break
            new_answers.append(answer)

        result = self.study_set.edit_question(old_question, new_question, new_answers)
        messagebox.showinfo("Edit Question", result)
        self.refresh_questions()

    def delete_question(self):
        """Deletes a selected question."""
        question = self.get_selected_question()
        if question:
            result = self.study_set.delete_question(question)
            messagebox.showinfo("Delete Question", result)
            self.refresh_questions()
        else:
            messagebox.showerror("Error", "No question selected.")

    def start_quiz(self):
        """Begins a quiz that loops through all questions."""
        if not self.study_set.studyset_dict:
            messagebox.showinfo("Quiz Mode", "The study set is empty. Add questions first.")
            return

        correct_count = 0
        total_questions = len(self.study_set.studyset_dict)
        questions = list(self.study_set.studyset_dict.items())
        random.shuffle(questions)

        for question, answers in questions:
            user_answer = simpledialog.askstring("Quiz Mode", f"Question: {question}")
            if user_answer:
                if user_answer in answers:
                    messagebox.showinfo("Quiz Mode", "Correct!")
                    correct_count += 1
                else:
                    messagebox.showinfo("Quiz Mode", f"Incorrect. Correct answers: {', '.join(answers)}")
            else:
                messagebox.showinfo("Quiz Mode", f"No answer provided. Correct answers: {', '.join(answers)}")

        messagebox.showinfo(
            "Quiz Results",
            f"Quiz complete! You answered {correct_count} out of {total_questions} questions correctly."
        )

    def refresh_questions(self):
        """Refreshes the listbox to show the current questions."""
        self.questions_listbox.delete(0, tk.END)
        for question, answers in self.study_set.studyset_dict.items():
            self.questions_listbox.insert(tk.END, f"{question}: {', '.join(answers)}")

    def get_selected_question(self):
        """Gets the currently selected question from the listbox."""
        selected = self.questions_listbox.curselection()
        if selected:
            return self.questions_listbox.get(selected[0]).split(":")[0]
        return None


if __name__ == "__main__":
    study_set = StudySet()
    root = tk.Tk()
    app = StudySetGUI(root, study_set)
    root.mainloop()
