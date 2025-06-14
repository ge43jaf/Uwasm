# WebAssembly Text Format (WAT) Parser + Interpreter with Log + Loop Support

import os
import pprint

# === Tokenization and Parsing ===
def tokenize(wat):
    wat = wat.replace("(", " ( ").replace(")", " ) ")
    tokens = wat.split()
    return [t for t in tokens if not t.startswith(';;') and not t.startswith('memory') and not t.startswith('fill')]

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

# === Simple WASM Interpreter Core ===
class WasmInterpreter:
    def __init__(self):
        self.locals = {}
        self.globals = {}
        self.stack = []
        self.functions = {}
        self.output = []
        self.memory = {}
        self.labels = []
    
    def exec_block(self, block, label_env=None):
        i = 0
        while i < len(block):
            instr = block[i]
            result = self.exec_instruction(instr, label_env)
            if isinstance(result, tuple) and result[0] == 'br':
                target = result[1]
                if label_env and target in label_env:
                    # Short-circuit execution to label target
                    return ('br', target)
                else:
                    return result
            i += 1




    def exec_instruction(self, instr):
        # print("                    [DEBUG] Executing instruction:", instr)
        if isinstance(instr, list):
            if not instr:
                return
            opcode = instr[0]
            args = instr[1:]
        else:
            opcode = instr
            args = []

        if opcode.startswith(';;'):
            print("                    [INFO] Skipping comment:", opcode)
            return

        try:
            if opcode == 'i32.const':
                if not args:
                    raise IndexError("Missing value for i32.const")
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
            elif opcode == 'i32.load':
                addr = self.stack.pop()
                self.stack.append(self.memory.get(addr, 0))
            elif opcode == 'i32.store':
                val = self.stack.pop()
                addr = self.stack.pop()
                self.memory[addr] = val
            elif opcode == 'local.set':
                var = args[0]
                val = self.stack.pop()
                self.locals[var] = val
            elif opcode == 'local.get':
                var = args[0]
                self.stack.append(self.locals.get(var, 0))
            elif opcode == 'local.tee':
                var = args[0]
                val = self.stack[-1]
                self.locals[var] = val
            elif opcode == 'global.set':
                var = args[0]
                val = self.stack.pop()
                self.globals[var] = val
            elif opcode == 'global.get':
                var = args[0]
                self.stack.append(self.globals.get(var, 0))
            elif opcode == 'call':
                fname = args[0]
                if fname == '$log':
                    val = self.stack.pop()
                    # print(f"🖨️  log: {val}")
                else:
                    return self.run_function(fname)
            elif opcode == 'return':
                return self.stack.pop()
            elif opcode == 'nop':
                return
            
            elif opcode == 'block':
                label = args[0] if args and isinstance(args[0], str) else None
                body = args[1:] if label else args
                block_labels = label_env.copy() if label_env else {}
                if label:
                    block_labels[label] = True
                self.exec_block(body, block_labels)
            elif opcode == 'loop':
                label = args[0] if args and isinstance(args[0], str) else None
                body = args[1:] if label else args
                loop_labels = label_env.copy() if label_env else {}
                if label:
                    loop_labels[label] = True
                while True:
                    result = self.exec_block(body, loop_labels)
                    if isinstance(result, tuple) and result[1] == label:
                        continue  # repeat loop
                    break
            elif opcode == 'br':
                label = args[0]
                return ('br', label)
            elif opcode == 'br_if':
                label = args[0]
                cond = self.stack.pop()
                if cond:
                    return ('br', label)
            
        
            elif opcode == 'if':
                cond = self.stack.pop()
                if cond:
                    for instr in args:
                        self.exec_instruction(instr)
                return
            else:
                if opcode.isnumeric():
                    return
                # print(f"[WARN] Unsupported instruction: {opcode}")
        except IndexError:
            print(f"[ERROR] Stack underflow in instruction: {opcode} {args}")

    def run_function(self, fname):
        func = self.functions.get(fname)
        # print(f"🔍 Running function: {fname}")
        if not func:
            raise RuntimeError(f"Function {fname} not found")
        for instr in func['body']:
            result = self.exec_instruction(instr)
            if isinstance(result, tuple) and result[0] == 'br':
                break
        return result

    def register_function(self, name, body):
        self.functions[name] = {'body': body}

# === Load and parse WAT ===
wat_path = "functions.wat"
if os.path.isfile(wat_path):
    with open(wat_path, "r", encoding="utf-8") as f:
        wat_code = f.read()
else:
    wat_code = """
    (module
      (func $init
        i32.const 7
        i32.const 3
        i32.add
        return
      )
      (export "init" (func $init))
    )
    """

tokens = tokenize(wat_code)
ast = parse_tokens(tokens)
# print("📜 Parsed AST:", pprint.pformat(ast))
# === Extract and register functions ===
def extract_functions(ast):
    functions = {}
    if ast[0] != 'module':
        raise ValueError("Expected module")
    for form in ast[1:]:
        if isinstance(form, list) and form[0] == 'func':
            # Get the function name (or anonymous)
            name = form[1] if isinstance(form[1], str) else '<anon>'

            # Build body by skipping signature/local declarations
            body = []
            for item in form[2:]:
                # If this is a (param …), (result …) or (local …) form, skip it
                if isinstance(item, list) and item and item[0] in ('param', 'result', 'local'):
                    continue
                # Otherwise, it’s an actual instruction (string or nested list)
                body.append(item)

            functions[name] = body

    return functions


interpreter = WasmInterpreter()
funcs = extract_functions(ast)
# print("📜 Extracted Functions:", pprint.pformat(funcs))
for fname, body in funcs.items():
    interpreter.register_function(fname, body)

result = interpreter.run_function('$init')
print("\n✅ Final Result:", result)
print("📦 Stack after execution:", interpreter.stack)
print("🧠 Locals:", interpreter.locals)
print("🌍 Globals:", interpreter.globals)
print("🧮 Memory:", interpreter.memory)
