from Lexer import Lexer
from Parser import Parser
import pprint


wat_code = """
    (module
        (func $add (param $a i32) (param $b i32) (result i32)
            (local.get $a)
            (local.get $b)
            (i32.add)
        )
        (func $addTest (param $a i32) (param $b i32) (result i32)
            (local.get $a)
            (local.get $b)
            (i32.add)
        )
        (export "add" (func $add))
    )
    """
    
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

