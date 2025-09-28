(module
  (func $foo (param $a i32) (result i32)
    (i32.div_s)
  )
  (export "foo" (func $foo))
)
