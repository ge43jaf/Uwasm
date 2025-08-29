from Lexer import Lexer
from Parser import Parser
import main
import pprint

import argparse
import sys
import os
from pathlib import Path

parser = argparse.ArgumentParser(description="An interpreter for WASM")

parser.add_argument(
    '-t',
    '--test',
    action='store_true',
    help="Run all test files in ../tests/success and ../tests/failure"
)

parser.add_argument(
    '-a',
    '--ast',
    action='store_true',
    help="Generate AST for the input"
)

parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help="List all intermediate steps, can be used for debugging purposes"
)

args = parser.parse_args()

def run_tests():
    test_dirs = ["../tests/success", "../tests/failure"]
    for test_dir in test_dirs:
        print(f"\nRunning tests in {test_dir}:")
        if not os.path.exists(test_dir):
            print(f"Directory {test_dir} not found")
            continue
            
        for test_file in Path(test_dir).glob('*'):
            if test_file.is_file():
                print(f"\nProcessing {test_file}...")
                
                lexer = Lexer()
                parser = Parser()
                    
                tokens = lexer.tokenize(test_file.read_text())
                if tokens is None:
                    print("Lexical analysis failed")

                    
                print("Tokens:")
                for token in tokens:
                    print(token)
                    
                ast = parser.parse(tokens)
                if ast is None:
                    print("Parsing failed")
                print(f"Test {test_file.name} completed")


if args.test:
    run_tests()
elif args.ast:
    main.verb_flag = False
    main()

elif args.verbose:
    main.verb_flag = True
    main()
    
else:
    print("Error: Either specify an input file or use -t to run tests")
    parser.print_help()
    