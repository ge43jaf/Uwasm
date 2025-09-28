(module
  ;; (func (export "fahrenheit_to_celsius") (param $fahrenhit i32) (result i32)
  (func $fahrenheit_to_celsius 
    (export "fahrenheit_to_celsius") 
    (param $fahrenheit i32) 
    (result i32)
    (local.get $fahrenheit)
	  (i32.const 32  )
    (i32.sub)
  
    (i32.const 5)
    (i32.mul)
    
    (i32.const 9)
    (i32.div_s)
  
  )

)
