# Mixer

> Can you reverse this obfuscated boi ? 


Files provided:
* mixer: ELF64 file

In this program we have to enter the correct password.

Let's analyze `mixer` with `r2`.
The only function is `entry0`:

![alt text](img/screen_001.png?raw=true "r2")
 
There aren't other functions...there is just other machine code next to `entry0` but it isn't so important, it's just I/O.

With so few instructions where is the trick? It is in the beginning of `entry0`:
```sh
│           0x00401000      b80a000000     mov eax, 0xa
│           0x00401005      48bf00006000.  movabs rdi, segment.LOAD1   ; 0x600000
│           0x0040100f      be00001000     mov esi, 0x100000
│           0x00401014      ba07000000     mov edx, 7
│           0x00401019      0f05           syscall
```
The `syscall` number is `10`, so it is `mprotect`. Take a look at the `man`:
```
        #include <sys/mman.h>
        int mprotect(void *addr, size_t len, int prot);

       mprotect() changes the access protections for the calling process's
       memory pages containing any part of the address range in the interval
       [addr, addr+len-1].  addr must be aligned to a page boundary.

       prot is a combination of the following access flags: PROT_NONE or a
       bitwise-or of the other values in the following list:

       PROT_NONE
              The memory cannot be accessed at all.

       PROT_READ
              The memory can be read.

       PROT_WRITE
              The memory can be modified.

       PROT_EXEC
              The memory can be executed.
```

Interesting, in this case `mprotect` is used to allow READ, WRITE, and EXECUTION in the block of memory from `0x600000` to `0x6fffff`. So, the real program is hidden into this portion of memory located in `.stack` segment.

Then the execution flow is totally redirected to the hidden istructions (`0x610000`).
Start analyzing them:
```
;-- rsi:
            0x00610000      6a2b           push 0x2b                   ; '+' ; 43
            0x00610002      1f             invalid
            0x00610003      b804000000     mov eax, 4
            ;-- rip:
            0x00610008      bb01000000     mov ebx, 1
            0x0061000d      6a10           push 0x10                   ; 16
            0x0061000f      6872643a20     push 0x203a6472             ; 'rd: '
            0x00610014      687373776f     push 0x6f777373             ; 'sswo'
            0x00610019      6872207061     push 0x61702072             ; 'r pa'
            0x0061001e      68456e7465     push 0x65746e45             ; 'Ente'
            0x00610023      89e1           mov ecx, esp
            0x00610025      ba14000000     mov edx, 0x14               ; 20
            0x0061002a      cd80           int 0x80
            0x0061002c      b871026100     mov eax, 0x610271
            0x00610031      b900010000     mov ecx, 0x100              ; 256
        ┌─> 0x00610036      31db           xor ebx, ebx
        ╎   0x00610038      28cb           sub bl, cl
        ╎   0x0061003a      881c18         mov byte [rax + rbx], bl
        └─< 0x0061003d      e2f7           loop 0x610036
            0x0061003f      ba47016100     mov edx, 0x610147
            0x00610044      bf0a000000     mov edi, 0xa
            0x00610049      be71016100     mov esi, 0x610171
            0x0061004e      b900010000     mov ecx, 0x100              ; 256
            0x00610053      31db           xor ebx, ebx
        ┌─> 0x00610055      39fb           cmp ebx, edi
       ┌──< 0x00610057      7c02           jl 0x61005b
       │╎   0x00610059      31db           xor ebx, ebx
       └──> 0x0061005b      8a241a         mov ah, byte [rdx + rbx]
        ╎   0x0061005e      8826           mov byte [rsi], ah
        └─< 0x00610060      4643e2f1       loop 0x610055
            0x00610064      bf71026100     mov edi, 0x610271
            0x00610069      31db           xor ebx, ebx
            0x0061006b      81ee00010000   sub esi, 0x100              ; 256
            0x00610071      31c0           xor eax, eax
            0x00610073      b900010000     mov ecx, 0x100              ; 256
        ┌─> 0x00610078      8a1406         mov dl, byte [rsi + rax]
        ╎   0x0061007b      00d3           add bl, dl
        ╎   0x0061007d      8a1407         mov dl, byte [rdi + rax]
        ╎   0x00610080      00d3           add bl, dl
        ╎   0x00610082      8a1407         mov dl, byte [rdi + rax]
        ╎   0x00610085      8a341f         mov dh, byte [rdi + rbx]
        ╎   0x00610088      883407         mov byte [rdi + rax], dh
        ╎   0x0061008b      88141f         mov byte [rdi + rbx], dl
        └─< 0x0061008e      40e2e7         loop 0x610078
            0x00610091      b803000000     mov eax, 3
            0x00610096      bb00000000     mov ebx, 0
            0x0061009b      6a00           push 0
            0x0061009d      6a00           push 0
            0x0061009f      6a00           push 0
            0x006100a1      6a00           push 0
            0x006100a3      6a00           push 0
            0x006100a5      6a00           push 0
            0x006100a7      6a00           push 0
            0x006100a9      6a00           push 0
            0x006100ab      89e1           mov ecx, esp
            0x006100ad      ba20000000     mov edx, 0x20               ; 32
            0x006100b2      cd80           int 0x80
            0x006100b4      b800000000     mov eax, 0
            0x006100b9      89ce           mov esi, ecx
            0x006100bb      bf71076100     mov edi, 0x610771
        ┌─> 0x006100c0      668b1406       mov dx, word [rsi + rax]
        ╎   0x006100c4      66891407       mov word [rdi + rax], dx
        ╎   0x006100c8      4083f820       cmp eax, 0x20               ; 32
        └─< 0x006100cc      75f2           jne 0x6100c0
            0x006100ce      be71076100     mov esi, 0x610771
            0x006100d3      bf71026100     mov edi, 0x610271
            0x006100d8      ba71036100     mov edx, 0x610371
            0x006100dd      31c0           xor eax, eax
            0x006100df      31db           xor ebx, ebx
            0x006100e1      b920000000     mov ecx, 0x20               ; 32
        ┌─> 0x006100e6      51             push rcx
        ╎   0x006100e7      0fb6c8         movzx ecx, al
        ╎   0x006100ea      fec1           inc cl
        ╎   0x006100ec      52             push rdx
        ╎   0x006100ed      8a340f         mov dh, byte [rdi + rcx]
        ╎   0x006100f0      00f3           add bl, dh
        ╎   0x006100f2      8a141f         mov dl, byte [rdi + rbx]
        ╎   0x006100f5      88140f         mov byte [rdi + rcx], dl
        ╎   0x006100f8      88341f         mov byte [rdi + rbx], dh
        ╎   0x006100fb      00f2           add dl, dh
        ╎   0x006100fd      0fb6d2         movzx edx, dl
        ╎   0x00610100      8a             invalid
        ╎   0x00610101      14             invalid
        ╎   0x00610102      17             invalid
        ╎   0x00610103      8a0c06         mov cl, byte [rsi + rax]
        ╎   0x00610106      30d1           xor cl, dl
        ╎   0x00610108      5a             pop rdx
        ╎   0x00610109      880c02         mov byte [rdx + rax], cl
        ╎   0x0061010c      4059           pop rcx
        └─< 0x0061010e      e2d6           loop 0x6100e6
            0x00610110      b900000000     mov ecx, 0
            0x00610115      b800000000     mov eax, 0
            0x0061011a      be51016100     mov esi, 0x610151
            0x0061011f      bf71036100     mov edi, 0x610371
        ┌─> 0x00610124      8a1c0e         mov bl, byte [rsi + rcx]
        ╎   0x00610127      8a140f         mov dl, byte [rdi + rcx]
        ╎   0x0061012a      30d3           xor bl, dl
        ╎   0x0061012c      30d8           xor al, bl
        ╎   0x0061012e      4183f920       cmp r9d, 0x20               ; 32
        └─< 0x00610132      75f0           jne 0x610124
            0x00610134      83ec08         sub esp, 8
            0x00610137      c74424043300.  mov dword [rsp + 4], 0x33   ; '3'
            0x0061013f      c70424951040.  mov dword [rsp], 0x401095   ; [0x401095:4]=0x7400f883
            0x00610146      cb             retf
```

the code is too much, so I'll try to resume:
1. many calculations have been made in the portion of memory in range `0x610171` - `0x610371`, and is calculated the real "encrypted" password (stored in 32 bytes starting from `0x610151`). It is: `0x84, 0xd3, 0xb8, 0xca, 0xe2, 0x36, 0x63, 0x17, 0xc5, 0xae, 0x30, 0x7f, 0xd5, 0xd9, 0x10, 0xcf, 0xfa, 0x41, 0x8a, 0xa0, 0xbb, 0x1d, 0xdb, 0x84, 0x62, 0xe2, 0xa6, 0x36, 0x1d, 0xb9, 0x1c, 0x8b`.
2. 32 Byte of text (password) are requested in input. They are stored in `0x610771`.
3. The entered password is ecrypted:
The Password is XORed with these bytes (32 bytes starting from `0x610271`): `0xf4, 0xbc, 0xcb, 0xaf, 0x8b, 0x52, 0x0c, 0x79, 0xbe, 0xcd, 0x00, 0x1b, 0xb0, 0x86, 0x7d, 0xa6, 0x82, 0x72, 0xf8, 0xda, 0xc1, 0x42, 0xba, 0xf6, 0x07, 0xbd, 0xd1, 0x05, 0x74, 0xcb, 0x78, 0xf6`.
You can read these values by placing a breakpoint on `0x00610103` and looking at `dl` for every  iteration, as shown in figure:


![alt text](img/screen_002.png?raw=true "r2")


4. The encrypted password entered by user is compared with the encrypted real password.

So, we have:
1. One operand of XOR ( Portion of memory, located in `0x610271` against which the password is compared )
2. Result of XOR (real encrypted password in `0x610151`)

Because of XOR is reversible, we can XOR first operand with result, to get second operand (the plaintext password):
```python
from pwn import *

#a XOR b = c

a = [ 0xf4, 0xbc, 0xcb, 0xaf, 0x8b, 0x52, 0x0c, 0x79, 0xbe, 0xcd, 0x00, 0x1b, 0xb0, 0x86, 0x7d, 0xa6, 0x82, 0x72, 0xf8, 0xda, 0xc1, 0x42, 0xba, 0xf6, 0x07, 0xbd, 0xd1, 0x05, 0x74, 0xcb, 0x78, 0xf6 ]
c = [ 0x84, 0xd3, 0xb8, 0xca, 0xe2, 0x36, 0x63, 0x17, 0xc5, 0xae, 0x30, 0x7f, 0xd5, 0xd9, 0x10, 0xcf, 0xfa, 0x41, 0x8a, 0xa0, 0xbb, 0x1d, 0xdb, 0x84, 0x62, 0xe2, 0xa6, 0x36, 0x1d, 0xb9, 0x1c, 0x8b ]
b = ""

#calculating b (b is equal to: a XOR c)
for n in range(32):
	b += p8(a[n]^c[n])

print(b)
```

```sh
$   python exploit.py
poseidon{c0de_mix3rzz_are_w3ird}
$   python exploit.py | ./mixer
Enter password: Password is correct :)
```

So, the flag is `poseidon{c0de_mix3rzz_are_w3ird}`





