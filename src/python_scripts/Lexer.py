
class Module:
    def __init__(self, funcs=None):
        self.funcs = funcs if funcs else []
    def __repr__(self):
        return f"Module(funcs={self.funcs})"

class Func:
    def __init__(self, name=None, params=None, results=None, locals=None, body=None):
        self.name = name
        self.params = params if params else []
        self.results = results if results else []
        self.locals = locals if locals else []
        self.body = body if body else []
    def __repr__(self):
        return f"Func(name={self.name}, params={self.params}, results={self.results}, locals={self.locals}, body={self.body})"

class Param:
    def __init__(self, name=None, type=None):
        self.name = name
        self.type = type
    def __repr__(self):
        return f"Param(name={self.name}, type={self.type})"

class Local:
    def __init__(self, name=None, type=None):
        self.name = name
        self.type = type
    def __repr__(self):
        return f"Local(name={self.name}, type={self.type})"

class Instruction:
    def __init__(self, op, operands=None):
        self.op = op
        self.operands = operands if operands else []
    def __repr__(self):
        return f"Instr({self.op}, {self.operands})"


class LPAREN:
    def __repr__(self): return "LPAREN()"

class RPAREN:
    def __repr__(self): return "RPAREN()"

class ID:
    def __init__(self, value): self.value = value
    def __repr__(self): return f"ID({self.value})"

class CONST:
    def __init__(self, value): self.value = value
    def __repr__(self): return f"CONST({self.value})"

class STRING:
    def __init__(self, value): self.value = value
    def __repr__(self): return f"STRING({self.value})"

class EOF:
    def __repr__(self): return "EOF()"

# TODO: Further
class Module: pass
class Func: pass
class Param: pass
class Result: pass
class Local: pass
class Export: pass
class Memory: pass
class Data: pass
class Type: pass

# Instruction Classes
class i32_const: pass
class i32_add: pass
class local_get: pass
class local_set: pass
class global_get: pass
class global_set: pass
class call: pass
class _return: pass  # 'return' is a Python keyword

# Keyword and Instruction Sets
KEYWORDS = {
    'module', 'func', 'param', 'result', 'local',
    'export', 'memory', 'data', 'type'
}

INSTRUCTIONS = {
    'i32.const', 'i32.add', 'local.get', 'local.set',
    'global.get', 'global.set', 'call', 'return'
}

class Lexer:
    def __init__(self):
        self.line_number = 1

    def get_token_class(self, lexeme):
        if lexeme in KEYWORDS:
            return globals()[lexeme.capitalize()]
        elif lexeme in INSTRUCTIONS:
            if lexeme == 'return':
                return _return
            return globals()[lexeme.replace('.', '_')]
        return None

    def tokenize(self, wat):
        self.input = wat
        self.pos = 0
        self.tokens = []
        
        while self.pos < len(self.input):
            c = self.input[self.pos]
            
            if c.isspace():
                if c == '\n':
                    self.line_number += 1
                self.pos += 1
            
            elif c == ';' and self.pos + 1 < len(self.input) and self.input[self.pos+1] == ';':
                self.pos += 2
                while self.pos < len(self.input) and self.input[self.pos] != '\n':
                    self.pos += 1
            
            elif c == '"':
                start = self.pos
                self.pos += 1
                while self.pos < len(self.input) and self.input[self.pos] != '"':
                    if self.input[self.pos] == '\\' and self.pos + 1 < len(self.input):
                        self.pos += 1
                    self.pos += 1
                if self.pos >= len(self.input):
                    print(f"Line {self.line_number}: Unclosed string literal")
                    return None
                self.pos += 1
                self.tokens.append(STRING(self.input[start:self.pos]))
            
            elif c == '(':
                self.tokens.append(LPAREN())
                self.pos += 1
            
            elif c == ')':
                self.tokens.append(RPAREN())
                self.pos += 1
            
            elif c.isdigit() or (c == '-' and self.pos + 1 < len(self.input) and self.input[self.pos+1].isdigit()):
                start = self.pos
                if c == '-':
                    self.pos += 1
                while self.pos < len(self.input) and (self.input[self.pos].isdigit() or 
                     self.input[self.pos].lower() in {'x', 'a', 'b', 'c', 'd', 'e', 'f'}):
                    self.pos += 1
                self.tokens.append(CONST(self.input[start:self.pos]))
            
            elif c.isalpha() or c in {'_', '$', '@', '#'}:
                start = self.pos
                self.pos += 1
                while self.pos < len(self.input) and (self.input[self.pos].isalnum() or 
                     self.input[self.pos] in {'_', '.', '+', '-', '$', '@', '#'}):
                    self.pos += 1
                lexeme = self.input[start:self.pos]
                
                token_class = self.get_token_class(lexeme)
                if token_class:
                    self.tokens.append(token_class())
                else:
                    self.tokens.append(ID(lexeme))
            
            else:
                print(f"Line {self.line_number}: Illegal character '{c}'")
                return None
        
        self.tokens.append(EOF())
        return self.tokens
