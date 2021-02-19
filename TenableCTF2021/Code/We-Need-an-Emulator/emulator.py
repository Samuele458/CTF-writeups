#!/usr/bin/python3

#global variables to handle TRX and DRX
DRX = b""
TRX = b"GED\x03hG\x15&Ka =;\x0c\x1a31o*5M"

#returns the value of a register
def readRegister( reg ):
    global DRX
    global TRX
    if reg == "DRX":
        return DRX
    elif reg == "TRX":
        return TRX

def writeRegister( reg, value ):   
    global DRX
    global TRX 
    if reg == "DRX":
        DRX = value
    elif reg == "TRX": 
        TRX = value

def isRegister( token ):
    if token == "TRX" or token == "DRX":
        return True
    else:
        return False

def execCommand( cmd_tokens ):
    global TRX
    global DRX
    cmd = cmd_tokens[0]
    if( cmd == "MOV" ):
        reg = cmd_tokens[1]
        if isRegister(cmd_tokens[2]):
            value = readRegister(cmd_tokens[2])
        else:
            value = bytes(cmd_tokens[2],encoding="raw_unicode_escape")
            value = value[1:len(value)-1]

        writeRegister( reg, value )
    elif( cmd == "REVERSE" ):
        writeRegister( cmd_tokens[1], readRegister(cmd_tokens[1])[::-1] )
    elif( cmd == "XOR" ):
        xor = bytes([a ^ b for a, b in zip(readRegister(cmd_tokens[1]), readRegister(cmd_tokens[2]))])
        if len(TRX) > len(DRX):
            writeRegister( cmd_tokens[1], xor + TRX[len(DRX):])
        elif len(DRX) > len(TRX):
            writeRegister( cmd_tokens[1], xor + DRX[len(TRX):])

file = open('./Crypto.asm', 'r')

line = file.readline()
while line:
    line_tokens = line.split()
    print(line_tokens)
    execCommand(line_tokens)
    
    line = file.readline()

file.close()

print("T:",readRegister("TRX"))
print("D:",readRegister("DRX"))
