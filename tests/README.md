# Unit Testing Package for Hash Raft

## How to run
In a terminal with Python 3 installed, navigate to this projects root directory. 
Enter the command: `python3.9 -m tests` in your terminal.

## How to add your own unit tests
1. Create a new file under `/tests`, name if after the file you would like to test.
2. Add the following import statments:
    1. `from .context import hashraft`: This will allow you to import packages and modules from the project.
    2. `import unittest`: This is the built-in Python 3 unit testing library. 
    3. Any other modules of packages, from the project or third-party, that you need.
3. Create a new class **with the same name as the file** that inherits `unittest.TestCase`. For example: `class Name (unittest.TestCase):`. This class must be the only class in the file. 
4. Each class method you add becomes it's own unit test. If you need a set up and tear down routine you can define that by implementing the `setUp (self)` and `tearDown (self)` methods. 
5. At this point you are finished! Run the testing package to run your tests.

## What is currently tested
- EventLogger
    