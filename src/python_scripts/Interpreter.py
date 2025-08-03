from Lexer import (
    LPAREN, RPAREN, ID, TYPE, CONST, STRING, EOF,
    Module, Func, Param, Result, Local, Export, Memory, 
    Instruction, ControlFlowInstruction,
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

from Parser import *


class Interpreter:
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
        
    def interpret(self, ast):
        if not ast:
            print("Error: No ast to interprete")
            return None
            
        self.module = ast
        # self.current_token = self.tokens[0]
        
        self.check_export()
        self.check_stack()

    
    # Export and Definition Checking
    def check_export(self):
        funcs_names = []
        for func in self.module.funcs:
            # print(type(func.name))
            funcs_names.append(func.name)
            
        for exported_func in self.module.exports:
            # print(type(exported_func.exp_func.name))
            if exported_func.exp_func.name not in funcs_names:
                print(f"Unexpected function to export: {exported_func}")
                return None
            
            print(f"Export checking successful")
            
    # Stack Checking
    def check_stack(self):
        
        for mem in self.module.mems:
            pass