(module
  (func $fib (param $n i32) (result i32)

    local.get $n
    i32.const 2
    i32.lt_s
    if (result i32)
      local.get $n
      return
    end

    ;; Stack: a=0, b=1
    i32.const 0
    i32.const 1

    ;; Loop: for i = n-2 downto 0
    local.get $n
    i32.const 2
    i32.sub
    loop $loop
      ;; stack: a b
      ;; compute a + b, push result -> new b
      ;; then slide old b (now top) down -> new a
      ;; a b
      ;; => a b a+b
      ;; => b a+b
      ;; swap: drop a, keep b and a+b
      ;; slide b as new a, a+b as new b
      ;; so just keep b, a+b

      ;; dup top two: a b → a b a b
      get_local $0 ;; reusing param register since no new locals allowed
      drop          ;; ignore actual value, placeholder
      ;; instead simulate with manual manipulation:
      ;; stack: a b → a b a b → a+b → b a+b
      ;; actual:
      ;; - duplicate top 2
      ;; - add
      ;; - swap for next iteration

      ;; Implement: a b → b a+b
      ;; do:
      ;; a b → a b → a+b → b a+b
      i32.add
      i32.swap

      ;; decrement loop counter
      local.get $n
      i32.const 2
      i32.sub
      i32.const 1
      i32.sub
      local.set $n

      local.get $n
      i32.const 0
      i32.gt_s
      br_if $loop
    end

    ;; result on top of stack
    i32.pop
  )

  (export "fib" (func $fib))
)
