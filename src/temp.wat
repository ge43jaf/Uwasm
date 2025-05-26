(module
  ;; Import a logging function from the host environment
  (import "console" "log" (func $log (param i32)))

  ;; Function demonstrating i32.const
  (func $use_const
    i32.const 42
    call $log
  )

  ;; Function demonstrating unary operation: i32.clz (count leading zeros)
  (func $use_iunop
    i32.const 16      ;; Binary: 00000000 00000000 00000000 00010000
    i32.clz           ;; Expected result: 27 leading zeros
    call $log
  )

  ;; Function demonstrating binary operation: i32.add
  (func $use_ibinop
    i32.const 10
    i32.const 20
    i32.add           ;; 10 + 20 = 30
    call $log
  )

  ;; Function demonstrating relational operation: i32.lt_u (unsigned less than)
  (func $use_irelop
    i32.const 5
    i32.const 10
    i32.lt_u          ;; 5 < 10 → 1 (true)
    call $log
  )
  
  (func $init
    call $use_const
    call $use_iunop
    call $use_ibinop
    call $use_irelop
  )
  
  ;; Automatically invoked when the module is instantiated, after tables and memories have been initialized.
  (start $init)
  ;; Export functions for external invocation
  (export "use_const" (func $use_const))
  (export "use_iunop" (func $use_iunop))
  (export "use_ibinop" (func $use_ibinop))
  (export "use_irelop" (func $use_irelop))
  (export "init" (func $init)) 
)
