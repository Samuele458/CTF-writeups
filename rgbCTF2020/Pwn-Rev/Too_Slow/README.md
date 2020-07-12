# Too Slow

> I've made this flag decryptor! It's super secure, but it runs a little slow.



Files provided:
* a.out:   ELF64 file

Let's run `a.out`:

foto

As we can see execution never ends.

So, what we can do is analyzing `a.out` with `radare2`.

This is the `main`:
foto

We have to take a look at these instructions:
```sh
           0x000012df      e873ffffff     call sym.getKey
           0x000012e4      89c7           mov edi, eax
           0x000012e6      e89efeffff     call sym.win
```

The return value of `sym.getKey` is passed to `sym.win`.

`sym.getKey` probably performs computationally too long calculations to generate the key, but let's analyze this function to understand if we can discover the real key:
foto

We can see that there is a main loop. `var_8h` is the counter firstly initialyzed to 0, and incremented by 1 at each iteration.
Take a look at the last 5 instructions:
```sh
│      ╎└─> 0x000012a1      817df8221d5d.  cmp dword [var_8h], 0x265d1d22
│      └──< 0x000012a8      76be           jbe 0x1268
│           0x000012aa      8b45f8         mov eax, dword [var_8h]
│           0x000012ad      5d             pop rbp
└           0x000012ae      c3             ret
```
The loop execution runs until the counter is below or equal `0x265d1d22`, so it means the loop ends when `var_8h` is uqual to `0x265d1d23`.

Because of, at the end of the function, `var_8h` is copied in `eax` and so returned, it means that the correct key value is `0x265d1d23`.

Let's change execution with radare2:
foto

I used:
* `aaa` to analyze the executable file
* `dcu main` to execute until main
* `dso 11` to execute until `call sym.getKey`
* `pd 3` to see the address of `call sym.win`
* `dr rip = 0x5640a240c2e6` to jump over `sym.getKey` without executing it.
* `dr rdi = 0x265d1d23` to set in `rdi` the correct key value (`0x265d1d23`)
* `dc` to continue execution

And here's the flag:
`rgbCTF{pr3d1ct4bl3_k3y_n33d5_no_w41t_cab79d}`






