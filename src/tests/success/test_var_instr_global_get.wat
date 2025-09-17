(module
  (global $global_1 i32 (i32.const 42))
  (func (export "addTwo") (param i32 i32) (result i32)
    global.get 0
    local.get 1
    i32.add))
