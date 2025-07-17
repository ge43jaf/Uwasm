(module
  (import "console" "log" (func $log (param i32)))

  (func $sort_array_imperative(export "sort_array_imperative") (param $len i32)
    (local $i i32)
    (local $j i32)
    (local $addr1 i32)
    (local $addr2 i32)
    (local $cmp i32)
    (local $tmp1 i32)
    (local $tmp2 i32)

    i32.const 0
    local.set $i
    loop $outer
      local.get $i
      local.get $len
      i32.const 1
      i32.sub
      i32.lt_u
      if
        i32.const 0
        local.set $j
        loop $inner
          local.get $j
          local.get $len
          local.get $i
          i32.sub
          i32.const 1
          i32.sub
          i32.lt_u
          if
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

            local.get $addr1
            i32.load
            local.get $addr2
            i32.load
            i32.gt_s
            if
              local.get $addr1
              i32.load
              local.set $tmp1

              local.get $addr2
              i32.load
              local.set $tmp2

              local.get $addr1
              local.get $tmp2
              i32.store

              local.get $addr2
              local.get $tmp1
              i32.store
            end

            local.get $j
            i32.const 1
            i32.add
            local.set $j
            br $inner
          end
        end
      
        local.get $i
        i32.const 1
        i32.add
        local.set $i
        br $outer
      end
    end
  )

  (func $init
    i32.const 0 i32.const 3 i32.store
    i32.const 4 i32.const 2 i32.store
    i32.const 8 i32.const 4 i32.store
    i32.const 12 i32.const 1 i32.store
    i32.const 16 i32.const 5 i32.store
    
    i32.const 5
    call $sort_array_imperative

    i32.const 0  i32.load call $log
    i32.const 4  i32.load call $log
    i32.const 8  i32.load call $log
    i32.const 12 i32.load call $log
    i32.const 16 i32.load call $log
  )
  (memory $mem 1)
  (export "memory" (memory $mem))
  (export "init" (func $init))
)
