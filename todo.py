from datetime import date
import json
import os

class Todo:
    file_name = 'todo.txt'
    def __init__(self):
        self.todos = {}
        self.cmds = self.set_cmds()
    
    def run(self):
        return self.get_user_input()
    
    def load_todos(self):
        if os.stat(self.file_name).st_size != 0:
            todo_file = open(self.file_name, "r")
            todos = json.load(todo_file)
            self.todos = todos

    def upload_todos(self):
        todo_file = open("todo.txt", "w")
        todo_json = json.dumps(self.todos, indent=4, sort_keys=True, default=str)
        todo_file.write(todo_json)
        todo_file.close()

    def set_cmds(self):
        return {
            'add': self.add,
            'get': self.get,
            'get_all': self.get_all,
            'delete': self.delete,
            'complete': self.complete,
            'update': self.update,
            'exit': self.run,
            '-help': self.show_cmds
        }
    
    def show_cmds(self):
        print('''
        Commands
        --------------------------------------------------------
        add: Add a new task
        get: View an existing task by id
        get: View all existing todos
        delete: Delete an existing task by id
        complete: Set a task as COMPLETE by id
        update: Update the properties of a task by id
        exit: Return to root application command line 
        -help: View all avaiable commands
        ''')
        self.run()
    
    def get_user_input(self):
        '''
            Get user input via terminal
        '''
        user_input = input('> ')
        if user_input not in self.cmds:
            print('Command not found, try again.')
            self.get_user_input()
        else:
            self.cmds[user_input]()

    def add(self):
        '''
            Add new task to todo list
        '''
        self.load_todos()
        todo_id = str(len(self.todos) + 1)
        start_date = date.today()
        due_date = input('Hit y to add due date > ')
        todo_date = None
        if due_date == 'y':
            try:
                year = input('year > ')
                month = input('month > ')
                day = input('day > ')
                todo_date = date(int(year), int(month), int(day))
            except:
                print('An error in storing the date occurred, please try again.')
                self.add()
    
        task = input('task > ')
        self.todos[todo_id] = {
            'creation_date': start_date,
            'task': task,
            'due_date': todo_date,
            'status': 'INCOMPLETE'
        }
        self.upload_todos()
        print(f'Todo #{todo_id} added to list')
        self.run()
    
    def get(self):
        '''
            Get a single task from todo list
        '''
        self.load_todos()

        if len(self.todos) == 0:
            print('No todos in list')
            self.run()
        
        index = input('Todo id > ')
        if index == 'exit':
            self.run()
        elif index in self.todos:
            self.display(index)
            self.run()
        else:
            print('Todo not found, try again.')
            self.get()

    def display(self, index):
        '''
            Display a single task to terminal
        '''
        todo = self.todos[index]
        print(f'''
            # {index}
            creation_date: {todo['creation_date']}
            task: {todo['task']}
            due_date: {todo['due_date']}
            status: {todo['status']}
        ''')
        
    def get_all(self):
        '''
            Get all tasks from todo list
        '''
        self.load_todos()
        length = len(self.todos)
        if length:
            for i in range(length):
                self.display(str(i + 1))
        else:
            print('No todos to display')
        self.run()

    def complete(self):
        '''
            Change the status of a task
            from INCOMPLETE to COMPLETE
        '''
        self.load_todos()
        index = input('Todo id > ')
        if index == 'exit':
            self.run()
        elif index in self.todos and self.todos[index]['status'] == 'INCOMPLETE':
            self.display(index)
            new_status = input('Hit y to complete this todo > ')
            if new_status == 'y':
                self.todos[index]['status'] = 'COMPLETE'
                self.upload_todos()
                print(f'Todo #{index} completed')
            self.run()
        else:
            print('Todo not found or already COMPLETE, try again.')
            self.complete()
    
    def delete(self):
        '''
            Delete a task from todo list
        '''
        self.load_todos()
        index = input('Todo id > ')
        if index == 'exit':
            self.run()
        elif index in self.todos:
            self.display(index)
            delete = input('Hit y to delete this todo > ')
            if delete == 'y':
                del self.todos[index]
                new_todos = {}
                new_index = 1
                for todo in self.todos:
                    new_todos[str(new_index)] = self.todos[todo]
                    new_index += 1
                self.todos = new_todos
                self.upload_todos()
                print(f'Todo #{index} deleted')
        elif len(self.todos) == 0:
            print('No todos available to delete')
        else:
            print('Todo not found, try again.')
            self.delete()
        self.run()
    
    def update(self):
        '''
            Update a single task from todo list
        '''
        self.load_todos()

        # check for existing todos
        if len(self.todos) == 0:
            print('No todos in list to update')
            self.run()
        
        index = input('Todo id > ')
        if index == 'exit':
            self.run()
        elif index in self.todos:
            new_todo = {
                'creation_date': self.todos[index]['creation_date'],
                'task': self.todos[index]['task'],
                'due_date': self.todos[index]['due_date'],
                'status': self.todos[index]['status'] 
            }
            self.display(index)
            creation_date = input('Hit y to change creation date > ')
            if creation_date == 'y':
                try:
                    year = input('year > ')
                    month = input('month > ')
                    day = input('day > ')
                    new_todo['creation_date'] = date(int(year), int(month), int(day))
                except:
                    print('An error in changing the creation date occurred, please try again.')
                    self.update()
            due_date = input('Hit y to change due date > ')
            if due_date == 'y':
                try:
                    year = input('year > ')
                    month = input('month > ')
                    day = input('day > ')
                    new_todo['due_date'] = date(int(year), int(month), int(day))
                except:
                    print('An error in changing the due date occurred, please try again.')
                    self.update()
            task = input('Hit y to change task > ')
            if task == 'y':
                try:
                    new_task = input('Write new task > ')
                    new_todo['task'] = new_task
                except:
                    print('An error in changing the task occurred, please try again.')
                    self.update()
            status = input('Hit y to change status > ')
            if status == 'y':
                try:
                    new_status = input(' 1 - change status to INCOMPLETE \n 2 - change status to COMPLETE \n > ')
                    if new_status == '1':
                        new_todo['status'] = 'INCOMPLETE'
                    elif new_status == '2':
                        new_todo['status'] = 'COMPLETE'
                    else:
                        print('You must chose 1 or 2, please try again.')
                        self.update()
                except:
                    print('An error in changing the status occurred, please try again.')
                    self.update()
            self.todos[index] = new_todo
            self.upload_todos()
            self.display(index)
            print(f'Todo #{index} successfully updated')
            self.run()


if __name__ == '__main__':
    Todo().run()

