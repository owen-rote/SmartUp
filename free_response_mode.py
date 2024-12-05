import random

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
            print(f"Flashcard set '{name}' already exists.")
        else:
            self.flashcard_sets[name] = FlashcardSet(name)
            print(f"Added flashcard set: {name}")

    def add_flashcard(self, set_name, word, definition):
        if set_name in self.flashcard_sets:
            self.flashcard_sets[set_name].add_flashcard(word, definition)
            print(f"Added flashcard to '{set_name}': {word} - {definition}")
        else:
            print(f"Flashcard set '{set_name}' does not exist.")

    def view_flashcard(self):
        if not self.flashcard_sets:
            print("No flashcard sets available.")
            return

        print("\nAvailable flashcard sets:")
        for name in self.flashcard_sets:
            print(f"- {name}")

        set_name = input("\nEnter the name of the flashcard set you want to view (or press Enter to go back): ").strip()
        if set_name not in self.flashcard_sets:
            if set_name == "":
                return  # Go back to the menu
            print(f"Flashcard set '{set_name}' does not exist.")
            return

        flashcards = self.flashcard_sets[set_name].flashcards
        if not flashcards:
            print(f"Flashcard set '{set_name}' is empty.")
        else:
            print(f"\nFlashcards in '{set_name}':")
            for i, flashcard in enumerate(flashcards, 1):
                print(f"{i}. Word: {flashcard.word} - Definition: {flashcard.definition}")

    def study_mode(self):
        if not self.flashcard_sets:
            print("No flashcard sets available.")
            return

        print("Available flashcard sets:")
        for name in self.flashcard_sets:
            print(f"- {name}")

        set_name = input("Enter the name of the flashcard set you want to study: ").strip()
        if set_name not in self.flashcard_sets:
            print(f"Flashcard set '{set_name}' does not exist.")
            return

        flashcards = self.flashcard_sets[set_name].flashcards
        if not flashcards:
            print(f"Flashcard set '{set_name}' is empty.")
            return

        randomize = input("Do you want to randomize the flashcards? (yes/no): ").strip().lower()
        if randomize == "yes":
            random.shuffle(flashcards)
            print("Flashcards have been randomized.")

        mode = input("Do you want to study 'words' or 'definitions'? ").strip().lower()
        if mode not in ["words", "definitions"]:
            print("Invalid choice. Please enter 'words' or 'definitions'.")
            return

        correct_count = 0
        for flashcard in flashcards:
            if mode == "words":
                print(f"Definition: {flashcard.definition}")
                answer = input("Enter the word: ").strip()
                if answer.lower() == flashcard.word.lower():
                    print("Correct!")
                    correct_count += 1
                else:
                    print(f"Incorrect! The correct word was: {flashcard.word}")
            elif mode == "definitions":
                print(f"Word: {flashcard.word}")
                answer = input("Enter the definition: ").strip()
                if answer.lower() == flashcard.definition.lower():
                    print("Correct!")
                    correct_count += 1
                else:
                    print(f"Incorrect! The correct definition was: {flashcard.definition}")

        print(f"Study session complete! You got {correct_count}/{len(flashcards)} correct.")


# Main Program
def main():
    app = SmartUp()

    while True:
        print("\nWelcome to SmartUp!")
        print("1. Add Flashcard Set")
        print("2. Add Flashcard")
        print("3. View Flashcard Sets")
        print("4. Study Flashcards")
        print("5. Quit")

        menu = input("Enter a number: ").strip()
        if menu == "1":
            name = input("Enter the name of the new flashcard set: ").strip()
            app.add_flashcard_set(name)
        elif menu == "2":
            set_name = input("Enter the name of the flashcard set: ").strip()
            word = input("Enter the word: ").strip()
            definition = input("Enter the definition: ").strip()
            app.add_flashcard(set_name, word, definition)
        elif menu == "3":
            app.view_flashcard()
        elif menu == "4":
            app.study_mode()
        elif menu == "5":
            print("Thank you for using SmartUp! Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
