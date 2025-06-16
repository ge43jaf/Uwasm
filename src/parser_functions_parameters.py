# WebAssembly Text Format (WAT) Parser + Interpreter with proper instruction parameter handling

import os
import pprint
from collections import defaultdict

# === Tokenization and Parsing ===
import re

def tokenize(wat):
    # Remove multi-line comments (; ... ;)
    wat = re.sub(r"\(\;.*?\;\)", "", wat, flags=re.DOTALL)
    # Remove single-line comments ;; ... (whole line)
    wat = re.sub(r";;.*", "", wat)
    # Now tokenize as usual
    wat = wat.replace("(", " ( ").replace(")", " ) ")
    tokens = wat.split()
    return tokens

def parse_tokens(tokens):
    if not tokens:
        return None
    token = tokens.pop(0)
    if token == '(':
        subexpr = []
        while tokens and tokens[0] != ')':
            subexpr.append(parse_tokens(tokens))
        if tokens:
            tokens.pop(0)
        return subexpr
    elif token == ')':
        raise SyntaxError("Unexpected )")
    else:
        return token

# === Improved WASM Interpreter Core ===
class WasmInterpreter:
    def __init__(self):
        self.globals = {}
        self.stack = []
        self.functions = {}
        self.output = []
        self.memory = defaultdict(int)
        self.locals = {}

    def exec_block(self, block, label_env=None):
        i = 0
        while i < len(block):
            instr = block[i]
            result = self.exec_instruction(instr, label_env)
            if isinstance(result, tuple) and result[0] == 'br':
                target = result[1]
                if label_env and target in label_env:
                    return ('br', target)
                else:
                    return result
            i += 1

    def validate_instruction(self, opcode, args):
        """Validate instruction has correct number of parameters"""
        if opcode not in WASM_INSTRUCTIONS:
            return False
        
        expected_params = WASM_INSTRUCTIONS[opcode]
        if expected_params == 'var':
            return True  # Variable number of params
        
        if isinstance(expected_params, tuple):
            # Range of acceptable parameters
            min_params, max_params = expected_params
            return min_params <= len(args) <= max_params
        else:
            # Exact number of parameters
            return len(args) == expected_params

    def exec_instruction(self, instr, label_env=None):
        if isinstance(instr, list):
            if not instr:
                return
            opcode = instr[0]
            args = instr[1:]
        else:
            opcode = instr
            args = []

        if opcode.startswith(';;'):
            return

        # Validate instruction parameters
        if not self.validate_instruction(opcode, args):
            print(f"[ERROR] Invalid parameters for {opcode}: expected {WASM_INSTRUCTIONS[opcode]}, got {len(args)}")
            return

        try:
            # Numeric instructions
            if opcode == 'i32.const':
                self.stack.append(int(args[0]))
            elif opcode == 'i32.add':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a + b)
            elif opcode == 'i32.sub':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a - b)
            elif opcode == 'i32.mul':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a * b)
            elif opcode == 'i32.div_s':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(int(a / b))
            elif opcode == 'i32.ge_u':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(1 if a >= b else 0)
            elif opcode == 'i32.gt_s':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(1 if a > b else 0)

            # Memory instructions
            elif opcode == 'i32.load':
                offset = 0
                align = 4
                for arg in args:
                    if arg.startswith('offset='):
                        offset = int(arg.split('=')[1])
                    elif arg.startswith('align='):
                        align = int(arg.split('=')[1])
                addr = self.stack.pop() + offset
                self.stack.append(self.memory[addr])
            elif opcode == 'i32.store':
                offset = 0
                align = 4
                for arg in args:
                    if arg.startswith('offset='):
                        offset = int(arg.split('=')[1])
                    elif arg.startswith('align='):
                        align = int(arg.split('=')[1])
                val = self.stack.pop()
                addr = self.stack.pop() + offset
                self.memory[addr] = val

            # Variable instructions
            elif opcode == 'local.set':
                self.locals[args[0]] = self.stack.pop()
            elif opcode == 'local.get':
                self.stack.append(self.locals[args[0]])
            elif opcode == 'local.tee':
                val = self.stack[-1]
                self.locals[args[0]] = val
            elif opcode == 'global.set':
                self.globals[args[0]] = self.stack.pop()
            elif opcode == 'global.get':
                self.stack.append(self.globals[args[0]])

            # Control flow
            elif opcode == 'call':
                if args[0] == '$log':
                    print(f"🖨️  log: {self.stack.pop()}")
                else:
                    return self.run_function(args[0])
            elif opcode == 'return':
                return self.stack.pop() if self.stack else None
            elif opcode == 'nop':
                return
            elif opcode == 'block':
                label = args[0] if args and isinstance(args[0], str) and not args[0].startswith('result') else None
                body = args[1:] if label else args
                block_labels = label_env.copy() if label_env else {}
                if label:
                    block_labels[label] = True
                self.exec_block(body, block_labels)
            elif opcode == 'loop':
                label = args[0] if args and isinstance(args[0], str) and not args[0].startswith('result') else None
                body = args[1:] if label else args
                loop_labels = label_env.copy() if label_env else {}
                if label:
                    loop_labels[label] = True
                while True:
                    result = self.exec_block(body, loop_labels)
                    if isinstance(result, tuple) and result[1] == label:
                        continue
                    break
            elif opcode == 'br':
                return ('br', args[0])
            elif opcode == 'br_if':
                if self.stack.pop():
                    return ('br', args[0])
            elif opcode == 'if':
                cond = self.stack.pop()
                then_branch = []
                else_branch = []
                branch = then_branch
                for item in args:
                    if item == 'else':
                        branch = else_branch
                    else:
                        branch.append(item)
                for instr in (then_branch if cond else else_branch):
                    self.exec_instruction(instr, label_env)
            else:
                if opcode.isnumeric():
                    return
                print(f"[WARN] Unsupported instruction: {opcode}")
        except IndexError:
            print(f"[ERROR] Stack underflow in instruction: {opcode} {args}")
        except Exception as e:
            print(f"[ERROR] Error executing {opcode}: {str(e)}")

    def run_function(self, fname, args=None):
        func = self.functions.get(fname)
        if not func:
            raise RuntimeError(f"Function {fname} not found")
        
        self.locals = func['locals'].copy()
        if args:
            for param, val in zip(func['params'], args):
                self.locals[param[0]] = val
        
        for instr in func['body']:
            result = self.exec_instruction(instr)
            if isinstance(result, tuple) and result[0] == 'br':
                break
        return result

    def register_function(self, name, body, params, locals_):
        processed_body = []
        i = 0
        while i < len(body):
            item = body[i]
            # Skip any remaining param/local declarations
            if isinstance(item, list) and item[0] in ('param', 'local'):
                i += 1
                continue
                
            if isinstance(item, str) and item in WASM_INSTRUCTIONS:
                # Get instruction and its parameters
                instr = [item]
                i += 1
                param_info = WASM_INSTRUCTIONS[item]
                
                # Handle variable parameter counts
                if param_info == 'var':
                    while i < len(body) and not (isinstance(body[i], str) and body[i] in WASM_INSTRUCTIONS):
                        instr.append(body[i])
                        i += 1
                # Handle parameter ranges (min, max)
                elif isinstance(param_info, tuple):
                    min_params, max_params = param_info
                    params_collected = 0
                    while params_collected < max_params and i < len(body) and not (isinstance(body[i], str) and body[i] in WASM_INSTRUCTIONS):
                        instr.append(body[i])
                        i += 1
                        params_collected += 1
                # Handle exact parameter count
                else:
                    for _ in range(param_info):
                        if i < len(body) and not (isinstance(body[i], str) and body[i] in WASM_INSTRUCTIONS):
                            instr.append(body[i])
                            i += 1
                processed_body.append(instr)
            else:
                processed_body.append(item)
                i += 1
        
        self.functions[name] = {
            'body': processed_body,
            'params': params,
            'locals': {**{p[0]: 0 for p in params}, **{l[0]: 0 for l in locals_}}
        }

# WebAssembly instructions with their parameter counts
# Format: {instruction: param_count}
# 'var' means variable number of parameters
WASM_INSTRUCTIONS = {
    # Numeric instructions
    'i32.const': 1,
    'i32.add': 0,
    'i32.sub': 0,
    'i32.mul': 0,
    'i32.div_s': 0,
    'i32.ge_u': 0,
    'i32.gt_s': 0,
    
    # Memory instructions
    'i32.load': (0, 2),  # optional offset and align
    'i32.store': (0, 2),  # optional offset and align
    
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

# === Load and parse WAT ===
wat_path = "functions.wat"
if os.path.isfile(wat_path):
    with open(wat_path, "r", encoding="utf-8") as f:
        wat_code = f.read()
else:
    wat_code = """
    (module
      (func $init (param $x i32) (local $temp i32)
        (i32.const 10)
        (local.set $temp)
        (local.get $temp)
        (call $log)
        (i32.const 20)
        (i32.const 30)
        (i32.add)
        (call $log)
        (return)
      )
      (export "init" (func $init))
    )
    """

tokens = tokenize(wat_code)
ast = parse_tokens(tokens)

# === Extract and register functions ===
def extract_functions(ast):
    functions = {}
    if ast[0] != 'module':
        raise ValueError("Expected module")
    for form in ast[1:]:
        if isinstance(form, list) and form[0] == 'func':
            name = form[1] if isinstance(form[1], str) else '<anon>'
            
            # Extract params and locals
            params = []
            locals_ = []
            body_start = 2  # Skip 'func' and name
            
            # Process params and locals
            while body_start < len(form):
                item = form[body_start]
                if isinstance(item, list):
                    if item[0] == 'param':
                        params.append(item[1:])
                    elif item[0] == 'local':
                        locals_.append(item[1:])
                    else:
                        break  # Found start of actual body
                else:
                    break  # Found start of actual body
                body_start += 1
            
            # The rest is the function body
            body = form[body_start:]
            
            functions[name] = (body, params, locals_)
            print(f"🔍 Found function: {name} with params {params} and locals {locals_}")
    return functions

interpreter = WasmInterpreter()
funcs = extract_functions(ast)
print("📜 Extracted Functions:", pprint.pformat(funcs))
for fname, (body, params, locals_) in funcs.items():
    interpreter.register_function(fname, body, params, locals_)

# Run the init function
print("\n🏃‍♂️ Running program...")
result = interpreter.run_function('$init')
print("\n✅ Final Result:", result)
print("📦 Stack after execution:", interpreter.stack)
print("🧠 Locals:", interpreter.locals)
print("🌍 Globals:", interpreter.globals)
print("🧮 Memory:", dict(interpreter.memory))