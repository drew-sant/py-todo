# Python TODO list Generator

Prints out a list of todo's in python files found in the directory.
It will also print out a hyperlink to the line in the file that the
todo is located. It will also print the name of the class or function
that the todo is located in.

## Setup

Place the file in the directory that you want to search and run:

```
python pytodo.py
```

I have it setup like this for simplicity but plan on imporving it with
finer controls.

## Tests

NOT YET TESTED
I plan on making a comprehesive test suit for this to help me improve it.
In the mean time, it works for all of my use cases so far.

## How it works

It searches for lines that contain 'TODO ' while maintaining a stack where
the top contains: the indent level, class name, function name and filename
(location data). When it enters a different file, the stack clears. Each
time we enter a line that looks like a class or function definition, we
check the indent level and update the location data. When the indent goes
up, the stack appends the new location data. When there is a dedent, the
stack pops off the end and then checks the indent level again in a recursion.
When the indent level remains the same for a new def or class then we pop off
the old and append the new location data.

## Tasks
* Create tests
* Improve the look of the print out
* Add args and make it more user friendly
