import random
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


class Flashcard:
    def __init__(self, word, definition):
        self.word = word
        self.definition = definition


class FlashcardSet:
    def __init__(self, name):
        self.name = name
        self.flashcards = []

    def add_flashcard(self, word, definition):
        self.flashcards.append(Flashcard(word, definition))


class SmartUp:
    def __init__(self):
        self.flashcard_sets = {}

    def add_flashcard_set(self, name):
        if name in self.flashcard_sets:
            return False
        else:
            self.flashcard_sets[name] = FlashcardSet(name)
            return True

    def add_flashcard(self, set_name, word, definition):
        if set_name in self.flashcard_sets:
            self.flashcard_sets[set_name].add_flashcard(word, definition)
            return True
        else:
            return False


class SmartUpApp:
    def __init__(self, root):
        self.smartup = SmartUp()
        self.root = root
        self.root.title("SmartUp")
        self.create_main_menu()

    def create_main_menu(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        title = tk.Label(frame, text="SmartUp", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        buttons = [
            ("Add Flashcard Set", self.add_flashcard_set),
            ("Add Flashcard", self.add_flashcard),
            ("View Flashcard Sets", self.view_flashcard_sets),
            ("Study Flashcards", self.study_flashcards),
            ("Quit", self.root.quit),
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(frame, text=text, command=command, width=20).grid(row=i + 1, column=0, columnspan=2, pady=5)

    def add_flashcard_set(self):
        set_name = simpledialog.askstring("Add Flashcard Set", "Enter the name of the new flashcard set:")
        if set_name:
            if self.smartup.add_flashcard_set(set_name.strip()):
                messagebox.showinfo("Success", f"Flashcard set '{set_name}' added successfully.")
            else:
                messagebox.showerror("Error", f"Flashcard set '{set_name}' already exists.")

    def add_flashcard(self):
        set_name = simpledialog.askstring("Add Flashcard", "Enter the name of the flashcard set:")
        if set_name:
            word = simpledialog.askstring("Add Flashcard", "Enter the word:")
            definition = simpledialog.askstring("Add Flashcard", "Enter the definition:")
            if word and definition:
                if self.smartup.add_flashcard(set_name.strip(), word.strip(), definition.strip()):
                    messagebox.showinfo("Success", f"Flashcard '{word}' added to set '{set_name}'.")
                else:
                    messagebox.showerror("Error", f"Flashcard set '{set_name}' does not exist.")

    def view_flashcard_sets(self):
        if not self.smartup.flashcard_sets:
            messagebox.showinfo("Info", "No flashcard sets available.")
            return

        sets_window = tk.Toplevel(self.root)
        sets_window.title("Flashcard Sets")

        frame = tk.Frame(sets_window, padx=10, pady=10)
        frame.pack()

        label = tk.Label(frame, text="Available Flashcard Sets:", font=("Helvetica", 12, "bold"))
        label.grid(row=0, column=0, padx=5, pady=5)

        listbox = tk.Listbox(frame, width=30, height=10)
        listbox.grid(row=1, column=0, padx=5, pady=5)
        for name in self.smartup.flashcard_sets.keys():
            listbox.insert(tk.END, name)

        def show_flashcards():
            selected_set = listbox.get(tk.ACTIVE)
            if selected_set:
                flashcards = self.smartup.flashcard_sets[selected_set].flashcards
                flashcard_list = "\n".join([f"{i + 1}. {fc.word} - {fc.definition}" for i, fc in enumerate(flashcards)])
                if flashcard_list:
                    messagebox.showinfo(f"Flashcards in {selected_set}", flashcard_list)
                else:
                    messagebox.showinfo("Info", f"Flashcard set '{selected_set}' is empty.")

        view_button = tk.Button(frame, text="View Flashcards", command=show_flashcards)
        view_button.grid(row=2, column=0, pady=5)

    def study_flashcards(self):
        if not self.smartup.flashcard_sets:
            messagebox.showinfo("Info", "No flashcard sets available.")
            return

        set_name = simpledialog.askstring("Study Flashcards", "Enter the name of the flashcard set:")
        if not set_name or set_name not in self.smartup.flashcard_sets:
            messagebox.showerror("Error", "Flashcard set does not exist.")
            return

        flashcards = self.smartup.flashcard_sets[set_name].flashcards
        if not flashcards:
            messagebox.showinfo("Info", f"Flashcard set '{set_name}' is empty.")
            return

        randomize = messagebox.askyesno("Randomize", "Do you want to randomize the flashcards?")
        if randomize:
            random.shuffle(flashcards)

        mode = simpledialog.askstring("Study Mode", "Do you want to study 'words' or 'definitions'?").strip().lower()
        if mode not in ["words", "definitions"]:
            messagebox.showerror("Error", "Invalid choice. Please enter 'words' or 'definitions'.")
            return

        correct_count = 0
        for flashcard in flashcards:
            if mode == "words":
                answer = simpledialog.askstring("Study Flashcards", f"Definition: {flashcard.definition}\nEnter the word:")
                if answer and answer.strip().lower() == flashcard.word.lower():
                    correct_count += 1
            elif mode == "definitions":
                answer = simpledialog.askstring("Study Flashcards", f"Word: {flashcard.word}\nEnter the definition:")
                if answer and answer.strip().lower() == flashcard.definition.lower():
                    correct_count += 1

        messagebox.showinfo("Study Complete", f"You got {correct_count}/{len(flashcards)} correct!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartUpApp(root)
    root.mainloop()
