(module
  (import "console" "log" (func $log (param i32)))

  ;; i32.const test
  (func $test_const
    i32.const 42
    call $log
  )

  ;; i32 unary operations: clz, ctz, popcnt
  (func $test_iunop
    i32.const 16   ;; 16
    i32.clz                ;; Count leading zeros
    call $log

    i32.const 16
    i32.ctz                ;; Count trailing zeros
    call $log

    i32.const 1195
    i32.popcnt             ;; Count 1 bits (should be 4)
    call $log
  )

  ;; i32 binary operations
  (func $test_ibinop
    i32.const 15
    i32.const 3
    i32.add
    call $log

    i32.const 15
    i32.const 3
    i32.sub
    call $log

    i32.const -4
    i32.const 5
    i32.mul
    call $log

    ;; Signed division
    i32.const -15
    i32.const 4
    i32.div_s
    call $log

    ;; Unsigned division
    i32.const 15
    i32.const 4
    i32.div_u
    call $log

    ;; Signed remainder
    i32.const -15
    i32.const 4
    i32.rem_s
    call $log

    ;; Unsigned remainder
    i32.const 15
    i32.const 4
    i32.rem_u
    call $log

    ;; Bitwise ops
    i32.const 6
    i32.const 3
    i32.and
    call $log

    i32.const 6
    i32.const 3
    i32.or
    call $log

    i32.const 6
    i32.const 3
    i32.xor
    call $log

    ;; Shifts and rotations
    i32.const 1
    i32.const 3
    i32.shl
    call $log

    i32.const -16
    i32.const 2
    i32.shr_s
    call $log

    i32.const 16
    i32.const 2
    i32.shr_u
    call $log

    i32.const 1
    i32.const 2
    i32.rotl
    call $log

    i32.const 1
    i32.const 2
    i32.rotr
    call $log
  )

  ;; i32 relational operations (signed and unsigned)
  (func $test_irelop
    ;; eq and ne
    i32.const 10
    i32.const 10
    i32.eq
    call $log

    i32.const 10
    i32.const 20
    i32.ne
    call $log

    ;; lt_s and lt_u
    i32.const -1
    i32.const 0
    i32.lt_s
    call $log

    i32.const 1
    i32.const 2
    i32.lt_u
    call $log

    ;; gt_s and gt_u
    i32.const 10
    i32.const -5
    i32.gt_s
    call $log

    i32.const 3
    i32.const 2
    i32.gt_u
    call $log

    ;; le_s and le_u
    i32.const -1
    i32.const -1
    i32.le_s
    call $log

    i32.const 1
    i32.const 2
    i32.le_u
    call $log

    ;; ge_s and ge_u
    i32.const 3
    i32.const 3
    i32.ge_s
    call $log

    i32.const 5
    i32.const 5
    i32.ge_u
    call $log
  )
  
  
    
  ;; Demonstrate 'drop': discard a value
  (func $test_drop (export "test_drop")
    i32.const 100   ;; Push value 100
    drop            ;; Drop it
    i32.const 42    ;; Push 42
    call $log       ;; Output should be 42
  )

  ;; Demonstrate 'select': choose between two values based on a condition
  (func $test_select_true (export "test_select_true")
    i32.const 111   ;; val1
    i32.const 222   ;; val2
    i32.const 1     ;; condition ≠ 0 → select val1
    select
    call $log       ;; Output should be 111
  )

  (func $test_select_false (export "test_select_false")
    i32.const 111   ;; val1
    i32.const 222   ;; val2
    i32.const 0     ;; condition = 0 → select val2
    select
    call $log       ;; Output should be 222
  )

  

  ;; Define a mutable global variable
  (global $g (mut i32) (i32.const 10)) ;; initially 10

  ;; Use local.get, local.set, local.tee
  (func $test_local (export "test_local")
    (local $x i32)
    i32.const 42         ;; push value
    local.set $x         ;; $x = 42

    local.get $x         ;; push $x (42)
    call $log            ;; log 42

    i32.const 7
    local.tee $x         ;; $x = 7, keep 7 on stack
    call $log            ;; log 7

    local.get $x         ;; get $x again (should be 7)
    call $log            ;; log 7
  )

  ;; Use global.get and global.set
  (func $test_global (export "test_global")
    global.get $g        ;; Get initial global value (10)
    call $log            ;; log 10

    i32.const 99
    global.set $g        ;; Set global to 99

    global.get $g
    call $log            ;; log 99
  )
  
  
  
  ;; Declare a memory of 1 page (64KiB)
  (memory $mem 1)

  ;; Export memory so it can be inspected externally (optional)
  (export "memory" (memory $mem))

  ;; Store a value into memory at offset 0
  (func $store_value (export "store_value")
    i32.const 0        ;; memory offset
    i32.const 1234     ;; value to store
    i32.store          ;; store 1234 at memory[0..3]
  )

  ;; Load the value from memory at offset 0
  (func $load_value (export "load_value")
    i32.const 0        ;; memory offset
    i32.load           ;; load 4 bytes starting at offset 0
    call $log          ;; print loaded value (should be 1234)
  )

  ;; Store another value at offset 4 and load it
  (func $store_and_load_other (export "store_and_load_other")
    i32.const 4
    i32.const 5678
    i32.store

    i32.const 4
    i32.load
    call $log          ;; Should log 5678
  )
  
  
  
  ;; A simple function that returns a constant and uses return
  (func $give_value (result i32)
    i32.const 42
    return
  )

  ;; Demonstrate `nop`, `call`, and `if`
  (func $test_if_call (export "test_if_call")
    nop                   ;; does nothing
    i32.const 1           ;; condition = true
    if                   ;; if condition ≠ 0
      call $give_value   ;; call function and push 42
      call $log          ;; log 42
    end
  )

  ;; Demonstrate `loop`, `br_if`, and `br`
  (func $test_loop (export "test_loop")
    (local $i i32)
    i32.const 0
    local.set $i

    loop $main_loop
      local.get $i
      call $log         ;; log i
      local.get $i
      i32.const 3
      i32.eq
      br_if 1           ;; break out of loop if i == 3

      local.get $i
      i32.const 1
      i32.add
      local.set $i
      br $main_loop     ;; go back to loop
    end
  )

  ;; Use `br` to skip over code
  (func $test_br (export "test_br")
    block
      i32.const 123
      call $log         ;; log 123
      br 0              ;; skip the next instruction
      i32.const 999     ;; this is skipped
      call $log
    end
  )
  
  
  
  (func $init
    call $test_const
    call $test_iunop
    call $test_ibinop
    call $test_irelop
    
    call $test_drop
    call $test_select_true
    call $test_select_false
    
    call $test_local
    call $test_global
    
    call $store_value
    call $load_value
    call $store_and_load_other
    
    
    ;; Why error here, because of the return inside $give_value?
    ;; call $give_value
    call $test_if_call
    call $test_loop
    call $test_br
  )
  
  ;; Automatically invoked when the module is instantiated, after tables and memories have been initialized.
  (start $init)

  (export "init" (func $init))
)
