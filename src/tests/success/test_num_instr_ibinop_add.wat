(module
  (func $foo (param $a i32) (result i32)
    local.get $a
    local.get $a
    (i32.add)
  )
  (export "foo" (func $foo))
)
