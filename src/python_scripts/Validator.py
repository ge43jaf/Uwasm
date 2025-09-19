
from Lexer import (
    LPAREN, RPAREN, ID, TYPE, CONST, STRING, EOF,
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

from Parser import *


class Validator:
    def __init__(self):
        self.current_token = None
        self.token_index = 0
        self.tokens = []
        self.module = None
        # self.funcs = []
        self.line_number = 1
        self.val_col_flag = False
        
    def next_token(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            print("Parser index Error")
            self.current_token = None
        return self.current_token
        
    def validate(self, ast):
        if not ast:
            print("Error: No ast to validate")
            return None
            
        self.module = ast
        # self.current_token = self.tokens[0]
        
        ce = self.check_export()
        cs = self.check_stack()
        ci = self.check_identifier()
        cf = self.check_floating_number()
        
        if ce and cs and ci and cf:
            return True
        else:
            return False
        
    def check_func_signature(self):
        pass
    
    # Export and Definition Checking
    def check_export(self):             # TODO: call by function index?
        funcs_names = []
        for func in self.module.funcs:
            # print(type(func.name))
            funcs_names.append(func.name)
            
        for exported_func in self.module.exports:
            if not exported_func.exp_func or not exported_func.exp_func.name:
                print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Export error: Missing function reference in export")
                return None
            
            # print(type(exported_func.exp_func.name))
            # print(exported_func.exp_func.name)
            # print(funcs_names)
            if exported_func.exp_func.name not in funcs_names:
                print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"Unexpected function to export: {exported_func}")
                return None
            
            print(f"Export checking successful")
        return True
    
    # Stack Checking
    def check_stack(self):
        
        stack = [] # Stack for simulation
        for mem in self.module.mems:
            pass
        
        for func in self.module.funcs:
            for instr in func.body:
                print("instr type : " + str(type(instr).__name__))
                # print(instr)
                # if isinstance(instr, _i32_const):
                #     stack.append("i32")
                
                # Check uniary instructions
                if isinstance(instr, _i32_const) or isinstance(instr, _local_get) or isinstance(instr, _global_get):
                    # print("Local get!!!")
                    stack.append("i32")     # TODO: Floating number check
                    
                # Check reverse uniary instructions
                if isinstance(instr, _local_set) or isinstance(instr, _global_set):
                    stack.pop()
                    
                if isinstance(instr, _local_tee):
                    if stack.pop() != "i32":
                        print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print("local.tee instrution waits for a i32 on stack!")
                        return None
                    stack.append("i32")
                    
                if isinstance(instr, BinaryInstruction):
                    print(f"BinaryInstruction: {instr}")
                    print(stack)
                    if len(stack) >= 2: # and stack[-1]
                        op1 = stack.pop()
                        op2 = stack.pop()
                        if op1 != "i32":
                            print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                            print(f"TypeError: op1 for BinaryInstruction {instr}")
                            return None
                        if op2 != "i32":
                            print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                            print(f"TypeError: op2 for BinaryInstruction {instr}")
                            return None
                        stack.append("i32")
                        
                    else:
                        print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                        print(f"Stack error: not enough operands for BinaryInstruction")
                        return None
                        
        print(f"Stack checking successful")
        return True
    
    def check_identifier(self):
        id_set =set()
        
        for mem in self.module.mems:
            print("TestMemmmmmmmmmmmmmmm")
            if not mem.name.startswith("$"):
                print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"MemoryIdentifierNameError: {mem.name}, should start with '$'")
                return None
        
        for func in self.module.funcs:
            
            func_id_set =set()
            
            # func.name can be None
            if not func.name:
                # DONE: wait for wasm2wat
                # print(f'{func}')
                # print(f"FunctionIdentifierNameError: function name NoneType")
                # return None
                pass
            elif not func.name.startswith("$"):
                print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                print(f"FunctionIdentifierNameError: {func.name}, should start with '$'")
                return None
            else:
                id_set.add(func.name)
                
            for param in func.params:
                
                # param.name can be None
                if not param.name:
                    # DONE: wait for wasm2wat
                    # print(f'{func}')
                    # print(f"ParameterIdentifierNameError: parameter name NoneType")
                    # return None
                    pass
                elif not param.name.startswith("$"):
                    print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"ParameterIdentifierNameError: {param.name}, should start with '$'")
                    return None
                else:
                    func_id_set.add(param.name)
                    
            for local in func.locals:
                
                # local.name can be None
                if not local.name:
                    # DONE: wait for wasm2wat
                    # print(f'{func}')
                    # print(f"LocalIdentifierNameError: local name NoneType")
                    # return None
                    pass
                elif not local.name.startswith("$"):
                    print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"LocalIdentifierNameError: {local.name}, should start with '$'")
                    return None
                else:
                    func_id_set.add(local.name)
            #TODO : check id in instructions    
        
        return True
    
    def check_floating_number(self):
        for func in self.module.funcs:
                
            for param in func.params:
                if not param.type:
                    # print(f'{func}')
                    print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")
                    print(f"ParameterTypeError: parameter type NoneType")
                    return None
                
                elif param.type != "i32":
                    # print("typeof param.type : " + str(type(param.type)))
                    # print('typeof "i32" : ' + str(type("i32")))
                    
                    print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")  
                    print(f"ParameterTypeError: {param.type}, should be i32")
                    return None
                else:
                    pass

            for local in func.locals:
                if not local.type:
                    # TODO: wait for wasm2wat
                    # print(f'{func}')
                    print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")  
                    print(f"LocalTypeError: local type NoneType")
                    return None
                
                elif local.type != "i32":
                    print(self._val_colorize("ERROR: ", 'ERROR_COLOR'), end="\n     ")  
                    print(f"Line {self.line_number}: LocalTypeError: {local.type}, should be i32")
                    return None
                else:
                    pass
        return True
    
    def _val_colorize(self, text, color_key):
        if self.val_col_flag:
            return f"{COLORS[color_key]}{text}{COLORS['RESET_COLOR']}"
        return text
    
    # def check_binary_instruction(self):
        