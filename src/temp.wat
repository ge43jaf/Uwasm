(module
  (import "console" "log" (func $log (param i32)))

  (func $init_log   ;; ← name this function properly
    i32.const 13
    call $log
  )
  
  ;; Automatically invoked when the module is instantiated, after tables and memories have been initialized.
  (start $init_log)

  (export "init_log" (func $init_log)) 
)
