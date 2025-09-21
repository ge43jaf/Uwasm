
from Lexer import (
    LPAREN, RPAREN, ID, TYPE, CONST, STRING, EOF, NEWLINE, SPACE,
    Module, Func, Param, Result, Local, Export, Memory, Global,
    Instruction, ControlFlowInstruction, BinaryInstruction,
    _i32_const, 
    _i32_add, 
    _i32_sub,
    _i32_mul,
    _i32_div_s,
    _i32_ge_u,
    _i32_gt_s,
    _i32_lt_s,
    _i32_lt_u,
    
    _i32_clz,
    
    _local_get, 
    _local_set,
    _local_tee,
    _global_get, 
    _global_set, 
    
    _call,
    _return,
    _nop,
    _block,
    _loop,
    _br,
    _br_if,
    _if,
    _then,
    _else,
    _end,
    
    _i32_load,
    _i32_store
    
)

COLORS = {
        
    'ERROR_COLOR': '\033[1;31m',   # Error messages - Bold Red
    'WARNING_COLOR': '\033[1;33m', # Warning messages - Bold Yellow  
    'SUCCESS_COLOR': '\033[1;32m', # Success messages - Bold Green
    'PARSER_DEBUG_COLOR': '\033[1;34m',    # Parser debug messages - Bold Blue
    'DEBUG_COLOR': '\033[36m', # Debug messages - Cyan (no bold)
    'HIGHLIGHT_COLOR': '\033[7;37m',   # Highlighted text - Reverse video (white on default background)
    'RESET_COLOR': '\033[0m',  # Reset all styles and colors
}

class Parser:
    def __init__(self):
        self.current_token = None
        self.token_index = 0
        self.tokens = []
        self.module = None
        # self.funcs = []
        self.line_number = 1
        self.par_verb_flag = False
        self.par_col_flag = False
        
    def next_token(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Parser index Error")
            self.current_token = None
        return self.current_token
    
    def previous_token(self):
        self.token_index -= 1
        if self.token_index >= 0:
            self.current_token = self.tokens[self.token_index]
        else:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Parser index Error")
            self.current_token = None
        return self.current_token
        
    def parse(self, tokens):
        
        if not tokens:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Error: No tokens to parse")
            return None
            
        self.tokens = tokens
        self.current_token = self.tokens[0]
        return self.parse_module()
    
    def parse_newline_and_space(self):
        while isinstance(self.current_token, NEWLINE) or isinstance(self.current_token, SPACE):
            if isinstance(self.current_token, NEWLINE):
                self.line_number += 1
            self.next_token()
    
    def reverse_parse_newline_and_space(self):
        while isinstance(self.current_token, NEWLINE) or isinstance(self.current_token, SPACE):
            if isinstance(self.current_token, NEWLINE):
                self.line_number -= 1
            self.previous_token()
            
    def parse_module(self):
        self.parse_newline_and_space()
        
        if self.current_token is None or isinstance(self.current_token, EOF):
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f'Line {self.line_number}: Unexpected token "EOF", expected a module field or a module')
                return None
                
        if not isinstance(self.current_token, LPAREN):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected '(' at start of module")
            return None
        
        self.next_token()
        self.parse_newline_and_space()
            
        if not isinstance(self.current_token, Module):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected 'module' keyword")
            return None
        
        self.module = Module(mems=[], funcs=[], exports=[])
        self.next_token()
        self.parse_newline_and_space()
                
        while not isinstance(self.current_token, RPAREN):
            
            if self.current_token is None:
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Unexpected EOF while parsing module")
                return None
            
            if isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                
                if isinstance(self.current_token, Func):        # Can only be surrounded by (...)
                    func = self.parse_func()
                    if func is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing function, current token : '{self.current_token}'")
                        
                        return None
                    self.module.funcs.append(func)
                elif isinstance(self.current_token, Export):    # Can only be surrounded by (...)
                    export = self.parse_export()
                    if export is None :
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing export, current token : '{self.current_token}'")
                        return None

                    self.module.exports.append(export)
                    # print(f"test_export : {export}")

                elif isinstance(self.current_token, Memory):    # Can only be surrounded by (...)

                    mem = self.parse_memory()
                    if mem is None :
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing memory, current token : '{self.current_token}'")
                        return None
                    self.module.mems.append(mem)
                    # print(f"test_mem : {mem}")

                # TODO : before or after function definition?
                elif isinstance(self.current_token, Global):    # Can only be surrounded by (...)

                    glob = self.parse_global()
                    if glob is None :   #TODO: Error message
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing global, current token : '{self.current_token}'")
                        return None
                    self.module.globs.append(glob)
                    # print(f"test_mem : {mem}")
                    
                
                else:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token in module: {self.current_token} after (")
                    return None
                
                self.parse_newline_and_space()
                
                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after module element")
                    return None
                self.next_token()
                self.parse_newline_and_space()
                
            else:
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Unexpected token in module: {self.current_token}")
                return None
        
        self.next_token()
        self.parse_newline_and_space()
        # TODO : indentation for if?
        if (not self.current_token is None) and (not isinstance(self.current_token, EOF)):
                # print("Type: " + str(type(self.current_token)))
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f'Line {self.line_number}: Unexpected token {self.current_token} after module')
                return None
        return self.module
    
    def parse_func(self):
        func = Func()
        self.next_token()
        self.parse_newline_and_space()
                
        if isinstance(self.current_token, ID):
            func.name = self.current_token.value
            self.next_token()
            self.parse_newline_and_space()
        # TODO: Parse params ... first, then instructions check
        current_section = None
        
        export_flag = False
        param_flag = False
        result_flag = False
        local_flag = False
        
        # # (...) (...) (...)
        # while not isinstance(self.current_token, RPAREN):
        #     # if not isinstance(self.current_token, LPAREN):
        #     #     print(f"Unexpected token in func: {self.current_token}")
        #     #     return None
        #     # while isinstance(self.current_token, NEWLINE) or isinstance(self.current_token, SPACE):
        #     #     if isinstance(self.current_token, NEWLINE):
        #     #         self.line_number += 1
        #     #     self.next_token()
                
        #     if isinstance(self.current_token, LPAREN):
        #         self.next_token()
        #         self.parse_newline_and_space()
                    
        #         if isinstance(self.current_token, Export):  
        #             self.next_token()
        #             self.parse_newline_and_space()
                    
        #             if not isinstance(self.current_token, STRING):
        #                 print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
        #                 print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected export name to be a string in function signature")
        #                 return None
        #             print(f"export_name : {self.current_token}")
        #             if self.current_token.value not in func.export_names:
        #                 func.export_names.append(self.current_token.value)
        #             else:
        #                 print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
        #                 print(f"Line {self.line_number}: Duplicate export '{self.current_token}'")
        #                 return None
        #             self.next_token()
        #             self.parse_newline_and_space()
                
        #         elif isinstance(self.current_token, Param):
        #             if current_section and current_section != 'param':
        #                 print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
        #                 print(f"Line {self.line_number}: Error: Params must come before results and locals")
        #                 return None
        #             current_section = 'param'
        #             params_returned = self.parse_param()
        #             if params_returned is None:
        #                 print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
        #                 print(f"Line {self.line_number}: None returned after parsing parameters, current token : '{self.current_token}'")
                        
        #                 return None
        #             func.params.extend(params_returned)
                    
        #         elif isinstance(self.current_token, Result):
        #             if current_section and current_section not in ('param', 'result'):
        #                 print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ") 
        #                 print(f"Line {self.line_number}: Error: Results must come after params and before locals")
        #                 return None
        #             current_section = 'result'
        #             result = self.parse_result()
        #             if result is None:
        #                 print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
        #                 print(f"Line {self.line_number}: None returned after parsing result, current token : '{self.current_token}'")
                        
        #                 return None
        #             func.results.append(result)
                    
        #         elif isinstance(self.current_token, Local):
        #             current_section = 'local'
        #             local = self.parse_local()
        #             if local is None:
        #                 print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
        #                 print(f"Line {self.line_number}: None returned after parsing local, current token : '{self.current_token}'")
                        
        #                 return None
        #             func.locals.append(local)
                    
        #         elif isinstance(self.current_token, ControlFlowInstruction):
        #             # TODO: Deletion
        #             print(self._par_colorize(f"Line {self.line_number}: ", 'PARSER_DEBUG_COLOR'), end="     ")
                    
        #             print('ControlFlowInstruction :  ' + str(type(self.current_token)))
                
        #             controlFlowInstr = self.parse_control_flow()
        #             if controlFlowInstr is None:
        #                 print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
        #                 print(f"Line {self.line_number}: No valid control flow instruction")
        #                 print(self.current_token)
        #                 print(self.next_token)
        #                 return None
        #             func.body.append(controlFlowInstr)
                    
        #         elif isinstance(self.current_token, Instruction):
        #             if self.par_verb_flag:
        #                 print(self._par_colorize(f"Line {self.line_number}: ", 'DEBUG_COLOR'), end="     ")
                        
        #                 print('func (...) (...) (... ' + str(type(self.current_token))) #TODO: MOdification
        #             instr = self.parse_instruction()
        #             if instr is None:
        #                 print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
        #                 print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
        #                 return None
        #             func.body.append(instr)
                    
        #         else:
        #             print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
        #             print(f"Line {self.line_number}: Instruction {self.current_token} in function {func.name} not found!")
        #             # break
        #             return None
                
        #         self.parse_newline_and_space()

        #         # Check closing parenthesis for this if branch
        #         if not isinstance(self.current_token, RPAREN):
        #             print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
        #             print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after func element")      # TODO : param i32 i32
        #             print(self.current_token)
        #             print(self.next_token)
        #             return None
        #         self.next_token()
        #         self.parse_newline_and_space()
                    
            
            
                # (...) (...) (...)
        # while not isinstance(self.current_token, RPAREN):
            # if not isinstance(self.current_token, LPAREN):
            #     print(f"Unexpected token in func: {self.current_token}")
            #     return None
            # while isinstance(self.current_token, NEWLINE) or isinstance(self.current_token, SPACE):
            #     if isinstance(self.current_token, NEWLINE):
            #         self.line_number += 1
            #     self.next_token()
              
        while isinstance(self.current_token, LPAREN):
            self.next_token()
            self.parse_newline_and_space()
            print("Enter Export")        
            if isinstance(self.current_token, Export):  
                self.next_token()
                self.parse_newline_and_space()
                    
                if not isinstance(self.current_token, STRING):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected export name to be a string in function signature")
                    return None
                print(f"export_name : {self.current_token}")
                if self.current_token.value not in func.export_names:
                    func.export_names.append(self.current_token.value)
                else:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Duplicate export '{self.current_token}'")
                    return None
                self.next_token()
                self.parse_newline_and_space()
                
                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after func export")      # TODO : param i32 i32
                
                self.next_token()
                self.parse_newline_and_space()
                
            else:
                self.previous_token()
                self.reverse_parse_newline_and_space()
                break
                
        
        while isinstance(self.current_token, LPAREN):
            self.next_token()
            self.parse_newline_and_space()
            print("Enter Param")        
            if isinstance(self.current_token, Param):  
                if current_section and current_section != 'param':
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Error: Params must come before results and locals")
                    return None
                current_section = 'param'
                params_returned = self.parse_param()
                if params_returned is None:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: None returned after parsing parameters, current token : '{self.current_token}'")
                        
                    return None
                func.params.extend(params_returned)
                
                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after func export")      # TODO : param i32 i32
                
                self.next_token()
                self.parse_newline_and_space()
                
            else:
                self.previous_token()
                self.reverse_parse_newline_and_space()
                break    
                
                
        while isinstance(self.current_token, LPAREN):
            self.next_token()
            self.parse_newline_and_space()
            print("Enter Result")        
            if isinstance(self.current_token, Result):  
                if current_section and current_section not in ('param', 'result'):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ") 
                    print(f"Line {self.line_number}: Error: Results must come after params and before locals")
                    return None
                current_section = 'result'
                results = self.parse_result()
                if results is None:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: None returned after parsing result, current token : '{self.current_token}'")
                    
                    return None
                func.results.extend(results)
                
                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after func export")      # TODO : param i32 i32
                
                self.next_token()
                self.parse_newline_and_space()
                
            else:
                self.previous_token()
                self.reverse_parse_newline_and_space()
                break            
                
        while isinstance(self.current_token, LPAREN):
            self.next_token()
            self.parse_newline_and_space()
            print("Enter Local")        
            if isinstance(self.current_token, Local):  
                current_section = 'local'
                locals = self.parse_local()
                if locals is None:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: None returned after parsing local, current token : '{self.current_token}'")
                        
                    return None
                print(locals)
                func.locals.extend(locals)
                
                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after func export")      # TODO : param i32 i32
                
                self.next_token()
                self.parse_newline_and_space()
                
            else:
                self.previous_token()
                self.reverse_parse_newline_and_space()
                break     
                
        print(f"Entering instruction fields : {self.current_token}")        
        while not isinstance(self.current_token, RPAREN):
            print(f"Line {self.line_number}: Inside instruction fields: {self.current_token}")
                        
                   
                
            if isinstance(self.current_token, LPAREN):    
                self.next_token()
                self.parse_newline_and_space()
                 
                if isinstance(self.current_token, ControlFlowInstruction):
                    # TODO: Deletion
                    print(self._par_colorize(f"Line {self.line_number}: ", 'PARSER_DEBUG_COLOR'), end="     ")
                    
                    print('ControlFlowInstruction :  ' + str(type(self.current_token)))
                
                    controlFlowInstr = self.parse_control_flow()
                    if controlFlowInstr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: No valid control flow instruction")
                        print(self.current_token)
                        print(self.next_token)
                        return None
                    func.body.append(controlFlowInstr)
                    
                elif isinstance(self.current_token, Instruction):
                    if self.par_verb_flag:
                        print(self._par_colorize(f"Line {self.line_number}: ", 'DEBUG_COLOR'), end="     ")
                        
                        print('func (...) (...) (... ' + str(type(self.current_token))) #TODO: MOdification
                    instr = self.parse_instruction(imm_instr = False)
                    if instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    func.body.append(instr)
                    
                else:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Instruction {self.current_token} in function {func.name} not found!")
                    # break
                    return None
                
                # print(f"After instruction : {self.current_token}")
                # # self.parse_newline_and_space()
                # print(f"After instruction and parsing new line and space : {self.current_token}")

                # Check closing parenthesis for this if branch
                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after func element")      # TODO : param i32 i32
                    print(self.current_token)
                    print(self.next_token)
                    return None
                # self.next_token()
                # self.parse_newline_and_space()
                
            
            
            elif isinstance(self.current_token, ControlFlowInstruction):
                #TODO: MOdification/Deletion
                print(self._par_colorize(f"Line {self.line_number}: ", 'DEBUG_COLOR'), end="     ")
                
                print('ControlFlowInstruction without (...):  ' + str(type(self.current_token)))

                controlFlowInstr = self.parse_control_flow()
                if controlFlowInstr is None:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: No valid control flow instruction")
                    print(self.current_token)
                    print(self.next_token)
                    return None
                func.body.append(controlFlowInstr)
                
                # if isinstance(self.current_token, _nop):
                #     self.next_token()
                #     while isinstance(self.current_token, NEWLINE) or isinstance(self.current_token, SPACE):
                #         if isinstance(self.current_token, NEWLINE):
                #             self.line_number += 1
                #         self.next_token()
                #     continue
                # elif isinstance(self.current_token, _block):
                #     block = self.parse_block()
                #     #TODO : IMplementation, etc.
                #     break
                # elif isinstance(self.current_token, _loop):
                #     loop = self.parse_loop()
                #     break
                # elif isinstance(self.current_token, _br):
                #     break
                # elif isinstance(self.current_token, _br_if):
                #     self.parse_br_if()
                #     break
                # elif isinstance(self.current_token, _if):
                #     self.parse_if()
                #     break
                # elif isinstance(self.current_token, _call):
                    
                #     break
                # elif isinstance(self.current_token, _return):
                #     break
                # else:
                #     print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")     
                #     print(f"Line {self.line_number}: Is ControlFlowInstruction {self.current_token} but not found!")
                #     break
                
            elif isinstance(self.current_token, Instruction):
                # print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                # print(f'Line {self.line_number}: Currrent Instruction without (...) surrounded' + str(type(self.current_token)))
                
                if self.par_verb_flag:
                    print(self._par_colorize(f"Line {self.line_number}: ", 'DEBUG_COLOR'), end="     ")
                    
                    print('func (...) (...) (... ' + str(type(self.current_token))) #TODO: MOdification
                instr = self.parse_instruction(imm_instr = True)
                if instr is None:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                    return None
                
                print(f"After instr : {self.current_token}")

                func.body.append(instr)
                    
                # self.next_token()
                # while isinstance(self.current_token, NEWLINE) or isinstance(self.current_token, SPACE):
                #     if isinstance(self.current_token, NEWLINE):
                #         self.line_number += 1
                #     self.next_token()
                # continue
            else:
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Instruction {self.current_token} in function {func.name} not found!")
                # break
                return None
            
            print(f"After instruction : {self.current_token}")
            print(f"After instruction and parsing new line and space : {self.current_token}")

            self.next_token()
            self.parse_newline_and_space()
            
        self.next_token()
        self.parse_newline_and_space()    
        # TODO: Error?
        print(f'Line {self.line_number}: After looping: ' + str(self.current_token))
        if not isinstance(self.current_token, RPAREN):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after all func elements")
            return None
            
        return func
    
    def parse_param(self):
        param = Param()
        params = []
        self.next_token()
        self.parse_newline_and_space()
        
        if isinstance(self.current_token, ID):
            param.name = self.current_token.value
            self.next_token()
            self.parse_newline_and_space()
                
            if isinstance(self.current_token, TYPE):
                param.type = self.current_token.value
                params.append(param)
                self.next_token()
                self.parse_newline_and_space()
            else:
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected parameter type for ID")
                return None
            
            return params
        
        if isinstance(self.current_token, TYPE):
            param.type = self.current_token.value
            params.append(param)
            self.next_token()
            self.parse_newline_and_space()
            
            while not isinstance(self.current_token, RPAREN):
                self.parse_newline_and_space()
                if isinstance(self.current_token, TYPE):
                    param_temp = Param()
                    param_temp.type = self.current_token.value
                    params.append(param_temp)
                    self.next_token()
                    self.parse_newline_and_space()
                    
                else:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected parameter type")
                    return None
        else:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected parameter type")
            return None
        
        return params
    
    def parse_local(self):
        local = Local()
        locals = []
        self.next_token()
        self.parse_newline_and_space()
        
        if isinstance(self.current_token, ID):
            local.name = self.current_token.value
            self.next_token()
            self.parse_newline_and_space()
            
            if isinstance(self.current_token, TYPE):
                local.type = self.current_token.value
                locals.append(local)
                self.next_token()
                self.parse_newline_and_space()
            
            else:
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected local type")
                return None
        
            return locals
        
        if isinstance(self.current_token, TYPE):
            local.type = self.current_token.value
            locals.append(local)
            self.next_token()
            self.parse_newline_and_space()
            
            while not isinstance(self.current_token, RPAREN):
                self.parse_newline_and_space()
                if isinstance(self.current_token, TYPE):
                    local_temp = Local()
                    local_temp.type = self.current_token.value
                    locals.append(local_temp)
                    self.next_token()
                    self.parse_newline_and_space()
                    
                else:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected local type")
                    return None
        else:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected local type")
            return None
        
        return locals
    
    
    def parse_result(self):
        self.next_token()
        self.parse_newline_and_space()
        result_types = []
        while isinstance(self.current_token, TYPE):
            result_types.append(self.current_token.value)
            self.next_token()
            self.parse_newline_and_space()
        
        if not isinstance(self.current_token, RPAREN): 

            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}' after result types, expected ')'")
            return None
        
        return result_types
    
    def parse_control_flow(self):
        
        print(self._par_colorize(f"Line {self.line_number}: ", 'PARSER_DEBUG_COLOR'), end="     ")
                
        print('ControlFlowInstruction inside parse_control_flow:  ' + str(type(self.current_token)))

        if isinstance(self.current_token, _nop):
            self.next_token()
            self.parse_newline_and_space()
            # return ControlFlowInstruction(_nop)
            return _nop
        
        elif isinstance(self.current_token, _block):
            op_block = self.current_token
            
            self.next_token()
            self.parse_newline_and_space()
            
            return self.parse_block(op_block)
            
        elif isinstance(self.current_token, _loop):
            op_loop = self.current_token
            
            self.next_token()
            self.parse_newline_and_space()
            
            return self.parse_loop(op_loop)

        elif isinstance(self.current_token, _br):
            op_br = self.current_token
            
            self.next_token()
            self.parse_newline_and_space()
            
            return self.parse_br(op_br)

        elif isinstance(self.current_token, _br_if):
            op_br_if = self.current_token
            
            self.next_token()
            self.parse_newline_and_space()
            
            return self.parse_br_if(op_br_if)
        
        elif isinstance(self.current_token, _if):
            op_if = self.current_token
            
            self.next_token()
            self.parse_newline_and_space()
            
            return self.parse_if(op_if)
            
        elif isinstance(self.current_token, _call):
            op_call = self.current_token
            
            self.next_token()
            self.parse_newline_and_space()
            
            operand = self.current_token
            if not isinstance(self.current_token, (CONST, ID)):
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected CONST or ID after call instruction")
                return None
            self.next_token()
            self.parse_newline_and_space()
            
            op_call.operands = {operand}
            return op_call
            # return ControlFlowInstruction(_call, {operand})
        
        elif isinstance(self.current_token, _return):
            # No operands needed, just consume any values on stack
            op_return = self.current_token
            
            self.next_token()
            self.parse_newline_and_space()
            op_return.operands = []
            # return ControlFlowInstruction(_return)
            return _return()
        
        else:
            op = self.current_token
            
            print(self._par_colorize("WARNING: ", 'WARNING_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Is ControlFlowInstruction {op} but not found!")
            self.next_token()
            self.parse_newline_and_space()
            
            # pass
            # return ControlFlowInstruction(op)
            return op
    
    # def parse_call(self):
        
    def parse_block(self, op_block: _block):

        operands = []
        # Parse operands/instructions until closing parenthesis
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                
                if isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction(imm_str=False)
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                else:
                    #TODO
                    print('(...) Other options in parse_block???')

                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after nested instruction")
                    return None
                self.next_token()
                self.parse_newline_and_space()
                
            else:
                # Handle immediate values
                if isinstance(self.current_token, (CONST, ID)):
                    operands.append(self.current_token.value)
                    self.next_token()
                    self.parse_newline_and_space()
                    
                elif isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction(imm_instr = True)
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                else:   #TODO
                    print('Other options in parse_block???')
                    break
        # return ControlFlowInstruction(_block, operands)    
        op_block.operands = operands
        return op_block


    def parse_loop(self, op_loop: _loop):
        
        operands = []
        
        if isinstance(self.current_token, (CONST, ID)):
            op_loop.name = self.current_token.value
            self.next_token()
            self.parse_newline_and_space()
            
        # Parse operands/instructions until closing parenthesis
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                
                if isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction(imm_instr = False)
                    print("nested_instr inside parse_loop : " + str(nested_instr))
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                else:   #TODO
                    print('(...) Other options in parse_loop???')

                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after nested instruction")
                    return None
                self.next_token()
                self.parse_newline_and_space()
                
            else:   #TODO
                if self.par_verb_flag:
                    print(self._par_colorize(f"Line {self.line_number}: ", 'DEBUG_COLOR'), end="     ")
                    
                    print(f'else in parse_loop, current_token : {self.current_token}')

                # Handle immediate values
                # if self.par_verb_flag:
                    print("Inside parse loop: " + str(type(self.current_token)))
                # if self.current_token == "end":
                if isinstance(self.current_token, _end):
                    print(self._par_colorize(f"Line {self.line_number}: ", 'DEBUG_COLOR'), end="     ")
                    print("_end for _loop")
                    self.next_token()   # To avoid the warning "Is ControlFlowInstruction ... but not found!"
                    self.parse_newline_and_space()
                    
                    # return ControlFlowInstruction(_loop, operands)
                    op_loop.operands = operands
                    print("op_loop.operands : " + str(op_loop.operands))
                    
                    return op_loop
                
                if isinstance(self.current_token, (CONST, ID)):
                    operands.append(self.current_token.value)
                    self.next_token()
                    self.parse_newline_and_space()
                    
                elif isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    print(f'Line {self.line_number}: nested control flow in parse_loop : {nested_instr}')   #TODO
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction(imm_instr = True)
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                else:   #TODO
                    print('Other options/operations/class of instrustions in parse_loop???')
                    break
        # return ControlFlowInstruction(_loop, operands)  
        
        op_loop.operands = operands
        print("op_loop.operands : " + str(op_loop.operands))
        return op_loop

    def parse_br(self, op_br: _br):
        # Parse function index or name
        if isinstance(self.current_token, (CONST, ID)):
            operand = self.current_token
            self.next_token()
            self.parse_newline_and_space()
            
            # return ControlFlowInstruction(_br, {operand})
            op_br.operands = {operand}
            return op_br
        
        else:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected function index/name for br")
            return None

    # def parse_br_if(self):
    #     pass
    
    def parse_br_if(self, op_br_if: _br_if):
        operands = []
        
        # Parse the branch target (label index/name)
        if isinstance(self.current_token, (CONST, ID)):
            target = self.current_token.value
            operands.append(target)
            self.next_token()
            self.parse_newline_and_space()
            
        else:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected branch target (label index/name) for br_if")
            return None

        # Parse condition and other nested instructions (similar to parse_loop/parse_if)
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                
                # Parse nested instruction
                if isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction(imm_instr = False)
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                else:
                    # Handle other cases like immediate values
                    if isinstance(self.current_token, (CONST, ID)):
                        operands.append(self.current_token.value)
                        self.next_token()
                    else:
                        print(f'Line {self.line_number}: Unexpected token in br_if: {self.current_token}')
                        return None

                # Expect closing parenthesis
                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after nested instruction in br_if")
                    return None
                
                self.next_token()
                self.parse_newline_and_space()
                    
            else:
                # Handle immediate values outside parentheses
                if isinstance(self.current_token, (CONST, ID)):
                    operands.append(self.current_token.value)
                    self.next_token()
                    self.parse_newline_and_space()
                    
                elif isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction(imm_instr = True)
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                else:
                    # End of br_if instruction or unexpected token
                    break

        # return ControlFlowInstruction(_br_if, operands)
        op_br_if.operands = operands
        return op_br_if
    
    def parse_if(self, op_if: _if):
        
        operands = []
        
        if isinstance(self.current_token, (CONST, ID)):
            op_if.name = self.current_token.value
            self.next_token()
            self.parse_newline_and_space()
        
        # Parse operands/instructions until closing parenthesis
        while not isinstance(self.current_token, RPAREN)   \
            and not isinstance(self.current_token, _else)  \
            and not isinstance(self.current_token, _end):
            
            if isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                
                if isinstance(self.current_token, _then):
                    op_then = self.current_token
                    
                    self.next_token()
                    self.parse_newline_and_space()
                    
                    then_instr = self.parse_then(op_then)
                    
                    operands.append(then_instr)
                    
                if isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction(imm_instr = False)
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                else:   #TODO
                    print('(...) Other options in parse_block???')

                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ") 
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after nested instruction")
                    return None
                self.next_token()
                self.parse_newline_and_space()
                
            else:
                # Handle immediate values
                
                if self.par_verb_flag:
                    print(self._par_colorize(f"Line {self.line_number}: ", 'DEBUG_COLOR'), end="     ")
                    
                    print("Inside parse if: " + str(type(self.current_token)))
                # if self.current_token == "end":
                if isinstance(self.current_token, _end):
                    print(self._par_colorize(f"Line {self.line_number}: ", 'DEBUG_COLOR'), end="     ")
                    print("_end for _if")
                    self.next_token()   # To avoid the warning "Is ControlFlowInstruction ... but not found!"
                    self.parse_newline_and_space()
                    
                    # return ControlFlowInstruction(_if, operands)
                    op_if.operands = operands
                    return op_if
                
                if isinstance(self.current_token, (CONST, ID)):
                    operands.append(self.current_token.value)
                    self.next_token()
                    self.parse_newline_and_space()
                    
                elif isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction(imm_instr = True)
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                else:   #TODO
                    print('Other options in parse_block???')
                    break
                
                
        # For 'if' instruction, handle else branch
        if isinstance(self.current_token, LPAREN):
            self.next_token()
            self.parse_newline_and_space()
            if isinstance(self.current_token, _else):
                self.next_token()
                self.parse_newline_and_space()
                
                else_operands = []
                    
                while not isinstance(self.current_token, RPAREN):
                    if isinstance(self.current_token, LPAREN):
                        self.next_token()
                        self.parse_newline_and_space()
                        
                        nested_instr = self.parse_instruction(imm_instr = False)
                        if nested_instr is None:
                            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                            print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                            return None
                        else_operands.append(nested_instr)
                            
                        if not isinstance(self.current_token, RPAREN):
                            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after else instruction")
                            return None
                        self.next_token()
                        self.parse_newline_and_space()
                        
                    else:
                        break
                    
                # return ControlFlowInstruction(_if, {
                #     'then': operands,
                #     'else': else_operands
                # })
                op_if.operands = {
                    'then': operands,
                    'else': else_operands
                }
                return op_if
            
            # return ControlFlowInstruction(_if, {
            #     'then': operands,
            #     'else': []  # Will be filled if there's an else branch
            # })
            op_if.operands = {
                'then': operands,
                'else':[]
            }
            return op_if
        
        elif isinstance(self.current_token, _else):
            self.next_token()
            self.parse_newline_and_space()
                
            else_operands = []
                    
            while not isinstance(self.current_token, RPAREN):
                if isinstance(self.current_token, LPAREN):
                    self.next_token()
                    self.parse_newline_and_space()
                        
                    nested_instr = self.parse_instruction(imm_instr = False)
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    else_operands.append(nested_instr)
                            
                    if not isinstance(self.current_token, RPAREN):
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after else instruction")
                        return None
                    self.next_token()
                    self.parse_newline_and_space()

                else:
                    # Handle immediate values
                
                    if self.par_verb_flag:
                        print(self._par_colorize(f"Line {self.line_number}: ", 'DEBUG_COLOR'), end="     ")
                    
                        print("Inside parse if: " + str(type(self.current_token)))
                    # if self.current_token == "end":
                    if isinstance(self.current_token, _end):
                        print(self._par_colorize(f"Line {self.line_number}: ", 'DEBUG_COLOR'), end="     ")
                        print("_end for _if")
                        self.next_token()   # To avoid the warning "Is ControlFlowInstruction ... but not found!"
                        self.parse_newline_and_space()
                    
                        # return ControlFlowInstruction(_if, operands)
                        op_if.operands = operands
                        return op_if
                
                    if isinstance(self.current_token, (CONST, ID)):
                        operands.append(self.current_token.value)
                        self.next_token()
                        self.parse_newline_and_space()
                    
                    elif isinstance(self.current_token, ControlFlowInstruction):
                        nested_instr = self.parse_control_flow()
                        if nested_instr is None:
                            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                            print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                        
                            return None
                        operands.append(nested_instr)
                    elif isinstance(self.current_token, Instruction):
                        nested_instr = self.parse_instruction(imm_instr = True)
                        if nested_instr is None:
                            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                            print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                            return None
                        operands.append(nested_instr)
                    else:   #TODO
                        print('Other options in parse_block???')
                        break
                    
                    
            op_if.operands = {
                'then': operands,
                'else': else_operands
            }
            return op_if
            
            
        
        
        
        
        # return ControlFlowInstruction(_if, operands)
        op_if.operands = operands
        return op_if
        
    def parse_then(self, op_then: _then):   # TODO : example
        operands = []
        
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                
                # Parse nested instruction
                if isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction(imm_instr = False)
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                else:
                    # Handle other cases like immediate values
                    if isinstance(self.current_token, (CONST, ID)):
                        operands.append(self.current_token.value)
                        self.next_token()
                    else:
                        print(f'Line {self.line_number}: Unexpected token in br_if: {self.current_token}')
                        return None

                # Expect closing parenthesis
                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after nested instruction in br_if")
                    return None
                
                self.next_token()
                self.parse_newline_and_space()
                    
            else:
                # Handle immediate values outside parentheses
                if isinstance(self.current_token, (CONST, ID)):
                    operands.append(self.current_token.value)
                    self.next_token()
                    self.parse_newline_and_space()
                    
                elif isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction(imm_instr = True)
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                else:
                    # End of then instruction or unexpected token
                    break

        # return ControlFlowInstruction(_then, operands)
        op_then.operands = operands
        return op_then
    
    
    def original_parse_control_flow(self):

        # control_flow_instr = ControlFlowInstruction()

        op = type(self.current_token).__name__[1:].replace('_', '.')
        self.next_token()
        self.parse_newline_and_space()
        
        operands = []
        # instructions = []
        
        # 3 ControlFlowInstructions with nested loop possibilities
        if op in ['block', 'loop', 'if']:
            
            # Parse operands/instructions until closing parenthesis
            while not isinstance(self.current_token, RPAREN):
                if isinstance(self.current_token, LPAREN):
                    self.next_token()
                    self.parse_newline_and_space()
                    
                    if isinstance(self.current_token, ControlFlowInstruction):
                        nested_instr = self.parse_control_flow()
                        if nested_instr is None:
                            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                            print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                        
                            return None
                        operands.append(nested_instr)
                    elif isinstance(self.current_token, Instruction):
                        nested_instr = self.parse_instruction()
                        if nested_instr is None:
                            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                            print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                            return None
                        operands.append(nested_instr)
                    else:   #TODO
                        print('Other options in parse_control_flow???')

                    if not isinstance(self.current_token, RPAREN):
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after nested instruction")
                        return None
                    self.next_token()
                    self.parse_newline_and_space()
                    
                else:
                    # Handle immediate values
                    if isinstance(self.current_token, (CONST, ID)):
                        operands.append(self.current_token.value)
                        self.next_token()
                        self.parse_newline_and_space()
                        
                    else:
                        break
            
            # For 'if' instruction, handle else branch
            if op == 'if' and isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                
                if isinstance(self.current_token, _else):
                    self.next_token()
                    self.parse_newline_and_space()
                    
                    else_operands = []
                    
                    while not isinstance(self.current_token, RPAREN):
                        if isinstance(self.current_token, LPAREN):
                            self.next_token()
                            self.parse_newline_and_space()
                            
                            nested_instr = self.parse_instruction()
                            if nested_instr is None:
                                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                                print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                                return None
                            else_operands.append(nested_instr)
                            
                            if not isinstance(self.current_token, RPAREN):
                                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ") 
                                print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after else instruction")
                                return None
                            self.next_token()
                            self.parse_newline_and_space()
                            
                        else:
                            break
                    
                    return ControlFlowInstruction(op, {
                        'then': operands,
                        'else': else_operands
                    })

                return ControlFlowInstruction(op, {
                    'then': operands,
                    'else': []  # Will be filled if there's an else branch
                })
        
        elif op == 'br_if': #TODO:Implementation
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected implementation for br_if parser")
            return None
        
        elif op == 'call':
            # Parse function index or name
            if isinstance(self.current_token, (CONST, ID)):
                operands.append(self.current_token.value)
                self.next_token()
                self.parse_newline_and_space()
                
            else:
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected function index/name for call")
                return None
            
            # Parse call arguments
            while not isinstance(self.current_token, RPAREN):
                if isinstance(self.current_token, LPAREN):
                    self.next_token()
                    self.parse_newline_and_space()
                    
                    nested_instr = self.parse_instruction()
                    if nested_instr is None:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                        return None
                    operands.append(nested_instr)
                    
                    if not isinstance(self.current_token, RPAREN):
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after call argument")
                        return None
                    self.next_token()
                    self.parse_newline_and_space()
                else:
                    break
        
        elif op == 'return':
            # No operands needed, just consume any values on stack
            pass
        
        # Create the instruction
        if op in ['block', 'loop']:
            return ControlFlowInstruction(op, operands)
        # elif op == 'if':
        #     return ControlFlowInstruction(op, {
        #         'then': operands,
        #         'else': []  # Will be filled if there's an else branch
        #     })
        else:
            return ControlFlowInstruction(op, operands) #TODO




    def parse_instruction(self, imm_instr):
        # if isinstance(self.current_token, (_i32_const,
        #                                     _i32_add, 
        #                                                     # TODO: wait for using WASM_INSTRUCTIONS directly
        #                                     _i32_sub,
        #                                     _i32_mul,
        #                                     _i32_div_s,
        #                                     _i32_ge_u,
        #                                     _i32_gt_s,
    
        #                                     _local_get, 
        #                                     _local_set,
        #                                     _local_tee,
        #                                     _global_get, 
        #                                     _global_set, 
                                            
        #                                     _call, 
        #                                     _return)):
        op_class = self.current_token
        op = type(self.current_token).__name__[1:].replace('_', '.', 1)    # 1 for avoiding i32.lt.s
        operands = []
        
        print(self._par_colorize(f"Line {self.line_number}: ", 'PARSER_DEBUG_COLOR'), end="     ")
                
        print('Instruction inside parse_instruction:  ' + str(type(self.current_token)))

        if isinstance(self.current_token, BinaryInstruction):
            self.next_token()
            self.parse_newline_and_space()
            
            # return BinaryInstruction(op, operands)
            op_class.operands = operands
            
            return op_class

        self.next_token()
        self.parse_newline_and_space()
        
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, (CONST, ID)):
                operands.append(self.current_token.value)
                
                if imm_instr:
                    break # TODO: More robust?
                
            elif isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                
                nested_instr = None
                if isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction(imm_instr = False)
                else:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Not an instruction, current token : '{self.current_token}'")
                    
                        
                
                if nested_instr is None:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                        
                    return None
                operands.append(nested_instr)
                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")   
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after nested instruction")
                    return None
            elif isinstance(self.current_token, ControlFlowInstruction):
                nested_instr = self.parse_control_flow()
                if nested_instr is None:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: None returned after parsing control flow, current token : '{self.current_token}'")
                    
                    return None
                operands.append(nested_instr)
            elif isinstance(self.current_token, Instruction):
                nested_instr = self.parse_instruction(imm_instr = True)
                if nested_instr is None:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: None returned after parsing instruction, current token : '{self.current_token}'")
                    
                    return None
                operands.append(nested_instr)
            
            
            
            
            else:
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Unexpected token in instruction: {self.current_token}")

                return None
                
            self.next_token()
            self.parse_newline_and_space()
            
        # if self.par_verb_flag:
        print(self._par_colorize(f"Line {self.line_number}: ", 'DEBUG_COLOR'), end="     ")
        
        op_class.operands = operands
        
        # print(f'In parse_instruction : {Instruction(op, operands)}')    #TODO
        print(f'In parse_instruction : {op_class}')    #TODO
        
        return op_class     # Instruction(op, operands)
        # else:
        #     print(f"Unknown instruction: {self.current_token}")
        #     return None
    
    def parse_export(self):
        export = Export()
        self.next_token()
        self.parse_newline_and_space()
        
        if self.current_token is None:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected EOF in export")
            return None
        if isinstance(self.current_token, LPAREN):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token ')' in export")
            return None

        if not isinstance(self.current_token, STRING):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")  
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected export name to be a string")
            return None
        
        export.value = self.current_token
        self.next_token()   
        self.parse_newline_and_space()
        
        if not isinstance(self.current_token, LPAREN):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected '(' after export name")
            return None
            
        self.next_token()
        self.parse_newline_and_space()
        
        # print(self.current_token)
        if not isinstance(self.current_token, Func):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected 'func' after '(' in export")
            return None
        
        self.next_token()
        self.parse_newline_and_space()
        
        # print(self.current_token)
        if not isinstance(self.current_token, ID):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected function name after 'func' in export")
            return None
        # func_name_registered = False
        exp_func = Func(self.current_token.value)
        # for func in self.module.funcs:
        #     if self.current_token.value == func.name:
        #         func_name_registered = True
        #         exp_func = func
        # if not func_name_registered:
        #     print("Function name not registered in export")
        #     return None

        export.exp_func = exp_func
        self.next_token()
        self.parse_newline_and_space()
        
        if not isinstance(self.current_token, RPAREN):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected token ')' after function name in export")
            return None
        self.next_token()
        self.parse_newline_and_space()
        
        if not isinstance(self.current_token, RPAREN):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected token ')' in export")
            return None
        
        return export
    
    def parse_memory(self):
        mem = Memory()
        self.next_token()
        self.parse_newline_and_space()
        
        # mem_name = None
        if not isinstance(self.current_token, ID):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")    
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected memory name after 'mem'")
            return None
        mem.name = self.current_token.value
        self.next_token() 
        self.parse_newline_and_space()
        
        if not isinstance(self.current_token, CONST):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected a CONST after memory name")
            return None
        mem.value = self.current_token
        # self.module.mems.append(mem)
        self.next_token()
        self.parse_newline_and_space()
        
        if not isinstance(self.current_token, RPAREN):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")    
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected token ')' in memory")
            return None
        return mem

    def parse_global(self):
        glob = Global()
        self.next_token()
        self.parse_newline_and_space()
        
        if isinstance(self.current_token, ID):
            glob.name = self.current_token.value
            self.next_token()
            self.parse_newline_and_space()
            
        if isinstance(self.current_token, TYPE):
            glob.type = self.current_token.value
            self.next_token()
            self.parse_newline_and_space()
            
        else:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected local type")
            return None
        
        if isinstance(self.current_token, LPAREN):
            self.next_token()
            self.parse_newline_and_space()
            
            if isinstance(self.current_token, _i32_const):
                self.next_token()
                self.parse_newline_and_space()
                
                if isinstance(self.current_token, CONST):
                    glob.value = self.current_token.value
                    self.next_token()
                    self.parse_newline_and_space()
                    
                    if isinstance(self.current_token, RPAREN):
                        self.next_token()
                        self.parse_newline_and_space()
                    else:
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')'")
                        return None
                
                else:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected a numeric literal")
                    return None          
                
            elif isinstance(self.current_token, Instruction):
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Invalid initializer: instruction not valid in initializer expression: '{self.current_token}'")
                return None  
            
            else:
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected an instr.")
                return None
            
            
            
        elif isinstance(self.current_token, _i32_const):
            self.next_token()
            self.parse_newline_and_space()
            
            if isinstance(self.current_token, CONST):
                glob.value = self.current_token.value
                self.next_token()
                self.parse_newline_and_space()
                
                # if isinstance(self.current_token, RPAREN):
                #     self.next_token()
                #     self.parse_newline_and_space()
                # else:
                #     print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                #     print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')'")
                #     return None
            
            else:
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected a numeric literal")
                return None
        elif isinstance(self.current_token, Instruction):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Invalid initializer: instruction not valid in initializer expression: '{self.current_token}'")
            return None  
            
        else:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected an instr.")
            return None
            
        if not isinstance(self.current_token, RPAREN):
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")    
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected token ')' in global")
            return None
        
        print("parse_global_current_token : " + str(self.current_token))       
        return glob
    
    def _par_colorize(self, text, color_key):
        if self.par_col_flag:
            return f"{COLORS[color_key]}{text}{COLORS['RESET_COLOR']}"
        return text