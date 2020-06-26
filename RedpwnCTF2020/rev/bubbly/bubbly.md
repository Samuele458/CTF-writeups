# bubbly

> It never ends

> nc 2020.redpwnc.tf 31039

Files provided:
* bubbly:   ELF64 file

Let's analyze it with `Ghidra`.
This is the `main`:

![alt text](img/bubbly-chl-1.png?raw=true "Ghidra")


In `main` function there is a `while` loop, from which we can exit by entering an integer greater than 8.

Our goal is to execute `print_flag()`, so we want to make `pass=true`, so function `check()` must return `true`.

This is the `check` function:

![alt text](img/bubbly-chl-2.png?raw=true "Ghidra")

`nums` is a `unsigned int` array of 10 elements:

![alt text](img/bubbly-chl-3.png?raw=true "Ghidra")

function `check()` returns `true` if `nums` is sorted in ascending order, so to get the flag we need to sort `nums` inside `main` function.

We have to take a look at these three lines:
```c
17    nums[i] = nums[i] ^ nums[i + 1];
18    nums[i + 1] = nums[i + 1] ^ nums[i];
19    nums[i] = nums[i] ^ nums[i + 1];
```
at first glance they seem very cryptic, but they are simply a way to swap `nums[i]` with `nums[i+1]`, so we can use them to create a sort of `bubble-sort`.

Let's do this in python:
```python
from pwn import *

#array nums
nums = [ 0x1, 0xA, 0x3, 0x2, 0x5, 0x9, 0x8, 0x7, 0x4, 0x6 ]

r = remote("2020.redpwnc.tf", 31039)	#used to get the flag
#r = process("./bubbly") 		#used to test exploit in local

r.recvuntil("hand?\n")

n = len(nums) 
for i in range(n-1): 
	for j in range(0, n-i-1): 
		if nums[j] > nums[j+1] : 
			#swap nums[i] with nums[i+1].
			nums[j] = nums[j] ^ nums[j+1]
			nums[j+1] = nums[j+1] ^ nums[j]
			nums[j] = nums[j] ^ nums[j+1]
			#instead of this we can obviously use:
			#hold = nums[j]
			#nums[j] = nums[j+1]
			#nums[j+1] = hold 			
			
			#sending current swap index
			r.sendline( str(j) )
			print(j)

#sending a number > 8, to exit loop and get flag
r.sendline("9")

print(r.recvall())
```

...And here's the flag:

`flag{4ft3r_y0u_put_u54c0_0n_y0ur_c011ege_4pp5_y0u_5t1ll_h4ve_t0_d0_th15_57uff}`
