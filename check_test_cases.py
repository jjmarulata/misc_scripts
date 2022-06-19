#!/usr/bin/python3

import os
import sys
import re

if len(sys.argv) < 2:
    print("The script requires at least one argument which is a direcotry with TypeScript files to check.")
    exit()
else:
    path_list = sys.argv[1:]

for path in path_list:
    if not os.path.isdir(path):
        print(f"{path} is not a directory")
        continue
    files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".ts")]
    then_at_line = 0
    expects_in_then = 0
    start = 0

    begin_then = re.compile('^Then.*')
    end_then = re.compile('^}\);$')
    expect_statement = re.compile('expect.*')

    for each_file in files:
        #print(f'Checking file {each_file}:')
        with open(each_file, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f):
                if begin_then.search(line):
                    start = 1
                    then_at_line = line_number
                elif start:
                    if end_then.search(line) and not expects_in_then:
                        print(f"No expects found in 'Then' statement on line {then_at_line + 1} in file:\n\t{path}/{each_file}\n")
                        expects_in_then = 0
                        start = 0
                    elif expect_statement.search(line):
                        expects_in_then = 1
