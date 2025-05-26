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


  (func $init
    call $test_const
    call $test_iunop
    call $test_ibinop
    call $test_irelop
    
    call $test_drop
    call $test_select_true
    call $test_select_false
  )
  
  ;; Automatically invoked when the module is instantiated, after tables and memories have been initialized.
  (start $init)

  (export "init" (func $init))
)
