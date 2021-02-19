#!/usr/bin/python3

#global variables to handle TRX and DRX registers
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

#write value on a specified register
def writeRegister( reg, value ):   
    global DRX
    global TRX 
    if reg == "DRX":
        DRX = value
    elif reg == "TRX": 
        TRX = value

#check if specified token is a register or not
def isRegister( token ):
    if token == "TRX" or token == "DRX":
        return True
    else:
        return False

#execute command by passing tokens of a line
def execCommand( cmd_tokens ):
    global TRX
    global DRX

    cmd = cmd_tokens[0]

    if( cmd == "MOV" ):
        #executing MOV <DEST> <SOURCE>
        #token pos [0] [1]    [2] 
        reg = cmd_tokens[1]

        #check if <SOURCE> is register or literal
        if isRegister(cmd_tokens[2]):
            value = readRegister(cmd_tokens[2])
        else:
            value = bytes(cmd_tokens[2],encoding="raw_unicode_escape")
            value = value[1:len(value)-1]

        #writing <SOURCE> value into <DEST>
        writeRegister( reg, value )


    elif( cmd == "REVERSE" ):
        #executing REVERSE <REG>
        #token pos [0]     [1]
        writeRegister( cmd_tokens[1], readRegister(cmd_tokens[1])[::-1] )
        

    elif( cmd == "XOR" ):
        #executing XOR <DEST> <SOURCE
        #token pos [0] [1]    [2]
        #it computes:   DEST = DEST ^ SOURCE
        xor = bytes([a ^ b for a, b in zip(readRegister(cmd_tokens[1]), readRegister(cmd_tokens[2]))])
        if len(TRX) > len(DRX):
            writeRegister( cmd_tokens[1], xor + TRX[len(DRX):])
        elif len(DRX) > len(TRX):
            writeRegister( cmd_tokens[1], xor + DRX[len(TRX):])

def main():
    file = open('./Crypto.asm', 'r')

    #reading file line by line
    line = file.readline()
    while line:
        line_tokens = line.split()
        execCommand(line_tokens)
        line = file.readline()

    file.close()

    #flag
    print(readRegister("TRX"))

if __name__ == "__main__":
    main()

