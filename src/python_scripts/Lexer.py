
import re

class Module:
    def __init__(self, mems=None, globs=None, funcs=None, exports=None):
        self.mems = mems if mems else []
        self.globs = globs if globs else []
        self.funcs = funcs if funcs else []
        self.exports = exports if exports else []

    def __repr__(self):

        # TODO : Refinement, whether it's catogrized in mems, funcs, and exports; 
        #       or according to the definition order in wat code

        mems_str = "\n".join(f"  {repr(m)}" for m in self.mems)
        globs_str = "\n".join(f"  {repr(g)}" for g in self.globs)
        funcs_str = "\n".join(f"  {repr(f)}" for f in self.funcs)
        exports_str = "\n".join(f"  {repr(e)}" for e in self.exports)

        return f"Module:\n{mems_str}\n{globs_str}\n{funcs_str}\n{exports_str}"
        
class Memory:
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value
    def __repr__(self): 
        return f"Memory: {self.name} {self.value})"
   
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
    def __repr__(self): 
        return f"Export: ({self.value}, exp_func={self.exp_func.name})"

class Global:
    def __init__(self, name=None, type=None, value=None):
        self.name = name
        self.type = type
        self.value = value
    def __repr__(self):
        return f"Global(name={self.name}, type={self.type}, value={self.value})"

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
    def __repr__(self): 
        return "LPAREN()"

class RPAREN:
    def __repr__(self): 
        return "RPAREN()"

class ID:
    def __init__(self, value=None): 
        self.value = value
    def __repr__(self): 
        return f"ID({self.value})"

class TYPE:
    def __init__(self, value): 
        self.value = value
    def __repr__(self): 
        return f"TYPE({self.value})"
    
class CONST:
    def __init__(self, value): 
        self.value = value
    def __repr__(self): 
        return f"CONST({self.value})"

class STRING:
    def __init__(self, value): 
        self.value = value
    def __repr__(self): 
        return f"STRING({self.value})"

class EOF:
    def __repr__(self): 
        return "EOF()"

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

                # __init__ will automatically inherated?
    # def __init__(self, op=None, operands=None):
    #     self.op = op
    #     self.operands = operands if operands else []

    def __repr__(self, indent=0):
        indent_str = "  " * indent
        operands_str = []
        for op in self.operands:
            if isinstance(op, Instruction):
                operands_str.append(f"\n      {op.__repr__(indent+1)}")
            else:
                operands_str.append(f"{indent_str}  {op}")
        # print(f'operands_str inside Class ControlFlowInstruction : {operands_str}')
        operands = "\n    ".join(operands_str)
        # print(f'operands inside Class ControlFlowInstruction : {operands}')
        return f"{indent_str}{self.op}:  {operands}"

class BinaryInstruction(Instruction):
    
    # def __init__(self, op=None, operand1=None, operand2=None):
    #     self.op = op
    #     self.operand1 = operand1
    #     self.operand2 = operand2
        # return f"{self.operand1} {self.op} {self.operand2}"
    
    def __init__(self, op=None, operands=None):
        super().__init__(op, operands)
        # if len(self.operands) != 2:
        #     raise ValueError(f"BinaryInstruction requires exactly 2 operands, got {len(self.operands)}")
        
    # def __repr__(self, indent=0):
    #     indent_str = "  " * indent
    #     operands_str = []
        
    #     if isinstance(self.operand1, Instruction):
    #         operands_str.append(self.operand1.__repr__(indent+1))
    #     else:
    #         operands_str.append(f"{indent_str}  {self.operand1}")
        
    #     if isinstance(self.operand2, Instruction):
    #         operands_str.append(self.operand2.__repr__(indent+1))
    #     else:
    #         operands_str.append(f"{indent_str}  {self.operand2}")
            
    #     operands = "\n    ".join(operands_str)
    #     # return f"{indent_str}{self.op}:  {operands}"
    #     return f"{indent_str}{self.operand1} {self.op} {self.operand2}"
        
class _i32_const(Instruction): 
    def __repr__(self): 
        return "_i32_const"
    
class _i32_add(BinaryInstruction):
    def __init__(self, op=None, operands=None):
        super().__init__(op, operands)
    def __repr__(self): 
        return "_i32_add"
    
class _i32_sub(BinaryInstruction):
    def __repr__(self): 
        return "_i32_sub"
class _i32_mul(BinaryInstruction):
    def __repr__(self): 
        return "_i32_mul"
class _i32_div_s(BinaryInstruction):
    def __repr__(self): 
        return "_i32_div_s"
class _i32_ge_u(BinaryInstruction):
    def __repr__(self): 
        return "_i32_ge_u"
class _i32_gt_s(BinaryInstruction):
    def __repr__(self): 
        return "_i32_gt_s"

class _i32_lt_s(BinaryInstruction):
    def __repr__(self): 
        return "_i32_lt_s"
    
class _i32_clz(Instruction):
    def __repr__(self): 
        return "_i32_clz"
    
class _local_get(Instruction):
    # def __init__(self, value=None): 
    #     self.value = value
    # def __repr__(self):  
    #     return f"_local_get({self.value})"
    def __init__(self, op=None, operands=None):
        super().__init__(op, operands)
    def __repr__(self): 
        return "_local_get"
class _local_set(Instruction):
    def __init__(self, op=None, operands=None):
        # print("_local_set op : " + str(op) + " operands : " + str(operands))
        super().__init__(op, operands)
    def __repr__(self): 
        return "_local_set"
class _local_tee: pass
class _global_get: pass
class _global_set: pass

class _call(ControlFlowInstruction): pass
class _return(ControlFlowInstruction): pass
class _nop(ControlFlowInstruction): pass
class _block(ControlFlowInstruction):
    # def __repr__(self): return "_block"     # Definition still necessory in subclass
    def __repr__(self):
        return super(Instruction, self).__repr__()
class _loop(ControlFlowInstruction):
    def __repr__(self):
        return super(Instruction, self).__repr__()
class _br(ControlFlowInstruction): pass
class _br_if(ControlFlowInstruction): pass
class _if(ControlFlowInstruction): pass
    # def __repr__(self):
    #     return super(Instruction, self).__repr__()
class _else(ControlFlowInstruction): pass
class _end(ControlFlowInstruction): pass

class _i32_load(Instruction): pass
class _i32_store(Instruction): pass

class NEWLINE:
    def __init__(self):
        pass
    def __repr__(self): 
        return f"NEWLINE(\\n)"

class SPACE:
    def __init__(self, value): 
        self.value = value
    def __repr__(self): 
        return f"SPACE({self.value})"


# Keyword and Instruction Sets
KEYWORDS = {
    'module', 'func', 'param', 'result', 'local',
    'export', 'memory', 'data', 'type', 'global'
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
            'i32.lt_s': 0,
            
    
            'i32.clz': 0,
                
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
            'if': 'var',
            'else': 'var',
            'end': 'var'
        }

COLORS = {
        
    'ERROR_COLOR': '\033[1;31m',   # Error messages - Bold Red
    'WARNING_COLOR': '\033[1;33m', # Warning messages - Bold Yellow  
    'SUCCESS_COLOR': '\033[1;32m', # Success messages - Bold Green
    'INFO_COLOR': '\033[1;34m',    # Information messages - Bold Blue
    'DEBUG_COLOR': '\033[36m', # Debug messages - Cyan (no bold)
    'HIGHLIGHT_COLOR': '\033[7;37m',   # Highlighted text - Reverse video (white on default background)
    'RESET_COLOR': '\033[0m',  # Reset all styles and colors
}

class Lexer:
    def __init__(self):
        self.line_number = 1
        self.lex_verb_flag = False
        self.lex_col_flag = False
        
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
        
        # print(wat)
        
        while self.pos < len(wat):
            c = wat[self.pos]
            
            if c.isspace():
                if c == '\n':
                    self.tokens.append(NEWLINE())
                    self.line_number += 1
                else:
                    self.tokens.append(SPACE(c))
                self.pos += 1
            
            elif c == ';':
                self.pos += 1
                pass
                # Further comment manipulation
            
            elif c == '"':
                start = self.pos
                self.pos += 1
                while self.pos < len(wat) and wat[self.pos] != '"':
                    if wat[self.pos] == '\\' and self.pos + 1 < len(wat):
                        self.pos += 1
                    self.pos += 1
                if self.pos >= len(wat):
                    print(self._lex_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")  
                    print(f"Line {self.line_number}: Unclosed string literal")
                    return None
                self.pos += 1
                self.tokens.append(STRING(wat[start:self.pos]))
            
            elif c == '(':
                self.tokens.append(LPAREN())
                self.pos += 1
            
            elif c == ')':
                self.tokens.append(RPAREN())
                self.pos += 1
            
            elif c.isdigit() or (c == '-' and self.pos + 1 < len(wat) and wat[self.pos+1].isdigit()):
                start = self.pos
                if c == '-':
                    self.pos += 1
                while self.pos < len(wat) and (wat[self.pos].isdigit() or 
                     wat[self.pos].lower() in {'x', 'a', 'b', 'c', 'd', 'e', 'f'}):
                    self.pos += 1
                self.tokens.append(CONST(wat[start:self.pos]))
            
            elif c.isalpha() or c in {'_', '$'}:
                start = self.pos
                self.pos += 1
                while self.pos < len(wat) and (wat[self.pos].isalnum() or 
                     wat[self.pos] in {'_', '.', '-'}):
                    self.pos += 1
                lexeme = wat[start:self.pos]
                
                token_class = self.get_token_class(lexeme)
                # print("lexer: lex_verb_flag: " + str(lex_verb_flag))
                # if lex_verb_flag:
                if self.lex_verb_flag:
                    print('isalpha() token_class: ' + str(token_class))
                # return None
                if token_class:
                    self.tokens.append(token_class())       # Passing parameters here?
                    
                elif lexeme == "i32":                   # TODO: signed, unsigned, etc.
                    self.tokens.append(TYPE(lexeme))
                else:
                    self.tokens.append(ID(lexeme))
            
            else:
                print(self._lex_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")  
                print(f"Line {self.line_number}: Illegal character '{c}'")
                return None
            
            # if c == '\n':
            #     print("c == '\n'")
        self.tokens.append(EOF())
        
        return self.tokens

    def _lex_colorize(self, text, color_key):
        if self.lex_col_flag:
            return f"{COLORS[color_key]}{text}{COLORS['RESET_COLOR']}"
        return text