(module

  (global $global_1 i32 (i32.const 42))
  (memory $x 2)
  (global $global_2 i32 (i32.const 42))
  (func $foo)
  (func $bar)
  (export "foo" (func $foo))
  (export "bar" (func $bar))
)
