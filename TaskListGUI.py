# This is AI generated based on tasklist.py and just for testing

import json
import re
from collections import OrderedDict
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog


class TaskList:
    def __init__(self, filename):
        self.filename = filename
        self.list_dictionary = {}

        try:
            with open(filename, "r") as file:
                self.list_dictionary = json.load(file)
        except FileNotFoundError:
            pass

    def add_task(self, date, task):
        if not self.is_valid_date_format(date):
            return "Incorrect date format!"

        self.list_dictionary[date] = task
        self.save_data()
        return "Task added successfully!"

    def modify_task(self, old_date, new_date=None, new_task=None):
        if old_date not in self.list_dictionary:
            return "Date not in list"

        if new_date:
            self.modify_key(self.list_dictionary, old_date, new_date)
            old_date = new_date

        if new_task:
            self.list_dictionary[old_date] = new_task

        self.save_data()
        return "Task modified successfully!"

    def delete_task(self, date):
        if date not in self.list_dictionary:
            return "Date not in list"

        del self.list_dictionary[date]
        self.save_data()
        return "Task deleted successfully!"

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.list_dictionary, file)

    def modify_key(self, dictionary, old_key, new_key):
        if old_key not in dictionary:
            raise KeyError(f"Key '{old_key}' not found in dictionary")

        saved_value = dictionary[old_key]
        del dictionary[old_key]
        dictionary[new_key] = saved_value

    def sort_by_date(self):
        sorted_items = sorted(
            self.list_dictionary.items(),
            key=lambda x: datetime.strptime(x[0], "%m/%d/%Y"),
        )
        return OrderedDict(sorted_items)

    def is_valid_date_format(self, date_str):
        try:
            datetime.strptime(date_str, "%m/%d/%Y")
            return True
        except ValueError:
            return False


class TaskListGUI:
    def __init__(self, root, task_list):
        self.task_list = task_list

        root.title("Task Manager")
        root.geometry("500x400")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=5)

        self.modify_button = tk.Button(
            self.frame, text="Modify Task", command=self.modify_task
        )
        self.modify_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(
            self.frame, text="Delete Task", command=self.delete_task
        )
        self.delete_button.grid(row=0, column=2, padx=5)

        self.refresh_button = tk.Button(
            self.frame, text="Refresh Tasks", command=self.refresh_task_list
        )
        self.refresh_button.grid(row=0, column=3, padx=5)

        self.task_list_box = tk.Listbox(root, width=50, height=15)
        self.task_list_box.pack(pady=20)

        self.refresh_task_list()

    def add_task(self):
        date = simpledialog.askstring("Input", "Enter date (mm/dd/yyyy):")
        task = simpledialog.askstring("Input", "Enter task:")
        if date and task:
            result = self.task_list.add_task(date, task)
            messagebox.showinfo("Add Task", result)
            self.refresh_task_list()

    def modify_task(self):
        old_date = simpledialog.askstring(
            "Input", "Enter date of task to modify (mm/dd/yyyy):"
        )
        if old_date and old_date in self.task_list.list_dictionary:
            new_date = simpledialog.askstring(
                "Input", "Enter new date (leave blank to keep current):"
            )
            new_task = simpledialog.askstring(
                "Input", "Enter new task (leave blank to keep current):"
            )
            result = self.task_list.modify_task(
                old_date, new_date if new_date else None, new_task if new_task else None
            )
            messagebox.showinfo("Modify Task", result)
            self.refresh_task_list()
        else:
            messagebox.showerror("Error", "Date not found in task list.")

    def delete_task(self):
        date = simpledialog.askstring(
            "Input", "Enter date of task to delete (mm/dd/yyyy):"
        )
        if date:
            result = self.task_list.delete_task(date)
            messagebox.showinfo("Delete Task", result)
            self.refresh_task_list()

    def refresh_task_list(self):
        self.task_list_box.delete(0, tk.END)
        sorted_tasks = self.task_list.sort_by_date()
        for date, task in sorted_tasks.items():
            self.task_list_box.insert(tk.END, f"{date}: {task}")


if __name__ == "__main__":
    task_list = TaskList("tasks.json")
    root = tk.Tk()
    app = TaskListGUI(root, task_list)
    root.mainloop()