"""Lists all todo's in a directory.
It provides a hyperlink to file:line.
Tells you the class and function (if it is in one).
And then the text in the todo

NOT BEEN TESTED but works for my use cases
"""


import fileinput
from pathlib import Path

# location (0-filename, 1-class, 2-indent, 3-function)
def checkDents(stack, location):
    """Append/pop location to stack depending on relative indent/dedents."""
    if location[2] == -3:
        stack.append(location)
    elif location[2] < stack[len(stack)-1][2]:
        stack.pop()
        checkDents(stack, location)
    elif location[2] > stack[len(stack)-1][2]:
        stack.append(location)
    elif location[2] == stack[len(stack)-1][2]:
        stack.pop()
        stack.append(location)

# Grab all python files that aren't in venv/ or in this file.
files = [f for f in Path().rglob("*.py") if 'venv/' not in str(f) and 'pytodo' not in str(f)]
stack = [] # (filename, function_name, indent, class_name)

with fileinput.input(files=files, encoding='utf-8') as f:
    stack.append((f.filename(), None, -3, None))
    # file      - 0
    # class     - 1
    # indent    - 2
    # function  - 3
    for line in f:
        if f.filename() != stack[len(stack)-1][0]:
            # If we switch files then reset stack
            stack.clear()
            stack = [(f.filename(), None, -3, None)]
        if 'def ' in line and '(' in line:
            # If found new function then get location and checkDent
            last_class = stack[len(stack)-1][1]
            indent = line.index('def')
            location = (f.filename(), last_class, indent, line[indent+4:line.index('(')])
            checkDents(stack, location)
        if 'class ' in line and (':' in line or '(' in line):
            # If found new class then get location and checkDent
            indent = line.index('class')
            new_class = line[indent+6:line.index('(')] if '(' in line else line[indent+6:line.index(':')]
            location = (f.filename(), new_class, indent, None)
            checkDents(stack, location)

        if 'TODO' in line:
            # Print todo to screen.
            last = stack[len(stack)-1]
            second_text = line[line.index('TODO')+5:len(line)-1]
            first_text = '{name}:{line}:0'.format(name=f.filename(), line=f.filelineno())
            between = f'{last[1]} {last[3]}'
            print('{first_text:<35s} | {between:<20s} | {text}'.format(first_text=first_text, between=between, text=second_text))