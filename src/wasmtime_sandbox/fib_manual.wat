(module
  (func $fib (param $n i32) (result i32)
    (if (result i32)
        (i32.lt_s (local.get $n)
                  (i32.const 2))
        (then (local.get $n))
        ;; recursive branch spawns _two_ calls to $fib; not ideal
        (else (i32.add (call $fib (i32.sub (local.get $n)
                                           (i32.const 1)))
                       (call $fib (i32.sub (local.get $n)
                                           (i32.const 2)))))))

  (export "fib" (func $fib)))