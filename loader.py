import json
import os

class Loader:
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