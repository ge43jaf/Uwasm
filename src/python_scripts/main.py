from Lexer import Lexer
from Parser import Parser
from Validator import Validator
from ASTPrinter import ASTPrinter, EnhancedASTPrinter
import pprint

import os
import argparse
from pathlib import Path

verb_flag = False
valid_flag = False
color_flag = False

wat_code_0 = """
    (module
        (memory $mem1 1)
    
        (func $add (param $a i32) (param $b i32) (result i32)
            (local.get $a)
            (local.get $b)
            (i32.add)
        )
        (export "add" (func $add))
        
        (func $getAnswer (result i32)
            (i32.const 42))
        (func (export "getAnswerPlus1") (result i32)
            
            (i32.const 1)
            (i32.add))
        (func $qwe
            nop
            
        )
    )
    """

wat_code______to_test = """
(module
  ;;(import "console" "log" (func $log (param i32)))
  (func $fib (param $fib i32) (result i32)
    (local $a i32)
    (local $b i32)
    (local $nextTerm i32)

    local.get $fib
    i32.const 2
    i32.lt_s
    if
      local.get $fib
      call $log
      local.get $fib
      return
    end

    ;; Stack: a=0, b=1
    i32.const 0
    local.set $a
    local.get $a
    call $log

    i32.const 1
    local.set $b
    local.get $b
    call $log

    loop $loop
      local.get $a
      local.get $b
      i32.add
      local.set $nextTerm
      local.get $nextTerm
      call $log
    
      local.get $b
      local.set $a
    
      local.get $nextTerm
      local.set $b
    
      local.get $fib
      i32.const 1
      i32.sub
      local.set $fib
    
      local.get $fib
      i32.const 0
      i32.gt_s
      br_if $loop
    end
    
    local.get $b
  )

  (export "fib" (func $fib))
)
"""
wat_code = """(module
(memory $mem1 1)
  (func $add (param $a i32) (param $b i32) (result i32)
            (local $a i32)
            (local $b i32)
            (local.get $a)
            (local.get $b)
            (i32.add)
        )
        (export "add" (func $add))
        (export "add" (func $ad))
        )

    
"""
# TODO : export check name existance, etc.

try:
    with open('../tests/success/test004_export.wat', 'r') as file:
        wat_code = file.read()
except FileNotFoundError:
    print("Error: File '../test/success' not found.")


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

parser.add_argument(
    '-i',
    '--interprete',
    action='store_true',
    help="Validate the programm based on the generated AST"
)

parser.add_argument(
    '-b',
    '--branch',
    action='store_true',
    help="Generate AST with branch structure"
)

parser.add_argument(
    '-c',
    '--color',
    action='store_true',
    help="Generate AST with branch and colorized keywords"
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

                # if args.verbose:    
                #     print("Tokens:")
                #     for token in tokens:
                #         print(token)
                    
                ast = parser.parse(tokens)
                if ast is None:
                    print("\033[31mParsing failed\033[0m")
                print(f"Test {test_file.name} completed")


if args.test:
    run_tests()
elif args.ast:
    verb_flag = False
    valid_flag = False
    
elif args.verbose:
    verb_flag = True
    
elif args.interprete:
    valid_flag = True
elif args.color:
    color_flag = True
else:
    print("Error: Either specify an input file or use -t to run tests")
    parser.print_help()
    
print("main.verb_flag: " + str(verb_flag))

if verb_flag:
    print(wat_code)

lexer = Lexer()
parser = Parser()
validator = Validator()

if verb_flag:
    lexer.lex_verb_flag = True
    parser.par_verb_flag = True
else:
    lexer.lex_verb_flag = False
    parser.par_verb_flag = False

if color_flag:
    lexer.lex_col_flag = True
    parser.par_col_flag = True
    validator.val_col_flag = True
else:
    lexer.lex_col_flag = False
    parser.par_col_flag = False
    validator.val_col_flag = False
    
print("lexer.lex_verb_flag: " + str(lexer.lex_verb_flag), "\nparser.par_verb_flag: " + str(parser.par_verb_flag) )
tokens = lexer.tokenize(wat_code)
if tokens is None:
    print("Lexical analysis failed")

if verb_flag:
# if True:
    print("Tokens:")
    for token in tokens:
        print(token)


ast = parser.parse(tokens)
astPrinter = ASTPrinter()
enhancedAstPrinter = EnhancedASTPrinter()

if args.branch:
    astPrinter.print_ast(ast)
elif args.color:
    enhancedAstPrinter.print_ast(ast)

if ast is None:
    print("Parsing failed")

if verb_flag:
    print("\nAST: Typeof AST:")
    print(type(ast))

pprint.pprint(ast)

# print(ast.funcs)
# print(ast.exports)

validator.validate(ast)
