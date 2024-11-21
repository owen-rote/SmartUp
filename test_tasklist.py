import tasklist 

class_obj = tasklist.TaskList("new.json")

response = input("Response: ")

if response == 'N':
    data = class_obj.add_task()
    print(data)

if response == 'Y':
    modify_data = class_obj.modify_task()
    print(modify_data)
    
if response == 'B':
    delete_data = class_obj.delete_task()
    print(delete_data)

if response == 'P':
    print_data = class_obj.print_tasks()
    print(print_data)    