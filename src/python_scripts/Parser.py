from Lexer import (
    LPAREN, RPAREN, ID, TYPE, CONST, STRING, EOF,
    Module, Func, Param, Result, Local, Export, Memory, 
    Instruction, ControlFlowInstruction, BinaryInstruction,
    _i32_const, 
    _i32_add, 
    _i32_sub,
    _i32_mul,
    _i32_div_s,
    _i32_ge_u,
    _i32_gt_s,
    
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
    _if
)

class Parser:
    def __init__(self):
        self.current_token = None
        self.token_index = 0
        self.tokens = []
        self.module = None
        # self.funcs = []
    
    def next_token(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            print("Parser index Error")
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
        
        self.module = Module(mems=[], funcs=[], exports=[])
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
                    self.module.funcs.append(func)
                elif isinstance(self.current_token, Export):
                    export = self.parse_export()
                    if export is None :
                        return None

                    self.module.exports.append(export)
                    print(f"test_export : {export}")

                elif isinstance(self.current_token, Memory):

                    mem = self.parse_memory()
                    if mem is None :
                        return None
                    self.module.mems.append(mem)
                    print(f"test_mem : {mem}")

                else:
                    print(f"Unexpected token in module: {self.current_token} after (")
                    return None
                
                if not isinstance(self.current_token, RPAREN):
                    print("Expected ')' after module element")
                    return None
                self.next_token()
            else:
                print(f"Unexpected token in module: {self.current_token}")
                return None
        
        self.next_token()
        return self.module
    
    def parse_func(self):
        func = Func()
        self.next_token()
        
        if isinstance(self.current_token, ID):
            func.name = self.current_token.value
            self.next_token()
        
        # TODO: Parse params ... first, then instructions check
        
        # (...) (...) (...)
        while not isinstance(self.current_token, RPAREN):
            # if not isinstance(self.current_token, LPAREN):
            #     print(f"Unexpected token in func: {self.current_token}")
            #     return None
            
            if isinstance(self.current_token, LPAREN):
                
                self.next_token()
                if isinstance(self.current_token, Export):
                    self.next_token()
                    if not isinstance(self.current_token, STRING):
                        print("Expected export name to be a string in function signature")
                        return None
                    func.export_name = self.current_token
                    self.next_token()
                elif isinstance(self.current_token, Param):
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
                
                elif isinstance(self.current_token, ControlFlowInstruction):
                    print('ControlFlowInstruction :  ' + str(type(self.current_token)))
                
                    controlFlowInstr = self.parse_control_flow()
                    if controlFlowInstr is None:
                        return None
                    func.body.append(controlFlowInstr)
                    
                elif isinstance(self.current_token, Instruction):
                    print('func (...) (...) (... ' + str(type(self.current_token)))
                    instr = self.parse_instruction()
                    if instr is None:
                        return None
                    func.body.append(instr)
                    
                else:
                    print(f"Instruction {self.current_token} in function {func.name} not found!")
                    break
                

                # Check closing parenthesis for this if branch
                if not isinstance(self.current_token, RPAREN):
                    print("Expected ')' after func element")
                    return None
                self.next_token()
                
            elif isinstance(self.current_token, ControlFlowInstruction):
                print('ControlFlowInstruction :  ' + str(type(self.current_token)))
                
                if isinstance(self.current_token, _nop):
                    self.next_token()
                    continue
                elif isinstance(self.current_token, _block):
                    block = self.parse_block()

                    break
                elif isinstance(self.current_token, _loop):
                    break
                elif isinstance(self.current_token, _br):
                    break
                elif isinstance(self.current_token, _br_if):
                    break
                elif isinstance(self.current_token, _if):
                    break
                elif isinstance(self.current_token, _call):
                    break
                elif isinstance(self.current_token, _return):
                    break
                else:
                    print("Is ControlFlowInstruction {self.current_token} but not found!")
                    break
                
            elif isinstance(self.current_token, Instruction):
                print('Currrent Instruction without (...) surrounded' + str(type(self.current_token)))
                continue
            else:
                print(f"Instruction {self.current_token} in function {func.name} not found!")
                break
            
        print('After looping: ' + str(self.current_token))
        if not isinstance(self.current_token, RPAREN):
            print("Expected ')' after all func elements")
            return None
            
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
    
    def parse_control_flow(self):

        if isinstance(self.current_token, _nop):
            self.next_token()
            return ControlFlowInstruction(_nop)

        elif isinstance(self.current_token, _block):
            self.next_token()
            return self.parse_block()
            
        elif isinstance(self.current_token, _loop):
            self.next_token()
            return self.parse_loop()

        elif isinstance(self.current_token, _br):
            self.next_token()
            return self.parse_br()

        elif isinstance(self.current_token, _br_if):
            pass
        
        elif isinstance(self.current_token, _if):
            self.next_token()
            return self.parse_if()
            
        elif isinstance(self.current_token, _call):
            self.next_token()
            
            if not isinstance(self.current_token, (CONST, ID)):
                print("Expected CONST or ID after call instruction")
                return None
            self.next_token()
                
        elif isinstance(self.current_token, _return):
            # No operands needed, just consume any values on stack
            self.next_token()
            return ControlFlowInstruction(_return)

        else:
            print("Is ControlFlowInstruction {self.current_token} but not found!")
            pass

    
    def parse_block(self):

        operands = []
        # Parse operands/instructions until closing parenthesis
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, LPAREN):
                self.next_token()
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
                    print('(...) Other options in parse_block???')

                if not isinstance(self.current_token, RPAREN):
                    print("Expected ')' after nested instruction")
                    return None
                self.next_token()
            else:
                # Handle immediate values
                if isinstance(self.current_token, (CONST, ID)):
                    operands.append(self.current_token.value)
                    self.next_token()
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
                    print('Other options in parse_block???')
                    break
        return ControlFlowInstruction(_block, operands)    



    def parse_loop(self):

        operands = []
        # Parse operands/instructions until closing parenthesis
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, LPAREN):
                self.next_token()
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
                    print('(...) Other options in parse_loop???')

                if not isinstance(self.current_token, RPAREN):
                    print("Expected ')' after nested instruction")
                    return None
                self.next_token()
            else:
                print(f'else in parse_loop, current_token : {self.current_token}')

                # Handle immediate values
                if isinstance(self.current_token, (CONST, ID)):
                    operands.append(self.current_token.value)
                    self.next_token()
                elif isinstance(self.current_token, ControlFlowInstruction):
                    nested_instr = self.parse_control_flow()
                    print(f'nested_instr in parse_loop : {nested_instr}')
                    if nested_instr is None:
                        return None
                    operands.append(nested_instr)
                elif isinstance(self.current_token, Instruction):
                    nested_instr = self.parse_instruction()
                    if nested_instr is None:
                        return None
                    operands.append(nested_instr)
                else:
                    print('Other options/operations/class of instrustions in parse_loop???')
                    break
        return ControlFlowInstruction(_loop, operands)  

    def parse_br(self):
        # Parse function index or name
        if isinstance(self.current_token, (CONST, ID)):
            operand = self.current_token
            self.next_token()
            return ControlFlowInstruction(_br, {operand})
        else:
            print("Expected function index/name for br")
            return None

    def parse_br_if(self):
        pass
    
    def parse_if(self):
        
        operands = []
        # Parse operands/instructions until closing parenthesis
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, LPAREN):
                self.next_token()
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
                    print('(...) Other options in parse_block???')

                if not isinstance(self.current_token, RPAREN):
                    print("Expected ')' after nested instruction")
                    return None
                self.next_token()
            else:
                # Handle immediate values
                if isinstance(self.current_token, (CONST, ID)):
                    operands.append(self.current_token.value)
                    self.next_token()
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
                    print('Other options in parse_block???')
                    break
                
                
        # For 'if' instruction, handle else branch
        if isinstance(self.current_token, LPAREN):
            self.next_token()
            if isinstance(self.current_token, _else):
                self.next_token()
                else_operands = []
                    
                while not isinstance(self.current_token, RPAREN):
                    if isinstance(self.current_token, LPAREN):
                        self.next_token()
                        nested_instr = self.parse_instruction()
                        if nested_instr is None:
                            return None
                        else_operands.append(nested_instr)
                            
                        if not isinstance(self.current_token, RPAREN):
                            print("Expected ')' after else instruction")
                            return None
                        self.next_token()
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

        operands = []
        # instructions = []
        
        # 3 ControlFlowInstructions with nested loop possibilities
        if op in ['block', 'loop', 'if']:
            
            # Parse operands/instructions until closing parenthesis
            while not isinstance(self.current_token, RPAREN):
                if isinstance(self.current_token, LPAREN):
                    self.next_token()
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
                        print('Other options in parse_control_flow???')

                    if not isinstance(self.current_token, RPAREN):
                        print("Expected ')' after nested instruction")
                        return None
                    self.next_token()
                else:
                    # Handle immediate values
                    if isinstance(self.current_token, (CONST, ID)):
                        operands.append(self.current_token.value)
                        self.next_token()
                    else:
                        break
            
            # For 'if' instruction, handle else branch
            if op == 'if' and isinstance(self.current_token, LPAREN):
                self.next_token()
                if isinstance(self.current_token, _else):
                    self.next_token()
                    else_operands = []
                    
                    while not isinstance(self.current_token, RPAREN):
                        if isinstance(self.current_token, LPAREN):
                            self.next_token()
                            nested_instr = self.parse_instruction()
                            if nested_instr is None:
                                return None
                            else_operands.append(nested_instr)
                            
                            if not isinstance(self.current_token, RPAREN):
                                print("Expected ')' after else instruction")
                                return None
                            self.next_token()
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
        
        elif op == 'br_if':
            
            print("Expected implementation for br_if parser")
            return None
        
        elif op == 'call':
            # Parse function index or name
            if isinstance(self.current_token, (CONST, ID)):
                operands.append(self.current_token.value)
                self.next_token()
            else:
                print("Expected function index/name for call")
                return None
            
            # Parse call arguments
            while not isinstance(self.current_token, RPAREN):
                if isinstance(self.current_token, LPAREN):
                    self.next_token()
                    nested_instr = self.parse_instruction()
                    if nested_instr is None:
                        return None
                    operands.append(nested_instr)
                    
                    if not isinstance(self.current_token, RPAREN):
                        print("Expected ')' after call argument")
                        return None
                    self.next_token()
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
            return ControlFLowInstruction(op, operands)




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
            return BinaryInstruction(op, operands)
        
        self.next_token()
        
        while not isinstance(self.current_token, RPAREN):
            if isinstance(self.current_token, (CONST, ID)):
                operands.append(self.current_token.value)
                
            elif isinstance(self.current_token, LPAREN):
                self.next_token()
                nested_instr = self.parse_instruction()
                if nested_instr is None:
                    return None
                operands.append(nested_instr)
                if not isinstance(self.current_token, RPAREN):
                    print("Expected ')' after nested instruction")
                    return None
            else:
                print(f"Unexpected token in instruction: {self.current_token}")
                return None
                
            self.next_token()
        
        print(f'In parse_instruction : {Instruction(op, operands)}')
        return op_class     # Instruction(op, operands)
        # else:
        #     print(f"Unknown instruction: {self.current_token}")
        #     return None
    
    def parse_export(self):
        export = Export()
        self.next_token()
        if self.current_token is None:
            print("Unexpected EOF in export")
            return None
        if isinstance(self.current_token, LPAREN):
            print("Unexpected token ')' in export")
            return None

        if not isinstance(self.current_token, STRING):
            print("Expected export name to be a string")
            return None
        
        export.value = self.current_token
        self.next_token()   
        if not isinstance(self.current_token, LPAREN):
            print("Expected '(' after export name")
            return None
            
        self.next_token()
        # print(self.current_token)
        if not isinstance(self.current_token, Func):
            print("Expected 'func' after '(' in export")
            return None
        
        self.next_token()
        # print(self.current_token)
        if not isinstance(self.current_token, ID):
            print("Expected funcction name after 'func' in export")
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
        if not isinstance(self.current_token, RPAREN):
            print("Expected token ')' after function name in export")
            return None
        self.next_token()
        if not isinstance(self.current_token, RPAREN):
            print("Expected token ')' in export")
            return None
        
        return export
    
    def parse_memory(self):
        mem = Memory()
        self.next_token()
        # mem_name = None
        if not isinstance(self.current_token, ID):
            print("Expected memory name after 'mem'")
            return None
        mem.name = self.current_token.value
        self.next_token() 
        if not isinstance(self.current_token, CONST):
            print("Expected a CONST after memory name")
            return None
        mem.value = self.current_token
        # self.module.mems.append(mem)
        self.next_token()
        if not isinstance(self.current_token, RPAREN):
            print("Expected token ')' in memory")
            return None
        return mem
