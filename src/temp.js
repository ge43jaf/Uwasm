const importObject = {
  console: {
    log: (x) => console.log("WASM log:", x)
  }
};

// Assume `wasmModule` is already compiled using WebAssembly.Module
const wasmInstance = new WebAssembly.Instance(wasmModule, importObject);

const { init } = wasmInstance.exports;

for (let i = 0; i < 10; i++) {
  init();
}
