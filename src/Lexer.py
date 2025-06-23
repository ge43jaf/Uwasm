import pprint
import re
from collections import defaultdict


wat_path = "functions.wat"

wat_code = """
    (module
      (func $init (param $x i32) (local $temp i32)
        (i32.const 10)
        (local.set $temp)
        (local.get $temp)
        (call $log)
        (i32.const 20)
        (i32.const 30)
        (i32.add)
        (call $log)
        (return)
      )
      (export "init" (func $init))
    )
    """

class Lexer:
    def __init__(self):
        self.globals = {}
        self.stack = []
        self.functions = {}
        self.output = []
        self.memory = defaultdict(int)
        self.locals = {}
        self.wat = wat_code
        self.tokens = []
        self.ast = []
        
    def lex(self, wat):
        
        wat = re.sub(r"\(\;.*?\;\)", "", wat, flags=re.DOTALL)
        wat = re.sub(r";;.*", "", wat)
        wat = wat.replace("(", " ( ").replace(")", " ) ")
        tokens = wat.split()
        return tokens
    
    
    def parse_tokens(self, tokens):

        if not tokens:
            return None
        token = tokens.pop(0)
        if token == '(':
            subexpr = []
            while tokens and tokens[0] != ')':
                subexpr.append(self.parse_tokens(tokens))
            if tokens:
                tokens.pop(0)
            return subexpr
        elif token == ')':
            raise SyntaxError("Unexpected )")
        else:
            return token
        
lexer = Lexer()

ast = lexer.parse_tokens(lexer.lex(wat_code))



pprint.pprint(ast)
