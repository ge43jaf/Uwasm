
import re

class Module:
    def __init__(self, mems=None, funcs=None, exports=None):
        self.mems = mems if mems else []
        self.funcs = funcs if funcs else []
        self.exports = exports if exports else []

    def __repr__(self):

        # TODO : Refinement, whether it's catogrized in mems, funcs, and exports; 
        #       or according to the definition order in wat code

        mems_str = "\n".join(f"  {repr(m)}" for m in self.mems)
        funcs_str = "\n".join(f"  {repr(f)}" for f in self.funcs)
        exports_str = "\n".join(f"  {repr(e)}" for e in self.exports)

        return f"Module:\n{mems_str}\n{funcs_str}\n{exports_str}"
        
class Memory:
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value
    def __repr__(self): return f"Memory: {self.name} {self.value})"
   
class Func:
    def __init__(self, name=None, export_name = None, params=None, results=None, locals=None, body=None):
        self.name = name
        self.export_name = export_name
        self.params = params if params else []
        self.results = results if results else []
        self.locals = locals if locals else []
        self.body = body if body else []
        
    def __repr__(self):
        parts = []
        if self.name:
            parts.append(f"  name: {self.name}")
        if self.params:
            parts.append("  params:")
            parts.extend(f"    {p}" for p in self.params)
        if self.results:
            parts.append(f"  results: {self.results}")
        if self.locals:
            parts.append("  locals:")
            parts.extend(f"    {l}" for l in self.locals)
        if self.body:
            parts.append("  body:")
            parts.extend(f"    {i}" for i in self.body)
        return "Func:\n  " + "\n  ".join(parts)

class Export:
    def __init__(self, value=None, exp_func=Func()):
        self.value = value
        self.exp_func = exp_func
    def __repr__(self): return f"Export: ({self.value}, exp_func={self.exp_func.name})"
 
class Instruction:
    def __init__(self, op=None, operands=None):
        self.op = op
        self.operands = operands if operands else []
    
    def __repr__(self, indent=0):
        indent_str = "  " * indent
        operands_str = []
        for op in self.operands:
            if isinstance(op, Instruction):
                operands_str.append(op.__repr__(indent+1))
            else:
                operands_str.append(f"{indent_str}  {op}")
        operands = "\n    ".join(operands_str)
        return f"{indent_str}{self.op}:  {operands}"


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


class LPAREN:
    def __repr__(self): return "LPAREN()"

class RPAREN:
    def __repr__(self): return "RPAREN()"

class ID:
    def __init__(self, value=None): self.value = value
    def __repr__(self): return f"ID({self.value})"

class TYPE:
    def __init__(self, value): self.value = value
    def __repr__(self): return f"TYPE({self.value})"
    
class CONST:
    def __init__(self, value): self.value = value
    def __repr__(self): return f"CONST({self.value})"

class STRING:
    def __init__(self, value): self.value = value
    def __repr__(self): return f"STRING({self.value})"

class EOF:
    def __repr__(self): return "EOF()"

# TODO: Further
# class Module: pass
# class Func: pass
# class Param: pass
class Result: pass
# class Local: pass
# class Export: pass
# class Memory: pass
class Data: pass
# class Type: pass


# Instruction Classes
# class Instruction:
#     def __init__(self, op, operands=None):
#         self.op = op
#         self.operands = operands if operands else []
    
#     def __repr__(self):
#         operands_str = ", ".join(repr(op) for op in self.operands)
#         return f"Instr({self.op}, [{operands_str}])"

class ControlFlowInstruction(Instruction):
    # def __repr__(self):
    #     return super(Instruction, self).__repr__()
    
    # pass

    def __repr__(self, indent=0):
        indent_str = "  " * indent
        operands_str = []
        for op in self.operands:
            if isinstance(op, Instruction):
                operands_str.append(op.__repr__(indent+1))
            else:
                operands_str.append(f"{indent_str}  {op}")
        operands = "\n    ".join(operands_str)
        return f"{indent_str}{self.op}:  {operands}"
        
class _i32_const(Instruction): 
    def __repr__(self): return "_i32_const"
class _i32_add(Instruction): pass

class _i32_sub: pass
class _i32_mul: pass
class _i32_div_s: pass
class _i32_ge_u: pass
class _i32_gt_s: pass

class _local_get(Instruction):
    def __init__(self, value=None): self.value = value
    def __repr__(self): return f"_local_get({self.value})"
class _local_set: pass
class _local_tee: pass
class _global_get: pass
class _global_set: pass

class _call(ControlFlowInstruction): pass
class _return: pass
class _nop(ControlFlowInstruction): pass
class _block(ControlFlowInstruction):
    # def __repr__(self): return "_block"     # Definition still necessory in subclass
    def __repr__(self):
        return super(Instruction, self).__repr__()
class _loop(ControlFlowInstruction): pass
class _br: pass
class _br_if: pass
class _if(ControlFlowInstruction): pass


# Keyword and Instruction Sets
KEYWORDS = {
    'module', 'func', 'param', 'result', 'local',
    'export', 'memory', 'data', 'type'
}

WASM_INSTRUCTIONS = {

            # TODO : Further refinement
            # Numeric instructions
            'i32.const': 1,
            'i32.add': 0,
            'i32.sub': 0,
            'i32.mul': 0,
            'i32.div_s': 0,
            'i32.ge_u': 0,
            'i32.gt_s': 0,
            
            # Memory instructions
            'i32.load': (0, 2),
            'i32.store': (0, 2),
            
            # Variable instructions
            'local.set': 1,
            'local.get': 1,
            'local.tee': 1,
            'global.set': 1,
            'global.get': 1,
            
            # Control flow
            'call': 1,
            'return': 0,
            'nop': 0,
            'block': 'var',
            'loop': 'var',
            'br': 1,
            'br_if': 1,
            'if': 'var'
        }

class Lexer:
    def __init__(self):
        self.line_number = 1

    def get_token_class(self, lexeme):
        if lexeme in KEYWORDS:
            return globals()[lexeme.capitalize()]
        elif lexeme in WASM_INSTRUCTIONS:
            # if lexeme == 'return':
            #     return _return
            
            return globals()['_' + lexeme.replace('.', '_')]
        return None

    def tokenize(self, wat):
        self.input = wat
        self.pos = 0
        self.tokens = []
        
        # Remove two types of comments
        wat = re.sub(r"\(\;.*?\;\)", "", wat, flags=re.DOTALL)

        wat = re.sub(r";;.*", "", wat)
        
        
        while self.pos < len(self.input):
            c = self.input[self.pos]
            
            if c.isspace():
                if c == '\n':
                    self.line_number += 1
                self.pos += 1
            
            elif c == ';':
                pass
                # Further comment manipulation
            
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
            
            elif c.isalpha() or c in {'_', '$'}:
                start = self.pos
                self.pos += 1
                while self.pos < len(self.input) and (self.input[self.pos].isalnum() or 
                     self.input[self.pos] in {'_', '.', '-'}):
                    self.pos += 1
                lexeme = self.input[start:self.pos]
                
                token_class = self.get_token_class(lexeme)
                print('isalpha() token_class: ' + str(token_class))
                # return None
                if token_class:
                    self.tokens.append(token_class())       # Passing parameters here?
                    
                elif lexeme == "i32":                   # TODO: signed, unsigned, etc.
                    self.tokens.append(TYPE(lexeme))
                else:
                    self.tokens.append(ID(lexeme))
            
            else:
                print(f"Line {self.line_number}: Illegal character '{c}'")
                return None
        
        self.tokens.append(EOF())
        
        
        return self.tokens
