(module
  
  (func $foo)
  (func $bar)(export "fo" (func $foo))
  (export "ba" (func $bar))
  
)
