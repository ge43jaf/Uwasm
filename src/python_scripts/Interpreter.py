from Lexer import (
    Module, Func, Param, Local, Export, Memory, Global,
    Instruction, ControlFlowInstruction, BinaryInstruction,
    _i32_const, _i32_add, _i32_sub, _i32_mul, _i32_div_s,
    _i32_ge_u, _i32_gt_s, _i32_lt_s, _i32_lt_u, _i32_clz,
    _local_get, _local_set, _local_tee,
    _global_get, _global_set,
    _call, _return, _nop, _block, _loop, _br, _br_if, _if,  _else, _end,
    _i32_load, _i32_store
)
from typing import List, Dict, Any, Optional, Union
import sys

COLORS = {
    'ERROR_COLOR': '\033[1;31m',
    'WARNING_COLOR': '\033[1;33m',
    'SUCCESS_COLOR': '\033[1;32m',
    'INFO_COLOR': '\033[1;34m',
    'DEBUG_COLOR': '\033[36m',
    'RESET_COLOR': '\033[0m',
}

class RuntimeError(Exception):  # Custom
    
    def __init__(self, message, line_number=None):
        self.message = message
        self.line_number = line_number
        super().__init__(f"RuntimeError: {message}" + (f" at line {line_number}" if line_number else ""))

class ExecutionContext:
    def __init__(self, func: Func, caller_context=None):
        self.func = func
        self.locals: Dict[str, Any] = {}
        self.return_value = None
        self.caller_context = caller_context
        self.pc = 0  # instruction sequence
        self.loops: Dict[str, Any] = {}
        self.ifs: Dict[str, Any] = {}
        
 
        
    def __repr__(self):
        return f"ExecutionContext(func={self.func.name}, locals={self.locals})"

class Interpreter:
    def __init__(self, module: Module, verbose: bool = False, use_colors: bool = False):
        self.module = module
        self.verbose = verbose
        self.use_colors = use_colors
        
        # Runtime state
        self.stack: List[Any] = []
        self.globals: Dict[str, Any] = {}
        self.memory: bytearray = bytearray()
        self.call_stack: List[ExecutionContext] = []
        self.current_context: Optional[ExecutionContext] = None
        
        # Function lookup table
        self.functions: Dict[str, Func] = {}
        for func in module.funcs:
            if func.name:
                self.functions[func.name] = func
        
        self.initialize_memory()
        
        self.initialize_globals()
    
    def _colorize(self, text: str, color_key: str) -> str:
        if self.use_colors and color_key in COLORS:
            return f"{COLORS[color_key]}{text}{COLORS['RESET_COLOR']}"
        return text
    
    def initialize_memory(self):
        
        for mem in self.module.mems:
            if mem.value and hasattr(mem.value, 'value'):
                # Convert pages to bytes (1 page = 64KB)
                pages = int(mem.value.value)
                self.memory = bytearray(pages * 65536)
                if self.verbose:
                    print(self._colorize(f"INFO: ", 'INFO_COLOR') + 
                          f"Initialized memory with {pages} pages ({len(self.memory)} bytes)")
    
    def initialize_globals(self):
        
        for glob in self.module.globs:
            if glob.name and glob.value:
                self.globals[glob.name] = int(glob.value)
                if self.verbose:
                    print(self._colorize(f"INFO: ", 'INFO_COLOR') + 
                          f"Initialized global {glob.name} = {glob.value}")
    
    def execute(self) -> Optional[Any]:
        """Main execution entry point"""
        try:
            # Start with exported functions or main function
            export_func = self.find_exported_function()
            if export_func:
                return self.execute_function(export_func)
            elif self.module.funcs:
                return self.execute_function(self.module.funcs[0])
            else:
                print(self._colorize("WARNING: ", 'WARNING_COLOR') + "No functions to execute")
                return None
                
        except RuntimeError as e:
            print(self._colorize("RUNTIME ERROR: ", 'ERROR_COLOR') + str(e))
            return None
        except Exception as e:
            print(self._colorize("INTERNAL ERROR: ", 'ERROR_COLOR') + str(e))
            return None
    
    def find_exported_function(self) -> Optional[Func]:
        # Find the first exported function
        for export in self.module.exports:
            if export.exp_func and export.exp_func.name:
                func_name = export.exp_func.name
                if func_name in self.functions:
                    return self.functions[func_name]
        raise RuntimeError(f"Nothing returned in find_exported_function()")
        return None
    
    def execute_function(self, func_name: str, args: List[Any] = None) -> Any:
        
        if args is None:
            args = []
        
        func = Func()
        for f in self.module.funcs:
            if f.name == func_name:
                func = f
                
        print("execute_function args: " + str(args))
        print("execute_function name: " + str(func))
        print("execute_function export_names: " + str(func.export_names))
        print("execute_function params: " + str(func.params))
        
        print("execute_function results: " + str(func.results))
        print("execute_function locals: " + str(func.locals))
        print("execute_function body: " + str(func.body[0] if func.body else "None "))
        
        # Validate arguments
        if len(args) != len(func.params):
            raise RuntimeError(f"Function {func.name} expects {len(func.params)} arguments, got {len(args)}")
        
        # Create execution context
        context = ExecutionContext(func)
        self.call_stack.append(context)
        self.current_context = context
        
        # Initialize parameters as locals
        for i, param in enumerate(func.params):
            # print(f"param : {param}")
            if param.name is not None:
                # print(f"param.name : {param.name}")
                context.locals[param.name] = args[i] 
            else:
                
                context.locals[i] = args[i]
            # context.locals[param.name] = args[i]
        # Initialize Default i32 value (0)
        # # param & local together
        # for param in func.params:
        #     self.locals[param.name] = 0  
        for i, local in enumerate(func.locals):
            # print(f"local : {local}")
            if local.name is not None:
                # print(f"local.name : {local.name}")
                context.locals[local.name] = 0 
            else:
                context.locals[len(func.params) + i] = 0 
                
        # print(f"locals : {context.locals}")
            
        if self.verbose:
            print(self._colorize(f"DEBUG: ", 'DEBUG_COLOR') + 
                  f"Executing function {func.name} with args {args}")
        
        # Execute  body
        try:
            result = self.execute_instructions(func.body, context)
            print("Result in execute_function : " + str(result))
            self.call_stack.pop()
            if self.call_stack:
                self.current_context = self.call_stack[-1]
            else:
                self.current_context = None
            return result
        except Exception as e:
            self.call_stack.pop()
            raise e
    
    def execute_instructions(self, instructions: List[Instruction], context: ExecutionContext) -> Any:
        
        for instr in instructions:
            if self.verbose:
                print(self._colorize(f"DEBUG: ", 'DEBUG_COLOR') + 
                      f"Executing: {type(instr).__name__}, Stack: {self.stack}")
            
            result = self.execute_instruction(instr, context)
            print("Result in execute_instructions : " + str(result))
            if result is not None:  # Return value from function
                return result

        # raise RuntimeError(f"Nothing returned in execute_instructions()")
        return None
    
    def execute_instruction(self, instr: Instruction, context: ExecutionContext) -> Any:
        
        try:
            if isinstance(instr, _i32_const):
                return self.execute_i32_const(instr)
            elif isinstance(instr, BinaryInstruction):
                return self.execute_binary_instruction(instr)
            elif isinstance(instr, _local_get):
                print("local.get in execute_instruction")
                return self.execute_local_get(instr, context)
            elif isinstance(instr, _local_set):
                return self.execute_local_set(instr, context)
            elif isinstance(instr, _call):
                return self.execute_call(instr, context)
            elif isinstance(instr, _return):
                return self.execute_return(instr, context)
            elif isinstance(instr, _nop):
                return self.execute_nop()
            elif isinstance(instr, ControlFlowInstruction):
                return self.execute_control_flow(instr, context)
            elif isinstance(instr, _i32_load):
                return self.execute_i32_load(instr)
            elif isinstance(instr, _i32_store):
                return self.execute_i32_store(instr)
            else:
                raise RuntimeError(f"Unsupported instruction: {type(instr).__name__}")
                
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"Error executing {type(instr).__name__}: {str(e)}")
    
    def execute_i32_const(self, instr: _i32_const) -> None:
        
        if hasattr(instr, 'operands') and instr.operands:
            value = int(instr.operands[0])
            self.stack.append(value)
            if self.verbose:
                print(self._colorize(f"DEBUG: ", 'DEBUG_COLOR') + f"Pushed constant: {value}")
    
    def execute_binary_instruction(self, instr: BinaryInstruction) -> None:
        
        self.check_stack_size(2, instr)
        
        b = self.stack.pop()
        a = self.stack.pop()
        
        print(str(type(instr)))
        print(f"instr : {instr} in execute_binary_instruction")
        
        print(f"a : {a}, b : {b} in execute_binary_instruction")
        if isinstance(instr, _i32_add):
            result = a + b
        elif isinstance(instr, _i32_sub):
            result = a - b
        elif isinstance(instr, _i32_mul):
            result = a * b
        elif isinstance(instr, _i32_div_s):
            if b == 0:
                raise RuntimeError("Division by zero")
            result = a // b
        elif isinstance(instr, _i32_ge_u):
            result = 1 if a >= b else 0
        elif isinstance(instr, _i32_gt_s):
            result = 1 if a > b else 0
        elif isinstance(instr, _i32_lt_s):
            result = 1 if a < b else 0
        elif isinstance(instr, _i32_lt_u):
            result = 1 if a < b else 0
        else:
            raise RuntimeError(f"Unsupported binary instruction: {type(instr).__name__}")
        
        self.stack.append(result)
        if self.verbose:
            print(self._colorize(f"DEBUG: ", 'DEBUG_COLOR') + f"{type(instr).__name__}: {a} op {b} = {result}")
    
    def execute_local_get(self, instr: _local_get, context: ExecutionContext) -> None:
        
        print(f"instr : {instr} with operands : {instr.operands} in execute_local_get : ")
        if hasattr(instr, 'operands') and instr.operands:
            local_name = instr.operands[0]
            print(f"type(local_name) : {type(local_name)}")
            if local_name.startswith("$") and local_name in context.locals:
                value = context.locals[local_name]
                self.stack.append(value)
                if self.verbose:
                    print(self._colorize(f"DEBUG: ", 'DEBUG_COLOR') + f"Pushed local {local_name}: {value}")
            elif int(local_name) < len(context.locals):
                print(context.locals)
                print(list(context.locals))
                value = context.locals[list(context.locals)[int(local_name)]]
                self.stack.append(value)
                if self.verbose:
                    print(self._colorize(f"DEBUG: ", 'DEBUG_COLOR') + f"Pushed local {local_name}: {value}")
            
            else:
                raise RuntimeError(f"Undefined local variable: {local_name}")
    
    def execute_local_set(self, instr: _local_set, context: ExecutionContext) -> None:
        
        self.check_stack_size(1, instr)
        
        if hasattr(instr, 'operands') and instr.operands:
            local_name = instr.operands[0]
            value = self.stack.pop()
            context.locals[local_name] = value
            if self.verbose:
                print(self._colorize(f"DEBUG: ", 'DEBUG_COLOR') + f"Set local {local_name} = {value}")
    
    def execute_call(self, instr: _call, context: ExecutionContext) -> Any:
        
        if hasattr(instr, 'operands') and instr.operands:
            func_name = instr.operands[0]
            if func_name in self.functions:
                # Prepare arguments from stack
                target_func = self.functions[func_name]
                args = []
                for _ in range(len(target_func.params)):
                    self.check_stack_size(1, instr)
                    args.insert(0, self.stack.pop())  # Reverse order for correct argument passing
                
                result = self.execute_function(target_func, args)
                
                # Push result
                if result is not None:
                    self.stack.append(result)
                
                return result
            else:
                raise RuntimeError(f"Undefined function: {func_name}")
    
    def execute_return(self, instr: _return, context: ExecutionContext) -> Any:
        
        return_value = None
        if self.stack:
            return_value = self.stack[-1]  # top of stack
            if self.verbose:
                print(self._colorize(f"DEBUG: ", 'DEBUG_COLOR') + f"Returning: {return_value}")
        return return_value
    
    def execute_nop(self) -> None:
        
        if self.verbose:
            print(self._colorize(f"DEBUG: ", 'DEBUG_COLOR') + "NOP executed")
    
    def execute_control_flow(self, instr: ControlFlowInstruction, context: ExecutionContext) -> Any:
        
        if isinstance(instr, _if):
            return self.execute_if(instr, context)
        elif isinstance(instr, _block):
            return self.execute_block(instr, context)
        elif isinstance(instr, _loop):
            return self.execute_loop(instr, context)
        elif isinstance(instr, _br):
            return self.execute_br(instr, context)
        elif isinstance(instr, _br_if):
            return self.execute_br_if(instr, context)
        else:
            raise RuntimeError(f"Unsupported control flow instruction: {type(instr).__name__}")
    
    def execute_if(self, instr: _if, context: ExecutionContext) -> Any:
        if hasattr(instr, 'name') and instr.name:
            context.ifs[instr.name] = instr
            
        self.check_stack_size(1, instr)
        condition = self.stack.pop()
        
        if condition != 0:  # True
            if hasattr(instr, 'operands') and instr.operands:
                return self.execute_instructions(instr.operands, context)
        # TODO : Else branch 
        # raise RuntimeError(f"Nothing returned in execute_if()")
        return None
    
    def execute_block(self, instr: _block, context: ExecutionContext) -> Any:
        
        if hasattr(instr, 'operands') and instr.operands:
            return self.execute_instructions(instr.operands, context)
        raise RuntimeError(f"Nothing returned in execute_block()")
        return None
    
    def execute_loop(self, instr: _loop, context: ExecutionContext) -> Any:
        if hasattr(instr, 'name') and instr.name:
            context.loops[instr.name] = instr
        
        if hasattr(instr, 'operands') and instr.operands:
            return self.execute_instructions(instr.operands, context)
        raise RuntimeError(f"Nothing returned in execute_loop()")
        return None
    
    def execute_br(self, instr: _br, context: ExecutionContext) -> Any:
        # TODO (simplified)
        if self.verbose:
            print(self._colorize(f"DEBUG: ", 'DEBUG_COLOR') + "BR instruction executed (no-op in simple interpreter)")
        raise RuntimeError(f"Nothing returned in execute_br()")
        return None
    
    def execute_br_if(self, instr: _br_if, context: ExecutionContext) -> Any:
        # TODO (simplified)
        self.check_stack_size(1, instr)
        condition = self.stack.pop()
        if condition != 0 and hasattr(instr, 'operands') and instr.operands:
            # Branch target would be used here in full implementation
            instr_name = instr.operands[0]
            if instr_name in context.ifs:
                return self.execute_if(context.ifs[instr_name], context)
            elif instr_name in context.loops:
                return self.execute_loop(context.loops[instr_name], context)
            else:
                raise RuntimeError(f"No if or loop called {instr_name}")
        
        # else:
        #     raise RuntimeError(f"No operand for {instr}")
        # raise RuntimeError(f"Nothing returned in execute_br_if()")
        return None
    
    def execute_i32_load(self, instr: _i32_load) -> None:
        
        self.check_stack_size(1, instr)
        address = self.stack.pop()
        
        # Check memory bounds
        if address < 0 or address + 4 > len(self.memory):
            raise RuntimeError(f"Memory access out of bounds: {address}")
        
        # Read 4 bytes from memory
        value = int.from_bytes(self.memory[address:address+4], 'little', signed=True)
        self.stack.append(value)
        
        if self.verbose:
            print(self._colorize(f"DEBUG: ", 'DEBUG_COLOR') + f"Loaded from memory[{address}]: {value}")
    
    def execute_i32_store(self, instr: _i32_store) -> None:
        
        self.check_stack_size(2, instr)
        value = self.stack.pop()
        address = self.stack.pop()
        
        # Check memory bounds
        if address < 0 or address + 4 > len(self.memory):
            raise RuntimeError(f"Memory access out of bounds: {address}")
        
        # Store 4 bytes to memory
        self.memory[address:address+4] = value.to_bytes(4, 'little', signed=True)
        
        if self.verbose:
            print(self._colorize(f"DEBUG: ", 'DEBUG_COLOR') + f"Stored to memory[{address}]: {value}")
    
    def check_stack_size(self, required: int, instr: Instruction) -> None:
        
        if len(self.stack) < required:
            raise RuntimeError(
                f"Stack underflow for {type(instr).__name__}: "
                f"required {required}, got {len(self.stack)}"
            )
    
    def get_result(self) -> Optional[Any]:
        
        if self.stack:
            return self.stack[-1]
        raise RuntimeError(f"Nothing returned in get_result()")
        return None

# Helper function 
def interpret_ast(ast: Module, verbose: bool = False, use_colors: bool = False) -> Optional[Any]:
    
    interpreter = Interpreter(ast, verbose=verbose, use_colors=use_colors)
    result = interpreter.execute()
    
    if verbose:
        if result is not None:
            print(interpreter._colorize(f"RESULT: ", 'SUCCESS_COLOR') + f"{result}")
        else:
            print(interpreter._colorize("INFO: ", 'INFO_COLOR') + "Execution completed (no return value)")
    
    return result

if __name__ == "__main__":
    # Test the interpreter standalone
    print("WebAssembly Interpreter - Standalone Test")
    print("This module is designed to be imported and used with the existing parser/validator")
    
    
    
# TODO : Check for export, etc. Currently all func called $foo