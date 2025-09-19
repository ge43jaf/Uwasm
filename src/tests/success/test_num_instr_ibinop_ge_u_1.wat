(module
  (func $foo (param $a i32) (result i32)
    (local.get $a)
    (local.get $a)
    (i32.ge_u)
  )
  (export "foo" (func $foo))
)
