(module
  (func $foo (param $a i32) (result i32)
    (i32.add)
  )
  (export "foo" (func $fo)) ; Name error
)
