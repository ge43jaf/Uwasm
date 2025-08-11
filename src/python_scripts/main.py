from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter
import pprint



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
    
tokens = lexer.tokenize(wat_code)
if tokens is None:
    print("Lexical analysis failed")

print("Tokens:")
for token in tokens:
    print(token)


ast = parser.parse(tokens)
if ast is None:
    print("Parsing failed")


print("\nAST: Typeof AST:")
print(type(ast))
pprint.pprint(ast)

# print(ast.funcs)
# print(ast.exports)
interpreter = Interpreter()
interpreter.interpret(ast)