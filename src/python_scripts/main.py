import pprint
from Lexer import Lexer
from Parser import Parser

wat_code = """
    (module
    (func (export "addTwo") (param i32 i32) (result i32)
        local.get 0
        local.get 5
        i32.add))
    )
    """

lexer = Lexer()
tokens = lexer.tokenize(wat_code)

parser = Parser()
ast = parser.parse(tokens)
pprint.pprint(ast[:5], width=100)

# with open("ast.txt", "w") as f:
#     pprint.pprint(ast, stream=f)