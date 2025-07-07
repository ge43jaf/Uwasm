from Lexer import (
    LPAREN, RPAREN, ID, TYPE, CONST, STRING, EOF,
    Module, Func, Param, Result, Local, Export, Memory, Instruction,
    _i32_const, 
    _i32_add, 
    _local_get, 
    _local_set,
    _global_get, 
    _global_set, 
    _call,
    _return
)

class Parser:
    def __init__(self):
        self.current_token = None
        self.token_index = 0
        self.tokens = []
        
    
    def next_token(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None
        return self.current_token
        
    def parse(self, tokens):
        if not tokens:
            print("Error: No tokens to parse")
            return None
            
        self.tokens = tokens
        self.current_token = self.tokens[0]
        return self.parse_module()
    
    
    
    def parse_module(self):
        if not isinstance(self.current_token, LPAREN):
            print("Expected '(' at start of module")
            return None
        
        self.next_token()
        if not isinstance(self.current_token, Module):
            print("Expected 'module' keyword")
            return None
        
        module = Module(funcs=[])
        self.next_token()
        
        while not isinstance(self.current_token, RPAREN):
            if self.current_token is None:
                print("Unexpected EOF while parsing module")
                return None
            
            if isinstance(self.current_token, LPAREN):
                self.next_token()
                if isinstance(self.current_token, Func):
                    func = self.parse_func()
                    if func is None:
                        return None
                    module.funcs.append(func)
                elif isinstance(self.current_token, Export):
                    if not self.parse_export():
                        return None
                elif isinstance(self.current_token, Memory):
                    if not self.parse_memory():
                        return None
                else:
                    print(f"Unexpected token in module: {self.current_token}")
                    return None
                
                if not isinstance(self.current_token, RPAREN):
                    print("Expected ')' after module element")
                    return None
                self.next_token()
            else:
                print(f"Unexpected token in module: {self.current_token}")
                return None
        
        self.next_token()
        return module
    
    def parse_func(self):
        func = Func()
        self.next_token()
        
        if isinstance(self.current_token, ID):
            func.name = self.current_token.value
            self.next_token()
        
        # (...) (...) (...)
        while not isinstance(self.current_token, RPAREN):
            if not isinstance(self.current_token, LPAREN):
                print(f"Unexpected token in func: {self.current_token}")
                return None
            
            self.next_token()
            if isinstance(self.current_token, Param):
                param = self.parse_param()
                if param is None:
                    return None
                func.params.append(param)
            elif isinstance(self.current_token, Result):
                result = self.parse_result()
                if result is None:
                    return None
                func.results.append(result)
            elif isinstance(self.current_token, Local):
                local = self.parse_local()
                if local is None:
                    return None
                func.locals.append(local)
            else:
                instr = self.parse_instruction()
                if instr is None:
                    return None
                func.body.append(instr)
            
            if not isinstance(self.current_token, RPAREN):
                print("Expected ')' after func element")
                return None
            self.next_token()
        
        return func
    
    def parse_param(self):
        param = Param()
        self.next_token()
        
        if isinstance(self.current_token, ID):
            param.name = self.current_token.value
            self.next_token()
        
        if isinstance(self.current_token, TYPE):
            param.type = self.current_token.value
            self.next_token()
        else:
            print("Expected parameter type")
            return None
        
        return param
    
    def parse_local(self):
        local = Local()
        self.next_token()
        
        if isinstance(self.current_token, ID):
            local.name = self.current_token.value
            self.next_token()
        
        if isinstance(self.current_token, ID):
            local.type = self.current_token.value
            self.next_token()
        else:
            print("Expected local type")
            return None
        
        return local
    
    def parse_result(self):
        self.next_token()
        
        if isinstance(self.current_token, TYPE):
            result_type = self.current_token.value
            self.next_token()
            return result_type
        else:
            print("Expected result type")
            return None
    
    def parse_instruction(self):
        if isinstance(self.current_token, (_i32_const,
                                            _i32_add, 
                                                            # TODO: wait for using WASM_INSTRUCTIONS directly
                                            _local_get, 
                                            _local_set,
                                            _global_get,
                                            _global_set, 
                                            _call, 
                                            _return)):
            op = type(self.current_token).__name__[1:].replace('_', '.')
            self.next_token()
            
            operands = []
            while not isinstance(self.current_token, RPAREN):
                if isinstance(self.current_token, (CONST, ID)):
                    operands.append(self.current_token.value)
                    self.next_token()
                elif isinstance(self.current_token, LPAREN):
                    self.next_token()
                    nested_instr = self.parse_instruction()
                    if nested_instr is None:
                        return None
                    operands.append(nested_instr)
                    if not isinstance(self.current_token, RPAREN):
                        print("Expected ')' after nested instruction")
                        return None
                    self.next_token()
                else:
                    print(f"Unexpected token in instruction: {self.current_token}")
                    return None
            
            return Instruction(op, operands)
        else:
            print(f"Unknown instruction: {self.current_token}")
            return None
    
    def parse_export(self):
        self.next_token()
        # Simplified export parsing
        while not isinstance(self.current_token, RPAREN):
            self.next_token()
        self.next_token()
        return True
    
    def parse_memory(self):
        self.next_token()
        # Simplified memory parsing
        while not isinstance(self.current_token, RPAREN):
            self.next_token()
        self.next_token()
        return True
