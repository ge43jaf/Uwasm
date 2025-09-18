
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
    _else,
    _end,
    
    _i32_load,
    _i32_store
    
)

COLORS = {
        
    'ERROR_COLOR': '\033[1;31m',   # Error messages - Bold Red
    'WARNING_COLOR': '\033[1;33m', # Warning messages - Bold Yellow  
    'SUCCESS_COLOR': '\033[1;32m', # Success messages - Bold Green
    'INFO_COLOR': '\033[1;34m',    # Information messages - Bold Blue
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
                        return None
                    self.module.funcs.append(func)
                elif isinstance(self.current_token, Export):    # Can only be surrounded by (...)
                    export = self.parse_export()
                    if export is None :
                        return None

                    self.module.exports.append(export)
                    # print(f"test_export : {export}")

                elif isinstance(self.current_token, Memory):    # Can only be surrounded by (...)

                    mem = self.parse_memory()
                    if mem is None :
                        return None
                    self.module.mems.append(mem)
                    # print(f"test_mem : {mem}")

                # TODO : before or after function definition?
                elif isinstance(self.current_token, Global):    # Can only be surrounded by (...)

                    glob = self.parse_global()
                    if glob is None :   #TODO: Error message
                        return None
                    self.module.mems.append(glob)
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
        
        # (...) (...) (...)
        while not isinstance(self.current_token, RPAREN):
            # if not isinstance(self.current_token, LPAREN):
            #     print(f"Unexpected token in func: {self.current_token}")
            #     return None
            # while isinstance(self.current_token, NEWLINE) or isinstance(self.current_token, SPACE):
            #     if isinstance(self.current_token, NEWLINE):
            #         self.line_number += 1
            #     self.next_token()
                
            if isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                    
                if isinstance(self.current_token, Export):  
                    self.next_token()
                    self.parse_newline_and_space()
                    
                    if not isinstance(self.current_token, STRING):
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected export name to be a string in function signature")
                        return None
                    func.export_name = self.current_token
                    self.next_token()
                    self.parse_newline_and_space()
                
                elif isinstance(self.current_token, Param):
                    if current_section and current_section != 'param':
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Line {self.line_number}: Error: Params must come before results and locals")
                        return None
                    current_section = 'param'
                    params_returned = self.parse_param()
                    if params_returned is None:
                        return None
                    func.params.extend(params_returned)
                    
                elif isinstance(self.current_token, Result):
                    if current_section and current_section not in ('param', 'result'):
                        print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ") 
                        print(f"Line {self.line_number}: Error: Results must come after params and before locals")
                        return None
                    current_section = 'result'
                    result = self.parse_result()
                    if result is None:
                        return None
                    func.results.append(result)
                    
                elif isinstance(self.current_token, Local):
                    current_section = 'local'
                    local = self.parse_local()
                    if local is None:
                        return None
                    func.locals.append(local)
                    
                elif isinstance(self.current_token, ControlFlowInstruction):
                    # TODO: Deletion
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
                        print('func (...) (...) (... ' + str(type(self.current_token))) #TODO: MOdification
                    instr = self.parse_instruction()
                    if instr is None:
                        return None
                    func.body.append(instr)
                    
                else:
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Instruction {self.current_token} in function {func.name} not found!")
                    # break
                    return None
                
                self.parse_newline_and_space()

                # Check closing parenthesis for this if branch
                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after func element")      # TODO : param i32 i32
                    print(self.current_token)
                    print(self.next_token)
                    return None
                self.next_token()
                self.parse_newline_and_space()
                    
            elif isinstance(self.current_token, ControlFlowInstruction):
                #TODO: MOdification/Deletion
                print('ControlFlowInstruction :  ' + str(type(self.current_token)))

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
                    print('func (...) (...) (... ' + str(type(self.current_token))) #TODO: MOdification
                instr = self.parse_instruction()
                if instr is None:
                    return None
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
        self.next_token()
        self.parse_newline_and_space()
        
        if isinstance(self.current_token, ID):
            local.name = self.current_token.value
            self.next_token()
            self.parse_newline_and_space()
            
        if isinstance(self.current_token, TYPE):
            local.type = self.current_token.value
            self.next_token()
            self.parse_newline_and_space()
            
        else:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected local type")
            return None
        
        return local
    
    def parse_result(self):
        self.next_token()
        self.parse_newline_and_space()
        if isinstance(self.current_token, TYPE):
            result_type = self.current_token.value
            self.next_token()
            self.parse_newline_and_space()
            return result_type
        else:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected result type")
            return None
    
    def parse_control_flow(self):

        if isinstance(self.current_token, _nop):
            self.next_token()
            self.parse_newline_and_space()
            return ControlFlowInstruction(_nop)

        elif isinstance(self.current_token, _block):
            self.next_token()
            self.parse_newline_and_space()
            return self.parse_block()
            
        elif isinstance(self.current_token, _loop):
            self.next_token()
            self.parse_newline_and_space()
            return self.parse_loop()

        elif isinstance(self.current_token, _br):
            self.next_token()
            self.parse_newline_and_space()
            return self.parse_br()

        elif isinstance(self.current_token, _br_if):
            self.next_token()
            self.parse_newline_and_space()
            return self.parse_br_if()
        
        elif isinstance(self.current_token, _if):
            self.next_token()
            self.parse_newline_and_space()
            return self.parse_if()
            
        elif isinstance(self.current_token, _call):
            self.next_token()
            self.parse_newline_and_space()
            
            if not isinstance(self.current_token, (CONST, ID)):
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected CONST or ID after call instruction")
                return None
            self.next_token()
            self.parse_newline_and_space()
            return ControlFlowInstruction(_call)
        
        elif isinstance(self.current_token, _return):
            # No operands needed, just consume any values on stack
            self.next_token()
            self.parse_newline_and_space()
            
            return ControlFlowInstruction(_return)

        else:
            op = self.current_token
            self.next_token()
            self.parse_newline_and_space()
            
            print(self._par_colorize("WARNING: ", 'WARNING_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Is ControlFlowInstruction {self.current_token} but not found!")
            # pass
            return ControlFlowInstruction(op)
    
    def parse_block(self):

        operands = []
        # Parse operands/instructions until closing parenthesis
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                
                if isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction()
                    if nested_instr is None:
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
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction()
                    if nested_instr is None:
                        return None
                    operands.append(nested_instr)
                else:   #TODO
                    print('Other options in parse_block???')
                    break
        return ControlFlowInstruction(_block, operands)    



    def parse_loop(self):

        operands = []
        # Parse operands/instructions until closing parenthesis
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                
                if isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction()
                    if nested_instr is None:
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
                    print(f'else in parse_loop, current_token : {self.current_token}')

                # Handle immediate values
                # if self.par_verb_flag:
                    print("Inside parse loop: " + str(type(self.current_token)))
                # if self.current_token == "end":
                if isinstance(self.current_token, _end):
                    return ControlFlowInstruction(_if, operands)
                
                if isinstance(self.current_token, (CONST, ID)):
                    operands.append(self.current_token.value)
                    self.next_token()
                    self.parse_newline_and_space()
                    
                elif isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    print(f'Line {self.line_number}: nested_instr in parse_loop : {nested_instr}')   #TODO
                    if nested_instr is None:
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction()
                    if nested_instr is None:
                        return None
                    operands.append(nested_instr)
                else:   #TODO
                    print('Other options/operations/class of instrustions in parse_loop???')
                    break
        return ControlFlowInstruction(_loop, operands)  

    def parse_br(self):
        # Parse function index or name
        if isinstance(self.current_token, (CONST, ID)):
            operand = self.current_token
            self.next_token()
            self.parse_newline_and_space()
            
            return ControlFlowInstruction(_br, {operand})
        else:
            print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
            print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected function index/name for br")
            return None

    # def parse_br_if(self):
    #     pass
    
    def parse_br_if(self):
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
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction()
                    if nested_instr is None:
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
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction()
                    if nested_instr is None:
                        return None
                    operands.append(nested_instr)
                else:
                    # End of br_if instruction or unexpected token
                    break

        return ControlFlowInstruction(_br_if, operands)
    
    def parse_if(self):
        
        operands = []
        # Parse operands/instructions until closing parenthesis
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                
                if isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction()
                    if nested_instr is None:
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
                    print("Inside parse if: " + str(type(self.current_token)))
                # if self.current_token == "end":
                if isinstance(self.current_token, _end):
                    return ControlFlowInstruction(_if, operands)
                
                if isinstance(self.current_token, (CONST, ID)):
                    operands.append(self.current_token.value)
                    self.next_token()
                    self.parse_newline_and_space()
                    
                elif isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    if nested_instr is None:
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction()
                    if nested_instr is None:
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
                        
                        nested_instr = self.parse_instruction()
                        if nested_instr is None:
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
                    
                return ControlFlowInstruction(_if, {
                    'then': operands,
                    'else': else_operands
                })

            return ControlFlowInstruction(_if, {
                'then': operands,
                'else': []  # Will be filled if there's an else branch
            })
                
        return ControlFlowInstruction(_if, operands)
        
    
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
                            return None
                        operands.append(nested_instr)
                    elif isinstance(self.current_token, Instruction):
                        nested_instr = self.parse_instruction()
                        if nested_instr is None:
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
            return ControlFLowInstruction(op, operands) #TODO




    def parse_instruction(self):
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
        op = type(self.current_token).__name__[1:].replace('_', '.')
        operands = []
        
        if isinstance(self.current_token, BinaryInstruction):
            self.next_token()
            self.parse_newline_and_space()
            
            return BinaryInstruction(op, operands)
        
        self.next_token()
        self.parse_newline_and_space()
        
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, (CONST, ID)):
                operands.append(self.current_token.value)
                
            elif isinstance(self.current_token, LPAREN):
                self.next_token()
                self.parse_newline_and_space()
                
                nested_instr = self.parse_instruction()
                if nested_instr is None:
                    return None
                operands.append(nested_instr)
                if not isinstance(self.current_token, RPAREN):
                    print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")   
                    print(f"Line {self.line_number}: Unexpected token '{self.current_token}', expected ')' after nested instruction")
                    return None
            else:
                print(self._par_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Line {self.line_number}: Unexpected token in instruction: {self.current_token}")

                return None
                
            self.next_token()
            self.parse_newline_and_space()
            
        if self.par_verb_flag:
            print(f'In parse_instruction : {Instruction(op, operands)}')    #TODO
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