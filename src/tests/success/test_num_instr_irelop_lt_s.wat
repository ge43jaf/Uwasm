(module
  (func $foo (param $a i32) (param $b i32) (result i32)
    (local.get $a)
    (local.get $b)
    (i32.lt_s)
  )
  (export "foo" (func $foo))
)
