# Purpose: Contains StudySet class. This class provides functions to import/export and maintain a 
#          dictionary of questions and answers

import json

class MatchingMode:
    def __init__(self, questions_dict):
        self.questions_dict = questions_dict #this stores the original questions and answers
        self.score = 0

    def start_matching(self):
        """Start the matching mode"""
        questions = list(self.questions_dict.keys())
        answers = [answer[0] for answer in self.questions_dict.values()]

        random.shuffle(questions) #shuffle the questions
        random.shuffle(answers) #shuffle answers

        #create map for correct answers
        correct_answers = {question: self.questions[question][0] for question in questions}

        print("Match the questions with the correct answers.\n")
        user_answers = {}

        #loop throuh each question and ask the user to match
        for idx, question in enumerate(questions, 1):
            print(f"{idx}. {question}")

        print("\nChoose the correct answer from the list below (enter the number corresponding to your choice).")

        for idx, answer in enumerate(answers, 1):
            print(f"{idx}. {answer}")

        #collect the user input for matching
        for idx, question in enumerate(questions, 1):
            while True:
                try:
                    user_answer_idx = int(input(f"Your answer for Question {idx}: ")) - 1
                    if user_answer_idx < 0 or user_answer_idx >= len(answers):
                        raise ValueError
                    user_answers[question] = answers[user_answer_idx]
                    break
                except (ValueError, IndexError):
                    print("Invalid choice. Please enter a valid number.")

        #check answers and calc score
        for question, user_answer in user_answers.items():
            if user_answer == correct_answers[question]:
                self.score += 1

        self.show_score()

    def show_score(self):
        """Display the score after the matching game."""
        print(f"\nYour final score is: {self.score} out of {len(self.questions_dict)}")


class QuizApp:
    def __init__(self):
        self.score = 0
        self.questions_dict = {}  # Store the loaded questions dictionary
        self.incorrect_answer_pool = ["Berlin", "Madrid", "Rome", "London", "New York", "Austen", "Dickens", "Hemingway", "10", "3", "5", "Yellow"]

    def load_quiz(self, filename):
        """Load the selected quiz deck from a JSON file."""
        try:
            with open(filename, 'r') as file:
                self.questions_dict = json.load(file)
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

    def choose_mode(self):
        """Allow the user to choose between quiz mode and matching mode."""
        print("Choose a mode:")
        print("1. Quiz Mode")
        print("2. Matching Mode")

        mode_choice = input("Enter 1 or 2: ")

        if mode_choice == '1':
            self.start_quiz()
        elif mode_choice == '2':
            matching_mode = MatchingMode(self.questions_dict)
            matching_mode.start_matching()
        else:
            print("Invalid choice. Please enter 1 or 2.")
            self.choose_mode()

            

class StudySet:
    """Class to store and operate on a set of question and answer pairs"""

    studyset_dict = {}  # Dict for {"question" : ["answer1", "answer2", ...]} pairs

    def __init__(self) -> None:
        pass

    def importStudySet(self, filename: str) -> None:
        """Imports StudySet dictionary from an existing file and stores.

        Args:
            filename (str): Name of file to import from

        TODO:
            Add checking to ensure dictionary is proper format {str: [strs]}
        """

        # Open file, error check, load from json file into self.studyset_dict
        try:
            with open(filename, "r") as f:
                self.studyset_dict = json.load(f)
        except Exception:  # TODO: Confirm json object is in correct notation
            print("Invalid Filename.")
            return

        self.filename = filename

    def createStudySet(self, filename: str) -> None:
        """Creates studyset dictionary from scratch and saves to filename

        Args:
            filename (str): File to save studyset dict to

        TODO:
            Adapt to a UI. This only includes user text prompts for demonstration
        """
        question = str()
        current_answer = str()
        answers = list()
        question_prompt = 'Input the question or "exit" to end: '

        # ********** Loop to add questions and answers **********
        while True: #PROGRAM STARTS HERE
            question = input(question_prompt)
            if question == "exit":
                break
            while True:
                # Take answers
                current_answer = input(
                    'Input an acceptable answer. Press enter after each input. Enter "exit" to end: '
                )
                if current_answer == "exit":
                    break
                if current_answer != "":
                    answers.append(current_answer)

            if not answers:  # If no answers given, discard the question and re-loop
                continue

            self.studyset_dict[question] = answers.copy()
            answers.clear()
            question_prompt = 'Input another question or "exit" to end: '

        # Save to filename
        self.filename = filename
        try:
            with open(filename, "w") as f:
                json.dump(self.studyset_dict, f)
        except Exception:
            print("File open error.")

     def editStudySet(self, filename):
        new_answer = list()
        new_question = str()
        question_to_edit = str()
        answers = list()
        
        while True: 
            editflashcard = input("Edit flashcards (Y or N)?: ")
        
            if editflashcard == 'Y':
                edits = input("Edit question or answer (A or Q): ")
                
                if edits == 'A':
                    question_to_edit = input("Question to edit: ")
                    
                    if question_to_edit not in self.studyset_dict: 
                        print("Question not in set")
                    
                    while True: 
                        new_answer = input("Enter new answer or input (exit) to end: ")
                       
                        if new_answer == 'exit':
                            break
                    
                        if new_answer != "":
                            answers.append(new_answer)
                            
                    if question_to_edit in self.studyset_dict:
                        self.studyset_dict[question_to_edit] = answers
                        
                    
                elif edits == 'Q':
                    while True: 
                        exit_function = input("Exit or not?: ")
                        
                        if exit_function == 'no':
                            question_to_edit = input("Question to edit: ")
                            new_question = input("Enter new question: ")
                    
                            answers = self.studyset_dict[question_to_edit]
                            del self.studyset_dict[question_to_edit]
                            self.studyset_dict[new_question] = answers
                            
                        elif exit_function == "exit":
                            break
                              
                
            if editflashcard == 'N':
                return
        
            self.filename = filename
        
            with open(filename, "w") as f:
                json.dump(self.studyset_dict, f)
                
    def deleteStudySet(self, filename):
        while True: 
            response = input("Delete deck or card or exit: ")
            
            if response == "card":
                question_to_delete = input("Choose flashcard to delete by question?: ")
        
                if question_to_delete not in self.studyset_dict:
                    print("Question not in set")
                
                else:
                    del self.studyset_dict[question_to_delete]
                
            
                        
            if response == "deck":
                 self.studyset_dict.clear()
                
            if response == "exit":
                break
            
            with open(filename, "w") as f:
                json.dump(self.studyset_dict, f)
