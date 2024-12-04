import json
import re
from collections import OrderedDict
from datetime import datetime
import random

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

class TaskList:
    # Class to input dates and tasks or upcoming assignments 
    def __init__(self, filename):
        self.filename = filename
        self.date = str()
        self.task = str()
        self.list_dictionary = {}
        
        # Open file to load data into self.list_dictionary
        try: 
            with open(filename, 'r') as file:
                self.list_dictionary = json.load(file)
        except FileNotFoundError: # File not found exception
            pass
        
    def add_task(self):
        # Function to add tasks and date to dictionary 
        
        self.date = input("Enter date (mm/dd/yyyy): ")
        if not self.is_valid_date_format(self.date):
            return "Incorrect date format! Please try again." 
        
        self.task = input("Enter task: ")
        
        self.list_dictionary[self.date] = self.task
        
        self.save_data() # Save data to self.list_dictionary
            
    def modify_task(self):
        
        while True: 
            modify_date = input("Modify Date? (Y or N): ")
        
            if(modify_date == ('Y' or 'Yes')):
                date_to_modify = input("Date to modify: ").strip()
            
                if date_to_modify not in self.list_dictionary:
                    return 'date not in list'
            
                if date_to_modify in self.list_dictionary:
                    new_date = input("Enter new date: ")
                    self.modify_key(self.list_dictionary, date_to_modify, new_date)
                
            self.save_data()

            # decide to modify task or not 
            modify_task_response = input("Modify Task? (Y or N): ")
        
            if(modify_task_response == ('Y' or 'Yes')):
                # input date to edit in the dictionary, with key selection 
                date_to_modify = input("Date to modify: ").strip()
            
                # check if selected date is in dictionary 
                if date_to_modify not in self.list_dictionary:
                    return 'date not in list'
            
                if date_to_modify in self.list_dictionary:
                    new_task = input("Enter new task: ")
                    self.list_dictionary[date_to_modify] = new_task
               
                self.save_data()
                
                if((modify_date and modify_task_response) == 'N' or 'n'):
                break   
            
                    
    def save_data(self): # function to save data to a json file 
        with open(self.filename, 'w') as file:
            json.dump(self.list_dictionary, file)
                
            
    def delete_task(self):
        self.date = input("Task to delete (date): ")
        
        if self.date not in self.list_dictionary:
            return 'date not in list'
        
        else: 
            del self.list_dictionary[self.date]
            
            self.save_data()
                
                
    def modify_key(self, dictionary, old_key, new_key):
        if old_key not in dictionary:
            raise KeyError(f"Key '{old_key}' not found in dictionary")

        saved_value = dictionary[old_key]
        
        del dictionary[old_key]
        
        dictionary[new_key] = saved_value
        
    def print_tasks(self):
        self.list_dictionary = self.sort_by_date()
        
        for k, v in self.list_dictionary.items():
            print(f'{k:22}{v:22}') 
        
    def sort_by_date(self):
        sorted_items = sorted(self.list_dictionary.items(), key = lambda x: datetime.strptime(x[0], "%m/%d/%Y" )) 
        
        return OrderedDict(sorted_items)       
        
        
    def is_valid_date_format(self, date_str):
        
        try:
            datetime.strptime(date_str, '%m/%d/%Y')
            return True
        except ValueError:
            return False



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
