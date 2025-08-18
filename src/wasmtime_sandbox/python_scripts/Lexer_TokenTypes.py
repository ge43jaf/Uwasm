# Token Types as standalone classes
class LPAREN:
    def __init__(self): pass
    def __repr__(self): return "LPAREN()"

class RPAREN:
    def __init__(self): pass
    def __repr__(self): return "RPAREN()"

class ID:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"ID({repr(self.value)})"

class CONST:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"CONST({repr(self.value)})"

class STRING:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"STRING({repr(self.value)})"

# Keywords
class MODULE:
    def __init__(self): pass
    def __repr__(self): return "MODULE()"

class FUNC:
    def __init__(self): pass
    def __repr__(self): return "FUNC()"

class PARAM:
    def __init__(self): pass
    def __repr__(self): return "PARAM()"

class RESULT:
    def __init__(self): pass
    def __repr__(self): return "RESULT()"

class LOCAL:
    def __init__(self): pass
    def __repr__(self): return "LOCAL()"

class IMPORT:
    def __init__(self): pass
    def __repr__(self): return "IMPORT()"

class EXPORT:
    def __init__(self): pass
    def __repr__(self): return "EXPORT()"

class MEMORY:
    def __init__(self): pass
    def __repr__(self): return "MEMORY()"

class DATA:
    def __init__(self): pass
    def __repr__(self): return "DATA()"

class TYPE:
    def __init__(self): pass
    def __repr__(self): return "TYPE()"

# Instructions
class I32_CONST:
    def __init__(self): pass
    def __repr__(self): return "I32_CONST()"

class I32_ADD:
    def __init__(self): pass
    def __repr__(self): return "I32_ADD()"

class LOCAL_GET:
    def __init__(self): pass
    def __repr__(self): return "LOCAL_GET()"

class LOCAL_SET:
    def __init__(self): pass
    def __repr__(self): return "LOCAL_SET()"

class GLOBAL_GET:
    def __init__(self): pass
    def __repr__(self): return "GLOBAL_GET()"

class GLOBAL_SET:
    def __init__(self): pass
    def __repr__(self): return "GLOBAL_SET()"

class CALL:
    def __init__(self): pass
    def __repr__(self): return "CALL()"

class RETURN:
    def __init__(self): pass
    def __repr__(self): return "RETURN()"

class EOF:
    def __init__(self): pass
    def __repr__(self): return "EOF()"

class Lexer:
    def __init__(self):
        self._lexical_errors = []
        self.line_number = 1

    def _is_keyword(self, lexeme):
        return lexeme in {
            'module', 'func', 'param', 'result', 'local',
            'import', 'export', 'memory', 'data', 'type'
        }

    def _is_instruction(self, lexeme):
        return lexeme in {
            'i32.const', 'i32.add', 'local.get', 'local.set',
            'global.get', 'global.set', 'call', 'return'
        }

    def tokenize(self, wat):
        self.input = wat
        self.pos = 0
        self.tokens = []
        
        while self.pos < len(self.input):
            c = self.input[self.pos]
            
            # Skip whitespace
            if c.isspace():
                if c == '\n':
                    self.line_number += 1
                self.pos += 1
                continue
                
            # Handle comments
            if c == ';' and self.pos + 1 < len(self.input) and self.input[self.pos+1] == ';':
                self.pos += 2
                while self.pos < len(self.input) and self.input[self.pos] != '\n':
                    self.pos += 1
                continue
                
            # Handle strings
            if c == '"':
                start = self.pos
                self.pos += 1
                while self.pos < len(self.input) and self.input[self.pos] != '"':
                    if self.input[self.pos] == '\\' and self.pos + 1 < len(self.input):
                        self.pos += 1  # skip escaped character
                    self.pos += 1
                if self.pos >= len(self.input):
                    self._lexical_errors.append((self.line_number, "Unclosed string literal"))
                    self.tokens.append(EOF())
                    return self.tokens
                self.pos += 1
                self.tokens.append(STRING(self.input[start:self.pos]))
                continue
                
            # Handle symbols
            if c == '(':
                self.tokens.append(LPAREN())
                self.pos += 1
                continue
            if c == ')':
                self.tokens.append(RPAREN())
                self.pos += 1
                continue
                    
            # Handle numbers
            if c.isdigit() or (c == '-' and self.pos + 1 < len(self.input) and self.input[self.pos+1].isdigit()):
                start = self.pos
                if c == '-':
                    self.pos += 1
                while self.pos < len(self.input) and (self.input[self.pos].isdigit() or 
                     self.input[self.pos].lower() in {'x', 'a', 'b', 'c', 'd', 'e', 'f'}):
                    self.pos += 1
                self.tokens.append(CONST(self.input[start:self.pos]))
                continue
                
            # Handle identifiers, keywords, and instructions
            if c.isalpha() or c in {'_', '$', '@', '#'}:
                start = self.pos
                self.pos += 1
                while self.pos < len(self.input) and (self.input[self.pos].isalnum() or 
                     self.input[self.pos] in {'_', '.', '+', '-', '$', '@', '#'}):
                    self.pos += 1
                lexeme = self.input[start:self.pos]
                
                # Check for multi-word instructions
                if '.' in lexeme:
                    if lexeme == 'i32.const':
                        self.tokens.append(I32_CONST())
                        continue
                    if lexeme == 'i32.add':
                        self.tokens.append(I32_ADD())
                        continue
                    if lexeme == 'local.get':
                        self.tokens.append(LOCAL_GET())
                        continue
                    if lexeme == 'local.set':
                        self.tokens.append(LOCAL_SET())
                        continue
                    if lexeme == 'global.get':
                        self.tokens.append(GLOBAL_GET())
                        continue
                    if lexeme == 'global.set':
                        self.tokens.append(GLOBAL_SET())
                        continue
                
                # Check keywords
                if lexeme == 'module':
                    self.tokens.append(MODULE())
                    continue
                if lexeme == 'func':
                    self.tokens.append(FUNC())
                    continue
                if lexeme == 'param':
                    self.tokens.append(PARAM())
                    continue
                if lexeme == 'result':
                    self.tokens.append(RESULT())
                    continue
                if lexeme == 'local':
                    self.tokens.append(LOCAL())
                    continue
                if lexeme == 'import':
                    self.tokens.append(IMPORT())
                    continue
                if lexeme == 'export':
                    self.tokens.append(EXPORT())
                    continue
                if lexeme == 'memory':
                    self.tokens.append(MEMORY())
                    continue
                if lexeme == 'data':
                    self.tokens.append(DATA())
                    continue
                if lexeme == 'type':
                    self.tokens.append(TYPE())
                    continue
                if lexeme == 'call':
                    self.tokens.append(CALL())
                    continue
                if lexeme == 'return':
                    self.tokens.append(RETURN())
                    continue
                
                # Default to ID
                self.tokens.append(ID(lexeme))
                continue
                
            # Unknown character
            self._lexical_errors.append((self.line_number, f"Illegal character '{c}'"))
            self.pos += 1
            
        self.tokens.append(EOF())
        return self.tokens

    @property
    def lexical_errors(self):
        return self._lexical_errors
