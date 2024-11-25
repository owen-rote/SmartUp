import json 
import re
from collections import OrderedDict
from datetime import datetime

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
