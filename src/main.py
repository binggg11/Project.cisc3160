import re
import os

class Interpreter:
    def __init__(self):
        self.variables = {}

    def parse(self, program):
        assignments = program.split(';')
        for a in assignments:
            if a.strip():
                self.evaluate_assignment(a.strip() + ';')

    def evaluate_assignment(self, assignment):
        match = re.match(r'([a-zA-Z_][a-zA-Z_0-9]*) *= *(.+);$', assignment)
        if not match:
            raise SyntaxError("Syntax error in assignment: " + assignment)

        var_name, expression = match.groups()
        self.variables[var_name] = self.evaluate_expression(expression)

    def evaluate_expression(self, expression):
        tokens = re.findall(r'[()]|[-+*]|[\d]+|[a-zA-Z_][a-zA-Z_0-9]*', expression)
        for i, token in enumerate(tokens):
            if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*', token):
                if token not in self.variables:
                    raise NameError(f"Uninitialized variable: {token}")
                tokens[i] = str(self.variables[token])

        try:
            return eval(''.join(tokens))
        except SyntaxError:
            raise SyntaxError("Invalid expression: " + expression)

    def run(self, program):
        try:
            self.parse(program)
            for var, val in self.variables.items():
                print(f"{var} = {val}")
        except (SyntaxError, NameError) as e:
            print("error")

    def run_from_file(self, file_path):
        with open(file_path, 'r') as file:
            program = file.read()
            self.run(program)

# Function to get all .txt files in the current directory
def get_txt_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.txt')]

# Create an instance of the Interpreter
interpreter = Interpreter()

# Get all .txt files in the current directory
file_paths = get_txt_files(".")

# Run the interpreter for each file
for file_path in file_paths:
    print(f"Running {file_path}:")
    interpreter = Interpreter()  # Reset the interpreter for each file
    interpreter.run_from_file(file_path)
    print()
