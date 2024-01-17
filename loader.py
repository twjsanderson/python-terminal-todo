import json
import os

class Loader:
    file_name = 'todo.txt'
    def load_todos(self):
        '''
            Read tasks from todo.txt & convert to json
        '''
        if os.stat(self.file_name).st_size != 0:
            todo_file = open(self.file_name, "r")
            todos = json.load(todo_file)
            self.todos = todos

    def upload_todos(self):
        '''
            Convert tasks to json & write to todo.txt
        '''
        todo_file = open(self.file_name, "w")
        todo_json = json.dumps(self.todos, indent=4, sort_keys=True, default=str)
        todo_file.write(todo_json)
        todo_file.close()