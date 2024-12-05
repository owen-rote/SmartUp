import random
import json
from tkinter import filedialog, messagebox

class FlashcardsRandomize:
    def __init__(self, root):
        self.root = root
        self.flashcards = {}
        self.current_question = None
        self.current_answer = None

    def load_flashcards(self):
        """Loads flashcards from a JSON file where questions are keys and answers are values."""
        # Open file dialog to select a JSON file
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        # Load flashcards from the selected file
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                # Validate structure: keys as strings, values as lists of strings
                if not isinstance(data, dict) or not all(
                    isinstance(key, str) and isinstance(value, list) and all(isinstance(ans, str) for ans in value)
                    for key, value in data.items()
                ):
                    raise ValueError("Invalid JSON structure")

                self.flashcards = data
                messagebox.showinfo("Success", "Flashcards loaded successfully!")
                self.root.enable_buttons()  # Enable the buttons in the GUI
                self.next_question()  # Load the first question
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", f"Failed to load flashcards: {e}")

    def next_question(self):
        #Selects a random question and displays it.
        if not self.flashcards:
            return

        self.current_question, self.current_answer = random.choice(list(self.flashcards.items()))
        self.root.update_question(self.current_question)
        self.root.clear_answer()

    def reveal_answer(self):
        #Displays the correct answer for the current question.
        if self.current_question:
            answer_text = f"Answer: {', '.join(self.current_answer)}"
            self.root.update_answer(answer_text)
