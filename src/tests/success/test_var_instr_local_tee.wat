(module

  (func $main

    (local $var i32) ;; create a local variable named $var
    (i32.const 10) ;; load `10` onto the stack
    (local.tee $var) ;; set the $var to `10` and keep `10` on the stack
	  (local.set $var)

  )

)
