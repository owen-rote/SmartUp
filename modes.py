import json


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
