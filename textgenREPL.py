#!/usr/bin/env python

""" REPL interface for a TextGenerator instance """

import sys
from TextGenerator import TextGenerator

def executeCommand(commandStr):
    try:
        exec(commandStr)
    except Exception as e:
        print("An exception occurred: " + str(sys.exc_info()))

def parse(command):
    if len(command) < 1:
        return
    
    words = command.split()
    s = len(words)
    c = words[0].lower()

    if c == "q" and s == 1:
        sys.exit("Goodbye")
    elif c == "r" and s == 1:
        executeCommand("generator.resetCorpus()")
    elif c == "s" and s == 2:
        filename = command.split()[1]
        executeCommand("generator.setCorpus(\"" + filename + "\")")
    elif c == "a" and s == 2: 
        filename = command.split()[1]
        executeCommand("generator.addToCorpus(\"" + filename + "\")")
    elif c == "p" and s < 5:
        executeCommand("generator.printText(" + command[2:] + ")")
    elif c == "f" and s == 1:
        if len(generator.files) < 1:
            print("No files yet")
        else:
            print(" ".join(sorted(generator.files)))
    else:
        print("Unknown command")

initialCorpusFile = sys.argv[1] if len(sys.argv) > 1 else None

generator = TextGenerator(initialCorpusFile)

prompt = """Commands:
         r : Reset corpus
         s filename : Set corpus to text in file
         a filename : Add text in file to corpus
         p prefix, sentenceLength, lineLength : Print randomized text
         f : Print filenames in current corpus
         q : Quit\n\n"""

try:
    while True:
        command = input(prompt)
        print()
        parse(command)
        print()
except EOFError:
    sys.exit("Goodbye")

            

