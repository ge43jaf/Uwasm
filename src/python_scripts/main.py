from Lexer import Lexer
from Parser import Parser
import pprint

def main():
    # Example WAT code
    wat_code = """
    (module
        (func $add (param $a i32) (param $b i32) (result i32)
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
        return
    
    print("Tokens:")
    for token in tokens:
        print(token)
    
    ast = parser.parse(tokens)
    if ast is None:
        print("Parsing failed")
        return
    
    print("\nAST: Typeof AST:")
    print(type(ast))
    pprint.pprint(ast)

if __name__ == "__main__":
    main()
