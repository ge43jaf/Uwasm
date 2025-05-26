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

  (func $init
    call $test_const
    call $test_iunop
    call $test_ibinop
    call $test_irelop
  )
  
  ;; Automatically invoked when the module is instantiated, after tables and memories have been initialized.
  (start $init)

  (export "init" (func $init))
)
