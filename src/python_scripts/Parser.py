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
        
        if tokens[-1] != ')':
            print("SyntaxError: Expected ) at the end of the program")
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
            print("SyntaxError: All terms/expression surrounded with (...) expected")
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
            return self.parse_function_signature(token, tokens)
        else:
            print("SyntaxError: Function signature not defined")     # TODO: Add situation like nop
            return None
            
    
    def parse_function_signature(self, token, tokens):
        params = {}
        locals = {}
        
        print('Parse signature, tokens : ')
        print(tokens)
        
        # (...) (...) (...)
        while tokens and tokens[0] != ')':
            if tokens[0] == 'export':
                tokens.pop(0)
                # TODO: Validation: Existance + Type
                token = tokens.pop(0)
                # Operations for export
                
                token = tokens.pop(0)
                print('Token in while export : ' + token)
                
                if token != ')':
                    print("SyntaxError: Expected ) at the end of function result")
                    return None
                elif tokens:
                    token = tokens.pop(0)
                    print('Token in while export elif : ' + token)
                    if(token == '('):
                        self.parse_function_signature(token, tokens)     # TODO : Single export?
                    else:
                        break
                else:
                    print("SyntaxError: Unexpected EOF at function result")
                    
            elif tokens[0] == 'param':
                
                tokens.pop(0)
                # TODO: Validation: Existance + Type
                token = tokens.pop(0)
                params.add(token)
                
                token = tokens.pop(0)
                if token != ')':
                    print("SyntaxError: Expected ) at the end of function params")
                    return None
                elif tokens:
                    token = tokens.pop(0)
                    if(token == '('):
                        self.parse_function_signature(token, tokens)
                    else:
                        break
                else:
                    print("SyntaxError: Unexpected EOF at function params")
                    return None
                    
            elif tokens[0] == 'local':
                tokens.pop(0)
                # TODO: Validation: Existance + Type
                token = tokens.pop(0)
                locals.add(token)
                
                token = tokens.pop(0)
                if token != ')':
                    print("SyntaxError: Expected ) at the end of function locals")
                    return None
                elif tokens:
                    token = tokens.pop(0)
                    if(token == '('):
                        self.parse_function_signature(token, tokens)
                    else:
                        break
                else:
                    print("SyntaxError: Unexpected EOF at function locals")
                    
            elif tokens[0] == 'result':  #TODO: Single result check
                tokens.pop(0)
                # TODO: Validation: Existance + Type
                token = tokens.pop(0)
                result = token  # TODO: K-V Pair
                
                token = tokens.pop(0)
                if token != ')':
                    print("SyntaxError: Expected ) at the end of function result")
                    return None
                elif tokens:
                    token = tokens.pop(0)
                    if(token == '('):
                        self.parse_function_signature(token, tokens)     # TODO : Single result?
                    else:
                        break
                else:
                    print("SyntaxError: Unexpected EOF at function result")
                    
            else:
                print("SyntaxError: Function signature not defined correctly")
                return None
                
        
        print('End of parse_function_signature Token : "' + token + '" ')
        
        if token not in self.WASM_INSTRUCTIONS:
            print(f"SyntaxError: Unknown instruction '{token}'")
            return None
        
        self.parse_function_instructions(token, tokens)
    
    
    def parse_function_instructions(self, instruction, tokens):

        params = self.WASM_INSTRUCTIONS[instruction]

        if params == 0:
            print(f"Valid instruction '{instruction}' with 0 parameters")
            # Validate remaining tokens recursively
            if tokens and tokens[0] not in ('(', ')'):
                self._validate_instruction(tokens.pop(0), tokens)
            return instruction
        
        

        
