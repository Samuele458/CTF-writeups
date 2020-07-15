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