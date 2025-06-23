(module
  (import "console" "log" (func $log (param i32)))
  (func $fib (param $fib i32) (result i32)
    (local $a i32)
    (local $b i32)
    (local $nextTerm i32)

    local.get $fib
    i32.const 2
    i32.lt_s
    if
      local.get $fib
      return
    end

    ;; Stack: a=0, b=1
    i32.const 0
    local.set $a
    local.get $a
    call $log

    i32.const 1
    local.set $b
    local.get $b
    call $log

    loop $loop
      local.get $a
      local.get $b
      i32.add
      local.set $nextTerm
      local.get $nextTerm
      call $log
    
      local.get $b
      local.set $a
    
      local.get $nextTerm
      local.set $b
    
      local.get $fib
      i32.const 1
      i32.sub
      local.set $fib
    
      local.get $fib
      i32.const 0
      i32.gt_s
      br_if $loop
    end
    
    local.get $b
  )

  (export "fib" (func $fib))
)
