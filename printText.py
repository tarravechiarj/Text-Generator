#!/usr/bin/env python

import sys
from TextGenerator import TextGenerator

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " <file> [Optional] <words> <maxLineLength> <firstWord>")

generator = TextGenerator(sys.argv[1])

if len(sys.argv) < 3:
    generator.printText()
elif len(sys.argv) < 4:
    generator.printText(None, int(sys.argv[2]))
elif len(sys.argv) < 5:
    generator.printText(None, int(sys.argv[2]), int(sys.argv[3]))
else:
    generator.printText(sys.argv[4], int(sys.argv[2]), int(sys.argv[3]))

