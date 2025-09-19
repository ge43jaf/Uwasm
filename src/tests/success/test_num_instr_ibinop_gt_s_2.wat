(module
  (func $foo (param $a i32) (param $b i32) (result i32)
    (local.get $b)
    (local.get $a)
    (i32.gt_s)
  )
  (export "foo" (func $foo))
)
