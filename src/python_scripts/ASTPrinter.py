
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
    _i32_lt_s,
    
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
    _else
)

from Parser import *

class ASTPrinter():
    def __init__(self):
        self.indent_str = "    "
        self.connector_str = "│   "
        self.branch_str = "├── "
        self.last_branch_str = "└── "
    
    def print_ast(self, ast, show_types=False):
        
        if isinstance(ast, Module):
            print("Module")
            self._print_module(ast, "", show_types)
        else:
            self._print_node(ast, "", True, show_types)
    
    def _print_module(self, module, prefix, show_types):

        children = []
        

        for i, mem in enumerate(module.mems):
            children.append(("Memory", mem, i == len(module.mems) - 1 and not module.funcs and not module.exports and not module.globs))
        

        for i, glob in enumerate(module.globs):
            children.append(("Global", glob, i == len(module.globs) - 1 and not module.funcs and not module.exports))
        

        for i, func in enumerate(module.funcs):
            children.append(("Function", func, i == len(module.funcs) - 1 and not module.exports))
        

        for i, export in enumerate(module.exports):
            children.append(("Export", export, i == len(module.exports) - 1))
        
        for i, (label, child, is_last) in enumerate(children):
            new_prefix = prefix + (self.indent_str if is_last else self.connector_str)
            branch = self.last_branch_str if is_last else self.branch_str
            
            print(f"{prefix}{branch}{label}: {getattr(child, 'name', '')}")
            self._print_node(child, new_prefix, is_last, show_types)
    
    def _print_node(self, node, prefix, is_last, show_types):
        """Recursively print AST nodes"""
        if isinstance(node, Memory):
            # pass
            self._print_memory(node, prefix, is_last, show_types)
        elif isinstance(node, Func):
            self._print_function(node, prefix, is_last, show_types)
        elif isinstance(node, Export):
            self._print_export(node, prefix, is_last, show_types)
        elif isinstance(node, (Instruction, ControlFlowInstruction)):
            self._print_instruction(node, prefix, is_last, show_types)
        elif isinstance(node, list):
            self._print_list(node, prefix, is_last, show_types)
        # elif hasattr(node, '__dict__'):
        #     self._print_object(node, prefix, is_last, show_types)
    
    def _print_memory(self, memory, prefix, is_last, show_types):
        # pass
        if memory.value:
            new_prefix = prefix + (self.indent_str if is_last else self.connector_str)
            print(f"{prefix}{self.last_branch_str}Size: {memory.value}")
            
    def _print_function(self, func, prefix, is_last, show_types):

        children = []
        
        if func.params:
            children.append(("Params", func.params, False))
        
        if func.results:
            children.append(("Results", func.results, False))
        
        if func.locals:
            children.append(("Locals", func.locals, False))
        
        if func.body:
            children.append(("Body", func.body, True))
        
        new_prefix = prefix + (self.indent_str if is_last else self.connector_str)
        
        for i, (label, child, child_is_last) in enumerate(children):
            branch = self.last_branch_str if child_is_last and i == len(children) - 1 else self.branch_str
            print(f"{prefix}{branch}{label}")
            self._print_node(child, new_prefix, child_is_last, show_types)
    
    def _print_export(self, export, prefix, is_last, show_types):

        if export.isFunc and export.exp_func and export.exp_func.name:
            # new_prefix = prefix + (self.indent_str if is_last else self.connector_str)
            print(f"{prefix}{self.last_branch_str}Function: {export.exp_func.name}")
        elif not export.isFunc and export.exp_mem and export.exp_mem.name:
            # new_prefix = prefix + (self.indent_str if is_last else self.connector_str)
            print(f"{prefix}{self.last_branch_str}Memory: {export.exp_mem.name}")
    
    
    def _print_instruction(self, instr, prefix, is_last, show_types):

        if hasattr(instr, 'operands') and instr.operands:
            new_prefix = prefix + (self.indent_str if is_last else self.connector_str)
            
            if isinstance(instr.operands, dict):
                # Handle dictionary operands (like if/block instructions)
                for i, (key, value) in enumerate(instr.operands.items()):
                    if value:  # Only print non-empty operands
                        branch = self.last_branch_str if i == len(instr.operands) - 1 else self.branch_str
                        print(prefix)
                        print(f"{prefix}{branch}{key.capitalize()}")
                        self._print_node(value, new_prefix, i == len(instr.operands) - 1, show_types)
            else:
                # Handle list operands
                for i, operand in enumerate(instr.operands):
                    branch = self.last_branch_str if i == len(instr.operands) - 1 else self.branch_str
                    operand_str = self._format_operand(operand, show_types)
                    print(f"{prefix}{branch}{operand_str}")
    
    def _print_list(self, items, prefix, is_last, show_types):

        new_prefix = prefix + (self.indent_str if is_last else self.connector_str)
        
        for i, item in enumerate(items):
            branch = self.last_branch_str if i == len(items) - 1 else self.branch_str
            
            if isinstance(item, (Param, Local)):
                
                item_str = f"{item.name}: {item.type}" if hasattr(item, 'name') and hasattr(item, 'type') else str(item)
                print(f"{prefix}{branch}{item_str}")
            elif isinstance(item, str):
                # result types
                print(f"{prefix}{branch}{item}")
            else:
                # print("type of item in body: " + str(type(item).__name__))
                # print("item in body: " + str(item))
                # Complex items
                print(f"{prefix}{branch}{type(item).__name__}")
                self._print_node(item, new_prefix, i == len(items) - 1, show_types)
    
    def _print_object(self, obj, prefix, is_last, show_types):
        """Print generic object properties"""
        new_prefix = prefix + (self.indent_str if is_last else self.connector_str)
        
        # Get all non-private attributes
        attrs = [(k, v) for k, v in vars(obj).items() if not k.startswith('_') and v is not None]
        
        for i, (key, value) in enumerate(attrs):
            branch = self.last_branch_str if i == len(attrs) - 1 else self.branch_str
            
            if isinstance(value, (str, int, float, bool)) or value is None:

                print(f"{prefix}{branch}{key}: {value}")
            elif isinstance(value, list):

                if value:
                    print(f"{prefix}{branch}{key}")
                    self._print_node(value, new_prefix, i == len(attrs) - 1, show_types)
            else:
                # Complex objects
                print(f"{prefix}{branch}{key}")
                self._print_node(value, new_prefix, i == len(attrs) - 1, show_types)
    
    def _format_operand(self, operand, show_types):
        """Format an operand for display"""
        if isinstance(operand, (CONST, ID, TYPE, STRING)):
            return f"{type(operand).__name__}({operand.value})"
        elif isinstance(operand, str):
            return operand
        elif hasattr(operand, 'op'):
            return f"{operand.op}"
        else:
            return str(operand)


class EnhancedASTPrinter(ASTPrinter):
    def __init__(self, use_colors=True, max_depth=None):
        # super().__init__()
        self.indent_str = "    "
        self.connector_str = "│   "
        self.branch_str = "├── "
        self.last_branch_str = "└── "
        self.use_colors = use_colors
        self.max_depth = max_depth
        # self.current_depth = 0
        
        # ANSI color codes
        self.colors = {
            'Module': '\033[1;34m',          # Bold blue
            
            'Memory': '\033[1;35m',          # Bold magenta
            'Global': '\033[0;33m',          # Yellow
            'Function': '\033[1;32m',        # Bold green
                'Param': '\033[0;32m',       # Green
                'Local': '\033[0;33m',       # Yellow
                
            'Export': '\033[1;33m',          # Bold yellow
            
            'Instruction': '\033[1;36m',     # Bold cyan
                'Operand': '\033[1;33m',     # Bold Yellow

            'Type': '\033[0;36m',            # Cyan
            'Reset': '\033[0m'               # Reset
        }
    
    def _colorize(self, text, color_key):

        if self.use_colors and color_key in self.colors:
            return f"{self.colors[color_key]}{text}{self.colors['Reset']}"
        return text
    
    def print_ast(self, ast, show_types=False):

        # self.current_depth = 0
        if isinstance(ast, Module):
            print(self._colorize("Module", 'Module'))
            self._print_module(ast, "", show_types)
        else:
            self._print_node(ast, "", True, show_types)
    
    def _print_module(self, module, prefix, show_types):
        # Depth checking
        # if self.max_depth is not None and self.current_depth >= self.max_depth:
        #     print(f"{prefix}{self.last_branch_str}...")
        #     return
            
        # self.current_depth += 1
        self._print_module_or(module, prefix, show_types)
        # self.current_depth -= 1
    
    def _print_module_or(self, module, prefix, show_types):

        children = []
        

        # print(module.mems)
        for i, mem in enumerate(module.mems):
            children.append(("Memory", mem, i == len(module.mems) - 1 and not module.funcs and not module.exports and not module.globs))
        

        for i, glob in enumerate(module.globs):
            children.append(("Global", glob, i == len(module.globs) - 1 and not module.funcs and not module.exports))
        

        for i, func in enumerate(module.funcs):
            children.append(("Function", func, i == len(module.funcs) - 1 and not module.exports))
        

        for i, export in enumerate(module.exports):
            children.append(("Export", export, i == len(module.exports) - 1))
        
        for i, (label, child, is_last) in enumerate(children):
            new_prefix = prefix + (self.indent_str if is_last else self.connector_str)
            branch = self.last_branch_str if is_last else self.branch_str
            
            # print(f"{prefix}{branch}{label}: {getattr(child, 'name', '')}")
            # print("label : " + label)
            
            if label in ("Function", "Memory", "Global"):
                name_display = child.name if child.name else "[anonymous]"
                print(f"{prefix}{self.last_branch_str if is_last else self.branch_str}"
                      f"{self._colorize(label, label)}: {self._colorize(name_display, label)}")
            # elif label == "Memory":
            #     name_display = child.name if child.name else "[anonymous]"
            #     print(f"{prefix}{self.last_branch_str if is_last else self.branch_str}"
            #           f"{self._colorize(label, label)}: {self._colorize(name_display, label)}")
            else:   # Export
                # pass
                name_display = child.value if child.value else "[anonymous]"
                print(f"{prefix}{self.last_branch_str if is_last else self.branch_str}"
                      f"{self._colorize(label, label)}: {self._colorize(name_display, label)}")

            self._print_node(child, new_prefix, is_last, show_types)
            
    def _print_node(self, node, prefix, is_last, show_types):
        
        if isinstance(node, Memory):
            self._print_memory(node, prefix, is_last, show_types)
        elif isinstance(node, Func):
            self._print_function(node, prefix, is_last, show_types)
        elif isinstance(node, Export):
            self._print_export(node, prefix, is_last, show_types)
        elif isinstance(node, (Instruction, ControlFlowInstruction)):
            self._print_instruction(node, prefix, is_last, show_types)
        elif isinstance(node, list):    # Body
            self._print_list(node, prefix, is_last, show_types)
        # elif hasattr(node, '__dict__'):
        #     self._print_object(node, prefix, is_last, show_types)
            
    def _print_function(self, func, prefix, is_last, show_types):

        # name_display = func.name if func.name else "[anonymous]"
        # print(f"{prefix}{self.last_branch_str if is_last else self.branch_str}"
        #       f"{self._colorize('Function', 'function')}: {self._colorize(name_display, 'function')}")
        
        new_prefix = prefix + (self.indent_str if is_last else self.connector_str)
        self._print_function_details(func, new_prefix, show_types)
    
    def _print_function_details(self, func, prefix, show_types):

        params = ", ".join([f"{p.name}: {self._colorize(p.type, 'Type')}" 
                           for p in func.params]) if func.params else "none"
        results = ", ".join([self._colorize(r, 'Type') for r in func.results]) if func.results else "void"
        
        print(f"{prefix}{self.branch_str}Signature: ({params}) -> {results}")
        
        if func.locals:
            locals_str = ", ".join([f"{l.name}: {self._colorize(l.type, 'Type')}" 
                                  for l in func.locals])
            print(f"{prefix}{self.branch_str}Locals: {locals_str}")
        
        if func.body:
            print(f"{prefix}{self.last_branch_str}Body:")
            body_prefix = prefix + self.indent_str
            # self._print_node(func.body, body_prefix, True, show_types)
            self._print_list(func.body, body_prefix, True, show_types)

    def _print_instruction(self, instr, prefix, is_last, show_types):
        # print("op : " + str(instr.op) + " operands : " + str(instr.operands)) #TODO: Usage for Debug
        # instr_name = getattr(instr, 'op', type(instr).__name__)
        instr_name = type(instr).__name__
        # print(instr_name) #TODO: Usage for Debug
        colored_instr = self._colorize(instr_name, 'Instruction')
        
        if hasattr(instr, 'operands') and instr.operands:
            print(f"{prefix}{self.branch_str}{colored_instr}")
            new_prefix = prefix + (self.indent_str if is_last else self.connector_str)
            self._print_operands(instr.operands, new_prefix, show_types)
        else:
            print(f"{prefix}{self.last_branch_str if is_last else self.branch_str}{colored_instr}")
    
    def _print_list(self, items, prefix, is_last, show_types):

        new_prefix = prefix + (self.indent_str if is_last else self.connector_str)
        
        for i, item in enumerate(items):
            branch = self.last_branch_str if i == len(items) - 1 else self.branch_str
            
            if isinstance(item, (Param, Local)):
                # Special handling for parameters and locals
                item_str = f"{item.name}: {item.type}" if hasattr(item, 'name') and hasattr(item, 'type') else str(item)
                print(f"{prefix}{branch}{item_str}")
            elif isinstance(item, str):
                # result types
                colored_item = self._colorize(item, 'Operand')
                # TODO: Actually colored item here
                print(f"{prefix}{branch}{colored_item}")
            else:
                # print("type of item in body: " + str(type(item).__name__))    #TODO: Usage for Debug
                # print("item in body: " + str(item))
                # Complex items
                colored_item = self._colorize(str(item), 'Instruction')
                if isinstance(item, (_if, _loop)):
                    name_display = item.name if item.name else "[anonymous]"
                    # print(f"{prefix}{self.last_branch_str if is_last else self.branch_str}"
                    print(f"{prefix}{branch}{colored_item}"
                          f": {self._colorize(name_display, 'Type')}")
                else:
                    print(f"{prefix}{branch}{colored_item}")
                # self._print_node(item, new_prefix, i == len(items) - 1, show_types)
                # print("item.operands : " + str(item.operands))
                
                # if item and item.operands is not None:
                #     self._print_list(item.operands, new_prefix, i == len(items) - 1, show_types)
                # else:
                #     self._print_node(item, new_prefix, i == len(items) - 1, show_types)
                if hasattr(item, 'operands') and item.operands:
                    self._print_list(item.operands, new_prefix, i == len(items) - 1, show_types)
                else:
                    self._print_list([], new_prefix, i == len(items) - 1, show_types)
                    
    def _print_operands(self, operands, prefix, show_types):

        if isinstance(operands, dict):
            for i, (key, value) in enumerate(operands.items()):
                if value:
                    is_last = i == len(operands) - 1
                    branch = self.last_branch_str if is_last else self.branch_str
                    print(f"{prefix}{branch}{key.capitalize()}:")
                    self._print_node(value, prefix + self.indent_str, is_last, show_types)
        else:
            # for i, operand in enumerate(operands):
            #     is_last = i == len(operands) - 1
            #     branch = self.last_branch_str if is_last else self.branch_str
            #     operand_str = self._format_operand(operand, show_types)
            #     print(f"{prefix}{branch}{operand_str}")
            
            for i, operand in enumerate(operands):
                is_last = i == len(operands) - 1
                branch = self.last_branch_str if is_last else self.branch_str
                operand_str = self._format_operand(operand, show_types)
                # print(f"{prefix}{branch}{operand_str}")
                self._print_node(operand, prefix + self.indent_str, is_last, show_types)