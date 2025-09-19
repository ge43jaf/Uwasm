(module
  (func $foo (param $a i32) (param $b i32) (result i32)
    (local.get $b)
    (local.get $a)
    (i32.lt_s)
  )
  (export "foo" (func $foo))
)
