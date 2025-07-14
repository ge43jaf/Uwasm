(module
  (import "console" "log" (func $log (param i32)))


  (func $swap (param $a i32) (param $b i32)
    (local $tmp1 i32)
    (local $tmp2 i32)
    local.get $a
    i32.load
    local.set $tmp1

    local.get $b
    i32.load
    local.set $tmp2

    local.get $a
    local.get $tmp2
    i32.store

    local.get $b
    local.get $tmp1
    i32.store
  )

  ;; Compare two values (functional part)
  (func $greater_than (param $a i32) (param $b i32) (result i32)
    local.get $a
    local.get $b
    i32.gt_s
  )

  ;; Imperative sorting function (Bubble Sort) that takes array length as parameter
  (func $sort_array_imperative(export "sort_array_imperative") (param $len i32)
    (local $i i32)
    (local $j i32)
    (local $addr1 i32)
    (local $addr2 i32)
    (local $cmp i32)

    i32.const 0
    local.set $i
    block $outer_break
    loop $outer
      local.get $i
      local.get $len
      i32.const 1
      i32.sub
      i32.ge_u
      br_if $outer_break

      i32.const 0
      local.set $j
      block $inner_break
      loop $inner
        local.get $j
        local.get $len
        i32.const 1
        i32.sub
        i32.ge_u
        br_if $inner_break

        ;; compute addresses
        local.get $j
        i32.const 4
        i32.mul
        local.set $addr1

        local.get $j
        i32.const 1
        i32.add
        i32.const 4
        i32.mul
        local.set $addr2

        ;; load elements
        local.get $addr1
        i32.load

        local.get $addr2
        i32.load

        call $greater_than
        local.set $cmp

        local.get $cmp
        if
          local.get $addr1
          local.get $addr2
          call $swap
        end

        local.get $j
        i32.const 1
        i32.add
        local.set $j
        br $inner
      end
      end ;; end inner loop
    
      local.get $i
      i32.const 1
      i32.add
      local.set $i
      br $outer
    end
    end ;; end outer loop
  )

  (func $init
    i32.const 0
    i32.const 3
    i32.store
    i32.const 4
    i32.const 2
    i32.store
    i32.const 8
    i32.const 4
    i32.store
    i32.const 12
    i32.const 1
    i32.store
	i32.const 16
    i32.const 5
    i32.store
    
    i32.const 5
    call $sort_array_imperative

    i32.const 0
    i32.load
    call $log
    i32.const 4
    i32.load
    call $log
    i32.const 8
    i32.load
    call $log
    i32.const 12
    i32.load
    call $log
    i32.const 16
    i32.load
    call $log
  )
  (memory $mem 1)
  (export "memory" (memory $mem))
  (export "init" (func $init))
 
)
