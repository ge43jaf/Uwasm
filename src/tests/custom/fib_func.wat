(module
  ;;(import "console" "log" (func $log (param i32)))
  (func $fib_func (param $fib i32) (param $a i32) (param $b i32)
    
    (local $nextTerm i32)

    (local.get $fib)
    (i32.const 1)
    (i32.lt_s)
    if
      ;;(local.get $fib)
      ;;(call $log)
      ;;(local.get $fib)
      return
    end

    ;; ;; Stack: a=0, b=1
    ;; (i32.const 0)
    ;; (local.set $a)
    (local.get $b)
    (i32.const 1)
    (i32.lt_s)
    if
      (i32.const 1)
      (local.set $b)
      (local.get $b)
      (call $log)
    else 
      (local.get $a)
      (call $log)
    end
    
    (local.get $fib)
    (i32.const 1)
    (i32.sub)
    (local.set $fib)

    (local.get $a)
    (local.get $b)
    (i32.gt_s)
    if
      (local.get $fib)
      (local.get $a)
      (call $log)
      (local.get $a)
      (local.get $b)
      (local.get $a)
      (i32.add)
      (call $fib_func)
    else
      (local.get $fib)
      (local.get $a)
      (local.get $b)
      (i32.add)
      (local.get $b)
      (local.get $b)
      (call $log)
      (call $fib_func)
    end
    
    
  )

  (export "fib" (func $fib_func))
)
