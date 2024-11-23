import json
import random

class QuizApp:
    def __init__(self):
        self.score = 0
        self.questions = []
        self.incorrect_answer_pool = [
            "Berlin", "Madrid", "Rome", "London", "New York", "Austen", "Dickens", "Hemingway", "10", "3", "5", "Yellow"
        ]

    def load_quiz(self, filename):
        """Load the selected quiz deck from a JSON file."""
        try:
            with open(filename, 'r') as file:
                self.questions_dict = json.load(file)

            # Convert the dictionary into a list of questions
            self.questions = []
            for question, correct_answers in self.questions_dict.items():
                self.questions.append({"question": question, "answer": correct_answers[0]})

        except FileNotFoundError:
            print(f"Error: {filename} not found. Please check the file and try again.")
            return False
        return True

    def start_quiz(self):
        """Start the quiz with questions loaded from JSON and random incorrect answers."""
        random.shuffle(self.questions)  # Shuffle the question order
        self.score = 0

        for question_data in self.questions:
            self.ask_question(question_data)

        self.show_score()

    def ask_question(self, question_data):
        """Display the question and choices, then get the user's answer."""
        question = question_data['question']
        correct_answer = question_data['answer']

        # Generate a list of incorrect answers randomly picked from the pool
        incorrect_answers = random.sample(self.incorrect_answer_pool, 3)
        choices = incorrect_answers + [correct_answer]
        random.shuffle(choices)  # Shuffle the answer choices to randomize their order

        # Display the question and choices
        print(f"Question: {question}")
        for idx, choice in enumerate(choices, 1):
            print(f"{idx}. {choice}")

        user_answer = input("Your answer (enter the number corresponding to your choice): ")

        try:
            user_answer_idx = int(user_answer) - 1
            if choices[user_answer_idx] == correct_answer:
                self.score += 1
                print("Correct!\n")
            else:
                print(f"Incorrect. The correct answer was: {correct_answer}\n")
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a number corresponding to a choice.\n")

    def show_score(self):
        """Show the user's final score."""
        print(f"Your final score is: {self.score} out of {len(self.questions)}")

    def choose_deck(self):
        """Allow the user to choose the quiz deck."""
        print("Choose a quiz deck to start:")
        print("1. Start with questions.json")
        print("2. Start with sample_questions.json")

        deck_choice = input("Enter 1 or 2: ")

        if deck_choice == '1':
            if self.load_quiz('questions.json'):
                self.start_quiz()
        elif deck_choice == '2':
            if self.load_quiz('sample_questions.json'):
                self.start_quiz()
        else:
            print("Invalid choice. Please enter 1 or 2.")
            self.choose_deck()

# Main program
if __name__ == "__main__":
    app = QuizApp()
    app.choose_deck()

