import re

# Input: A WAT string
wat_code = """
(module
  (func $add (param $x i32) (param $y i32) (result i32)
    local.get $x
    local.get $y
    i32.add
  )
)
"""

# Tokenize by parentheses and words
def tokenize(wat):
    wat = wat.replace("(", " ( ").replace(")", " ) ")
    return wat.split()

# Recursive parser
def parse_tokens(tokens):
    if not tokens:
        return None
    token = tokens.pop(0)
    if token == '(':
        subexpr = []
        while tokens[0] != ')':
            subexpr.append(parse_tokens(tokens))
        tokens.pop(0)  # Remove ')'
        return subexpr
    elif token == ')':
        raise SyntaxError("Unexpected )")
    else:
        return token

tokens = tokenize(wat_code)
ast = parse_tokens(tokens)

import pprint
pprint.pprint(ast[:5], width=100)

def walk_module(ast):
    assert ast[0] == 'module'
    imports = []
    exports = []
    functions = []
    memory = None
    globals = []

    for item in ast[1:]:
        if isinstance(item, list):
            head = item[0]
            if head == 'import':
                imports.append(item)
            elif head == 'export':
                exports.append(item)
            elif head == 'func':
                functions.append(item)
            elif head == 'memory':
                memory = item
            elif head == 'global':
                globals.append(item)

    return {
        'imports': imports,
        'exports': exports,
        'functions': functions,
        'memory': memory,
        'globals': globals
    }


module_info = walk_module(ast)
print(f"Found {len(module_info['functions'])} functions")
print(f"Memory definition: {module_info['memory']}")
print(f"Exported functions: {[e[2] for e in module_info['exports'] if e[1] == 'func']}")
