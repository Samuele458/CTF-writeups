# Insanity1

> nc insanity1.chujowyc.tf 4004

---
Let's connect to `nc insanity1.chujowyc.tf 4004`:

```sh
$   nc insanity1.chujowyc.tf 4004
Welcome chCTF Sanity Check :D
What is 2+2:
```

The aswer to the first question is (obviously) `4`:

```
nc insanity1.chujowyc.tf 4004
Welcome chCTF Sanity Check :D
What is 2+2: 4
What number between 0 and 100 am I thinking about right now?
```

Now it's more difficult. To find the correct number i wrote a script (test_1.py):

```python
from pwn import *

for i in range( 0, 101 ):
	r = remote( "insanity1.chujowyc.tf", 4004 )
	r.sendlineafter( "2+2: ", "4" )

	r.sendlineafter( "now?\n", str(i) )
	
	#check if number is correct or not
	if r.recvline() != "Invalid answer Bye\n":
		print( "Correct Number: " + str(i)  )
		break;

	r.close()
```

By executing this script we will know that the correct number is `81`.

So, let's proceed:
```sh
$   nc insanity1.chujowyc.tf 4004
Welcome chCTF Sanity Check :D
What is 2+2: 4
What number between 0 and 100 am I thinking about right now?
81
xD xD The answer to the next one is in front of your eyes xD xD
What is 2+2: 
```

Uhm...the answer isn't `4`, but it says that the answer is in front of our eyes. 
In facts, not all output is correcly printed to the screen. Let's write a script to discover the correct number (test_2.py):
```python
from pwn import *

r = remote( "insanity1.chujowyc.tf", 4004 )
r.sendlineafter( "2+2: ", "4" )
r.sendlineafter( "now?\n", "81" )

print( r.recv() )

r.close()
```

```sh
$    python exploit.py 
[+] Opening connection to insanity1.chujowyc.tf on port 4004: Done
xD xD The answer to the next one is in front of your eyes xD xD
The answer is 42123 ;)                         What is 2+2: 
[*] Closed connection to insanity1.chujowyc.tf port 4004
```

So the answer is `42123`.
Now we know all 'secret' numbers:

```sh
nc insanity1.chujowyc.tf 4004
Welcome chCTF Sanity Check :D
What is 2+2: 4
What number between 0 and 100 am I thinking about right now?      
81        
xD xD The answer to the next one is in front of your eyes xD xD   
What is 2+2: 42123   
Congratulations the flag is: chCTF{Ez3_cha113ng3}
```

And the flag is `chCTF{Ez3_cha113ng3}`

