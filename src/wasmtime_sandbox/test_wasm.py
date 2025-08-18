import wasmtime.loader
import sys
sys.path.append(".")
sys.path.append("target\wasm32-wasi\debug") #add path of wasm module
import fib_manual #use manual wat file in python
import wasm_lib #import wasm module generate from rust
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--num', type=int, required=True)
args = parser.parse_args()
fib_wasm = wasm_lib.fib(args.num)
print("from wasm fibonachi of",args.num," is:",fib_wasm)

fib_wat = fib_manual.fib(args.num)
print("from wat fibonachi of",args.num," is:",fib_wat)