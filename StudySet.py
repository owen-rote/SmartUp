# Purpose: Contains StudySet class. This class provides functions to import/export and maintain a 
#          dictionary of questions and answers

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

    def editStudySet(self):
        pass  # TODO
