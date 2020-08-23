
# BEGINNER
> easy

> Dust off the cobwebs, let's reverse!


Files provided:
* a.out: ELF64 file

In this program we have to enter the correct flag:

```sh
$  ./a.out
Flag: AAAAAAAAAAA
FAILURE
```

Let's analyze `a.out` with `radare2` and `ghidra`:
![r2](https://github.com/Samuele458/CTF-writeups/blob/master/GoogleCTF2020/Reversing/BEGINNER/img/screen_01.png?raw=true)

Let's try to understand what does `main` do.

 The flag is stored in a string of 16 chars (15+end char): 
```sh
0x000010a2      488d3d620f00.  lea rdi, str.15s            ; 0x200b ; "%15s" ; const char *format
e8b2ffffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
```

...but the most important instructions are these:
```sh
0x000010be      660f380005a9.  pshufb xmm0, xmmword [obj.SHUFFLE]
0x000010c7      660ffe05912f.  paddd xmm0, xmmword [obj.ADD32] ; arg7
0x000010cf      660fef05792f.  pxor xmm0, xmmword [obj.XOR] ; arg7
0x000010d7      0f29442410     movaps xmmword [var_28h], xmm0 ; arg7
```
These are `SIMD` instructions (in this case, in `xmm0` is stored the flag entered by user). 

 1. `pshufb` performs a shuffle of all 16 bytes (`xmm0` is a 128-bit long register), using the second operand as a mask.
 2.  `paddd` adds the second operand to the first (destination), 32 bit at a time.
 3. `pxor` performs a bitwise xor of both operands and store the result to the first operand.
 4. `movaps`store the content of an `xmm` register to memory.
 

So, the flag entered by user, is firstly shuffled using `SHUFFLE` as mask.
Content of `SHUFFLE`
```sh
02 06 07 01 05 0b 09 0e 03 0f 04 08 0a 0c 0d 00
```
It means that the element 0 is replaced with the one in position 2, etc...

Then, the shuffled text is used in the `paddd`, so it is added to the content of `ADD32`.
Content of `ADD32`:
```sh
ef be ad de ad de e1 fe 37 13 37 13 66 74 63 67
```

and then the result is XORed with `XOR`:
Content of `XOR`:
```sh
76 58 b4 49 8d 1a 5f 38 d4 23 f8 34 eb 86 f9 aa
```
The result of `pxor` is compared with the original flag entered by user. If they are equal, it means that the flag is correct.
There is also another comparison: the first 4 chars of flag must be `"CTF{"`, So, we know the flag format.

to reproduce all execution flow, i wrote some lines in python:
```python
def shuffle( in_str ):
	new_pos = [ 0x2, 0x6, 0x7, 0x1, 0x5, 0xB, 0x9, 0xE, 0x3, 0xF, 0x4, 0x8, 0xA, 0xC, 0xD, 0x0 ]
	out_str = []
	for x in range( 16 ):
		out_str.append(ord(in_str[new_pos[x]]))
	return out_str

def toInt32( num_array ):
	num = 0
	num += num_array[3] * 0x1000000
	num += num_array[2] * 0x10000
	num += num_array[1] * 0x100
	num += num_array[0]
	return num & 0xffffffff

def fromInt32( num ):
	num = num & 0xffffffff
	num_array = []
	num_array.append(num%0x100)
	num_array.append((num%0x10000)//0x100)
	num_array.append((num//0x10000)%0x100)
	num_array.append(num//0x1000000)
	return num_array

def add( in_str ):
	values = [ 0xEF, 0xBE, 0xAD, 0xDE, 0xAD, 0xDE, 0xE1, 0xFE, 0x37, 0x13, 0x37, 0x13, 0x66, 0x74, 0x63, 0x67 ]
	out_str = []
	for x in range( 0, 16, 4 ):
		out_str.extend(fromInt32(toInt32(values[x:x+4])+toInt32(in_str[x:x+4])))

	return out_str

def xor( in_str ):
	values= [ 0x76, 0x58, 0xb4, 0x49, 0x8d, 0x1A, 0x5F, 0x38, 0xD4, 0x23, 0xF8, 0x34, 0xEB, 0x86, 0xF9, 0xAA ]
	out_str = []
	for x in range( 16):
		out_str.append(in_str[x]^values[x])
	return out_str
	
result = xor(add(shuffle("CTF{AAAAAAAAAA}\x00")))  
print("Result of shuffle, add, and xor:")
for x in result:  
   print( hex(x) )
```

Now it's time to focus on how to solve this challenge.
We know just a small part of the flag (`"CTF{"`), but because of shuffled bytes, every output char is evaluated by starting from another char pointed by its corresponding `SHUFFLE` value.

For example:
```
We know that:
input_string[3] -> 7B		the char at pos 3 is 7B
SHUFFLE[8] -> 3			the char at pos 8 is exchanged with the char at pos 3

So let's calculate output_string[8]:
( 7B + ADD32[8] ) ^ XOR[8] =
( 7B + 37 ) ^ D4 = 66  ('f')
in facts, the char at pos 8, inside the correct flag, is 'f'.
```
I wrote a python function to do it for all chars:
```python
def getFlag():
	pos_changed = [ 0x2, 0x6, 0x7, 0x1, 0x5, 0xB, 0x9, 0xE, 0x3, 0xF, 0x4, 0x8, 0xA, 0xC, 0xD, 0x0 ]
	add_val = [ 0xEF, 0xBE, 0xAD, 0xDE, 0xAD, 0xDE, 0xE1, 0xFE, 0x37, 0x13, 0x37, 0x13, 0x66, 0x74, 0x63, 0x67 ]
	xor_val= [ 0x76, 0x58, 0xb4, 0x49, 0x8d, 0x1A, 0x5F, 0x38, 0xD4, 0x23, 0xF8, 0x34, 0xEB, 0x86, 0xF9, 0xAA ]

	flag = []
	for x in range(16):
		flag.append(-1)	

	flag[0] = ord('C')
	flag[1] = ord('T')
	flag[2] = ord('F')
	flag[3] = ord('{')

	current_32bit = 0

	for cycle in range(16):
		for pos in range(16):
			if pos % 4 == 0:
				current_32bit = pos
			if flag[pos] == -1 and flag[pos_changed[pos]] != -1:
				flag[pos] = (((flag[pos_changed[pos]] + add_val[pos])%0x100)^xor_val[pos])
				if (flag[pos_changed[pos]] + add_val[pos]) > 0x100 and pos+1 < current_32bit+4 :
					add_val[pos+1] += 1

	return ''.join(chr(c) for c in flag)
```
The string returned by `getFlag()` is `CTF{S1MDf0rM3!}`

So, the correct flag is `CTF{S1MDf0rM3!}`. I checked it using [exploit.py](exploit.py)
