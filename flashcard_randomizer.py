import random
import json
from tkinter import filedialog, messagebox

class FlashcardsRandomize:
    def __init__(self, root):
        self.root = root
        self.flashcards = []
        self.current_card = {}

    def load_flashcards(self):
        # Open file dialog to select a JSON file
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        # Load flashcards from the selected file
        try:
            with open(file_path, "r") as file:
                self.flashcards = json.load(file)
                if not isinstance(self.flashcards, list) or not all(
                    isinstance(card, dict) and "question" in card and "answer" in card
                    for card in self.flashcards
                ):
                    raise ValueError("Invalid JSON structure")
            messagebox.showinfo("Success", "Flashcards loaded successfully!")
            self.root.enable_buttons()  # Enable the buttons in the GUI
            self.next_question()  # Load the first question
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", f"Failed to load flashcards: {e}")

    def next_question(self):
        if not self.flashcards:
            return
        self.current_card = random.choice(self.flashcards)
        self.root.update_question(self.current_card["question"])
        self.root.clear_answer()

    def reveal_answer(self):
        if self.current_card:
            self.root.update_answer(f"Answer: {self.current_card['answer']}")
