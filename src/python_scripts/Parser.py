import pprint

class Parser:
    def __init__(self):
        self.ast = []
        self.WASM_INSTRUCTIONS = {

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


    def parse(self, tokens):
        return self.parse_module(tokens)
        
    def parse_module(self, tokens):    
        if not tokens:
            print("CompilationError: Token list ot initialized")
            return None
            
        if len(tokens) == 0:
            print("SyntaxError: Expected ( at the start of the program")
            return None
            
        # Should first check (module ...)
        token = tokens.pop(0)
        print('Token : "' + token + '" ')
        if token != '(':
            print("SyntaxError: Expected ( at the start of the program")
            return None
        
        token = tokens.pop(0)
        print('Token : "' + token + '" ')
        
        if token != 'module':
            print("SyntaxError: Expected a module at the beginning")
            return None
        
        if tokens[-1] != ')':
            print("SyntaxError: Expected ) at the end of the program")
            return None
        
        token = tokens.pop(0)
        print('Token : "' + token + '" ')
        
        if token == ')':
            print("Syntax Correct!)")       # A little duplicate here
            return None
        elif token == '(':
            # expression = []
            # while tokens and tokens[0] != ')':
            #     expression.append(self.parse(tokens))
            # if tokens:
            #     tokens.pop(0)
            # return expression
            
            return self.parse_functions(token, tokens)
            
        else:
            # return self.validate(token, tokens)
            print("SyntaxError: All terms7expression surrounded with (...) expected")
            return None
        
    def parse_functions(self, token, tokens):
        
        funcs = {}
        
        token = tokens.pop(0)
        print('parse_functions Token : "' + token + '" ')
        
        if token != 'func':
            print("SyntaxError: Only func supported after module")
            return None
            
        token = tokens.pop(0)
        print('parse_functions Token : "' + token + '" ')
        
        if token[0] == '$':         # TODO: Further validations waited
            funcs.add(token[1:])
        elif token == '(':
            
            
            
        
    def validate(self, instruction, tokens):
        
        if instruction not in self.WASM_INSTRUCTIONS:
            print(f"SyntaxError: Unknown instruction '{instruction}'")
            return None

        params = self.WASM_INSTRUCTIONS[instruction]

        if params == 0:
            print(f"Valid instruction '{instruction}' with 0 parameters")
            # Validate remaining tokens recursively
            if tokens and tokens[0] not in ('(', ')'):
                self._validate_instruction(tokens.pop(0), tokens)
            return instruction
        
        

        
