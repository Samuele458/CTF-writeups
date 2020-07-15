from pwn import *


r = remote( "insanity1.chujowyc.tf", 4004 )
r.sendlineafter( "2+2: ", "4" )
r.sendlineafter( "now?\n", "81" )


print( r.recv() )

r.close()