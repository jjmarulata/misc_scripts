#!/usr/bin/python3

import os
import sys
import re
import argparse

#if len(sys.argv) < 2:
    #print("The script requires at least one argument which is a direcotry with TypeScript files to check.")
    #exit()
#else:
    #path_list = sys.argv[1:]
def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def file_path(file):
    if os.path.isfile(file):
        return file
    else:
        raise argparse.ArgumentTypeError(f'{file} is not a valid file or does not exist')

parser = argparse.ArgumentParser(description="Script to check if 'Then' statements in TypeScript files have expect statements.")
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--directories', type=dir_path, nargs='+', help='One or more directories which hold TypeScript files using the .ts extension.')
group.add_argument('-f', '--files', type=file_path, help='One or more TypeScript files.')


args = parser.parse_args()

def check_files(files):
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
                    if end_then.search(line):
                        if expects_in_then:
                            expects_in_then = 0
                            start = 0
                        else:
                            print(f"No expects found in 'Then' statement on line {then_at_line + 1} in file:\n\t{each_file}\n")
                    elif expect_statement.search(line):
                        expects_in_then = 1
def main():
    if args.directories:
        for path in args.directories:
            if not os.path.isdir(path):
                print(f"{path} is not a directory")
                continue
            files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".js")]
            check_files(files)
    elif args.files:
        check_files(args.files)

if __name__ == "__main__":
    main()