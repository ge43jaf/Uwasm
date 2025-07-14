(module
  (func $foo (param $a i32) (result i32)
    (local.get $a)
  )
  (export "foo" (func $foo))
)
