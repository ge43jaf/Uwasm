(module
  (func
    i32.const 0 
    (if
      (
        (i32.const 1)
        ;; (call $log) ;; should log '1'
      )
      (else
        (i32.const 0)
        ;; (call $log) ;; should log '0'
      )
    )
  )

;;   (start 1) ;; run the first function automatically
)
