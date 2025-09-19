from Lexer import Lexer
from Parser import Parser
from Validator import Validator
from ASTPrinter import ASTPrinter, EnhancedASTPrinter
from Interpreter import interpret_ast, Interpreter
import pprint
import os
import sys
import argparse
from pathlib import Path
import json

verb_flag = False
valid_flag = False
color_flag = False

# ... (keep your existing imports and setup code) ...

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
    '-d',
    '--debug',
    action='store_true',
    help="List all intermediate verbose steps, can be used for debugging purposes"
)

parser.add_argument(
    '-v',
    '--validate',
    action='store_true',
    help="Validate the program based on the generated AST"
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

parser.add_argument(
    '-i',
    '--interpret',
    action='store_true',
    help="Interpret the WebAssembly program"
)

parser.add_argument(
    '-f',
    '--function',
    type=str,
    default="",
    help="Name of the function to execute (default: first exported function)"
)

parser.add_argument(
    '-p',
    '--params',
    type=str,
    default="",
    help="Function parameters as JSON array, e.g., '[1, 2, 3]'"
)

parser.add_argument(
    '-o',
    '--output',
    type=str,
    choices=['text', 'json', 'quiet'],
    default='text',
    help="Output format for results"
)

parser.add_argument('file', type=argparse.FileType('r'), nargs='?', help="Input .wat file")

# ... (keep your existing run_tests function) ...

def main():
    global verb_flag, valid_flag, color_flag
    
    args = parser.parse_args()
    
    # Set flags based on arguments
    if args.debug:
        verb_flag = True
    if args.validate:
        valid_flag = True
    if args.color:
        color_flag = True
    
    # Handle test mode
    if args.test:
        run_tests()
        return
    
    # Check if file was provided
    if not args.file:
        print("Error: No input file specified")
        parser.print_help()
        sys.exit(1)
    
    # Read and process the file
    try:
        wat_code = args.file.read()
        args.file.close()
        
        if verb_flag:
            print("=== SOURCE CODE ===")
            print(wat_code)
            print("===================")
            
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Lexical analysis
    lexer = Lexer()
    if verb_flag:
        lexer.lex_verb_flag = True
    if color_flag:
        lexer.lex_col_flag = True
        
    tokens = lexer.tokenize(wat_code)
    if tokens is None:
        print("Lexical analysis failed")
        sys.exit(1)
        
    if verb_flag:
        print("\n=== TOKENS ===")
        for token in tokens:
            print(token)
        print("==============")
    
    # Parsing
    parser_obj = Parser()
    if verb_flag:
        parser_obj.par_verb_flag = True
    if color_flag:
        parser_obj.par_col_flag = True
    
    print("\n=== Parsing ===")
        
    ast = parser_obj.parse(tokens)
    if ast is None:
        print("Parsing failed")
        sys.exit(1)
    
    # AST Printing
    if args.ast or args.branch or args.color:
        astPrinter = ASTPrinter()
        enhancedAstPrinter = EnhancedASTPrinter()
        
        if args.branch:
            print("\n=== AST (BRANCH STRUCTURE) ===")
            astPrinter.print_ast(ast)
        elif args.color:
            print("\n=== AST (COLORIZED) ===")
            enhancedAstPrinter.print_ast(ast)
        else:
            print("\n=== AST ===")
            pprint.pprint(ast)
    
    # Validation
    validator = Validator()
    if color_flag:
        validator.val_col_flag = True
        
    if valid_flag:
        print("\n=== VALIDATION ===")
        validation_result = validator.validate(ast)
        if validation_result:
            print("✓ Validation passed")
        else:
            print("✗ Validation failed")
            sys.exit(1)
    
    # Interpretation
    if args.interpret:
        print("\n=== INTERPRETATION ===")
        
        # Parse function parameters
        params = []
        if args.params:
            params = args.params.split()
            # try:
            #     params = json.loads(args.params)
            #     if not isinstance(params, list):
            #         print("Error: Parameters must be a JSON array")
            #         sys.exit(1)
            # except json.JSONDecodeError:
            #     print("Error: Invalid JSON format for parameters")
            #     sys.exit(1)
        
        print(params)
        print(list(map(int, params)))
        params = list(map(int, params))
        # Create interpreter
        interpreter = Interpreter(ast, verbose=True, use_colors=color_flag)
        
        # Execute specific function or find exported function
        result = None
        print(args.function)
        if args.function:
            # Find the specified function
            func_to_execute = None
            for func in ast.funcs:
                if func.name == args.function:
                    func_to_execute = func
                    break
            # print("func_to_execute")
            if func_to_execute:
                try:
                    result = interpreter.execute_function(func_to_execute, params)
                except Exception as e:
                    print(f"Error executing function {args.function}: {e}")
                    sys.exit(1)
            else:
                print(f"Error: Function '{args.function}' not found")
                sys.exit(1)
        else:
            # Execute with default behavior (exported function or first function)
            result = interpreter.execute_function("$foo", params)
            print("Result : " + str(type(result)))
            
            # try:
            #     # result = interpreter.execute()
            #     result = interpreter.execute_function("$fib", params)
            # except Exception as e:
            #     print(f"Error during execution: {e}")
            #     sys.exit(1)
        
        # Output results
        if args.output == 'json':
            output_data = {
                "success": True,
                "result": result,
                "stack_size": len(interpreter.stack),
                "memory_size": len(interpreter.memory)
            }
            print(json.dumps(output_data, indent=2))
        elif args.output == 'text':
            if result is not None:
                print(f"Result: {result}")
            else:
                print("Execution completed (no return value)")
            
            # if verb_flag:
            if True:
                print(f"Final stack size: {len(interpreter.stack)}")
                print(f"Memory size: {len(interpreter.memory)} bytes")
        # For 'quiet' mode, no output is printed
        
        print("Stack : " + str(interpreter.stack))
        print("✓ Interpretation completed")

        # result = interpret_ast(ast, True, True)
        # print(result)
if __name__ == "__main__":
    main()