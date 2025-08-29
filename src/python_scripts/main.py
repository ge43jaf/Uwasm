from Lexer import Lexer
from Parser import Parser
from Validator import Validator
import pprint

verb_flag = False

wat_code = """
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

try:
    with open('../tests/success/test004_export.wat', 'r') as file:
        wat_code = file.read()
except FileNotFoundError:
    print("Error: File '../test/success' not found.")

print(wat_code)

lexer = Lexer()
parser = Parser()
    
if verb_flag:
    lexer.lex_verb_flag = True
    parser.par_verb_flag = True
else:
    lexer.lex_verb_flag = False
    parser.par_verb_flag = False
    

tokens = lexer.tokenize(wat_code)
if tokens is None:
    print("Lexical analysis failed")

if verb_flag:
    print("Tokens:")
    for token in tokens:
        print(token)


ast = parser.parse(tokens)
if ast is None:
    print("Parsing failed")

if verb_flag:
    print("\nAST: Typeof AST:")
    print(type(ast))

pprint.pprint(ast)

# print(ast.funcs)
# print(ast.exports)
validator = Validator()
validator.interpret(ast)