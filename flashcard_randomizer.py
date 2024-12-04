import tkinter as tk
from tkinter import filedialog, messagebox
import random
import json

class FlashcardApp:
    def __init__(self, root):
        self.root = root                    
        self.root.title("Flashcards")
        self.flashcards = []
        self.current_card = {}

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Load Flashcards Button
        self.load_button = tk.Button(self.root, text="Load Flashcards", command=self.load_flashcards)
        self.load_button.pack(pady=10)

        # Question Label
        self.question_label = tk.Label(self.root, text="Load a flashcard file to begin", font=("Arial", 24))
        self.question_label.pack(pady=20)

        # Answer Label
        self.answer_label = tk.Label(self.root, text="", font=("Arial", 18), fg="blue")
        self.answer_label.pack(pady=20)

        # Reveal Answer Button
        self.reveal_button = tk.Button(self.root, text="Reveal Answer", command=self.reveal_answer, state=tk.DISABLED)
        self.reveal_button.pack(pady=10)

        # Next Question Button
        self.next_button = tk.Button(self.root, text="Next Question", command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=10)

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
            self.next_question()  # Load the first question
            self.reveal_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", f"Failed to load flashcards: {e}")

    def next_question(self):
        if not self.flashcards:
            return
        self.current_card = random.choice(self.flashcards)              #Randomize flashcards
        self.question_label.config(text=self.current_card["question"])
        self.answer_label.config(text="")  # Clear the previous answer

    def reveal_answer(self):                #Show user answer to flashcard
        if self.current_card:
            self.answer_label.config(text=f"Answer: {self.current_card['answer']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
