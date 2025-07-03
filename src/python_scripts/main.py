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

print("Tokens:")
for token in tokens:
    # print(f"{token[0].name}: {token[1]}")
    print(f"{token}")
    
# if lexer.lexical_errors:
#     print("Lexical errors:")
#     for error in lexer.lexical_errors:
#         print(error)
# else:
#     # Parse
#     parser = Parser()
#     ast = parser.parse(tokens)
    
#     if parser.errors:
#         print("Parser errors:")
#         for error in parser.errors:
#             print(error)
#     else:
#         print("AST:")
#         pprint.pprint(ast, indent=2)
        
        
# parser = Parser()
# ast = parser.parse(tokens)
# pprint.pprint(ast[:5], width=100)

# with open("ast.txt", "w") as f:
#     pprint.pprint(ast, stream=f)
