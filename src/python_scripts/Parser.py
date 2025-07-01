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
                
                if tokens:
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

                if token[0] == '$':
                    print('Token as variable name in param : ' + token)
                    params[token] = 'i32'   # TODO : Wait for further types support
                    
                    if tokens:
                        token = tokens.pop(0)
                        if(token == 'i32'):
                            
                            if tokens:
                                token = tokens.pop(0)
                                
                            else:
                                print("SyntaxError: Unexpected EOF at function params")
                                return None
                            
                        else:
                            print("TypeError: i32 waited at function params")
                    else:
                        print("SyntaxError: Unexpected EOF at function params")
                        return None
                else:
                    index = 0;
                    while tokens:
                        token = tokens.pop(0)
                        if token == 'i32':
                            params[index] = 'i32'
                        elif token == ')':
                            break
                        else:
                            print("SyntaxError: Unexpected Symbol at function params")
                #params.add(token)
                
                
                if token != ')':
                    print("SyntaxError: Expected ) at the end of function params")
                    return None
                
                if tokens:
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
                
                if tokens:
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
                
                if tokens:
                    token = tokens.pop(0)
                    if(token == '('):
                        self.parse_function_signature(token, tokens)     # TODO : Single result?
                    else:
                        break
                else:
                    print("SyntaxError: Unexpected EOF at function result")
                    
            else:
                return None
                print("SyntaxError: Function signature not defined correctly : " + tokens[0])
                
        
        print('End of parse_function_signature Token : "' + token + '" ')
        
        if token not in self.WASM_INSTRUCTIONS:
            print(f"SyntaxError: Unknown instruction '{token}'")
            return None
        
        return self.parse_function_instructions(token, tokens)
    
    
    def parse_function_instructions(self, instruction, tokens):

        params = self.WASM_INSTRUCTIONS[instruction]

        if params == 0:
            print(f"Valid instruction '{instruction}' with 0 parameters")
            # Validate remaining tokens recursively
            if tokens and tokens[0] not in ('(', ')'):
                self._validate_instruction(tokens.pop(0), tokens)
            return instruction
        
        elif params == 1:
            if tokens and tokens[0] not in ('(', ')'):
                
                # param
                token = tokens.pop(0)   
                # self._validate_instruction(tokens.pop(0), tokens)
                
                if tokens and tokens[0]:
                    token = tokens.pop(0)
                    
                    if token == ')':
                        print("End of function body")
                    elif token == '(':
                        print("Not implemented yet")
                    elif token in self.WASM_INSTRUCTIONS:
                        return [instruction, token] + [self.parse_function_instructions(token, tokens)]
                    else:    
                        print(f"SyntaxError: Unknown instruction '{token}'")
                        return None
                        
                
            else:
                print(f"SyntaxError : Instruction '{instruction}' requires 1 parameter")
                return None
        
        elif isinstance(params, tuple):
            
            # Range of parameters (min, max)
            min_p, max_p = params
            params_list = []
            while len(params_list) < max_p and tokens and tokens[0] not in ('(', ')'):
                params_list.append(tokens.pop(0))
                
            print(f"[instruction '{instruction}' + params_list '{params_list}' ")
            
            return [instruction] + params_list + self.parse_function_instructions(token, tokens)
        elif params == 'var':
            
            return [instruction] + self.parse_function_instructions(token, tokens)
            
        else:
            print(f"ValueError : Invalid parameter specification for instruction {instruction}")
            return None

