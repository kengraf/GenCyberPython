# Python3 program to illustrate Rail Fence Cipher
# This code was written to support a Python security lab
# in UNH's 2021 GenCyber camp

def encrypt( text, railCount, offset):

    # fix wild railCount values
    if railCount < 2: railCount = 2
    railCount = railCount % (len(text)//2)
    cycleSize = railCount + (railCount-2)

    # fix wild offset values
    if offset < 0: offset = 0
    offset = offset % cycleSize

    rails = []
    for i in range(railCount):
        rails.append("")
    
    # loop over all characters in string
    for i in range(len(text)):
        pc = (i+offset) % cycleSize
        if pc >= railCount:
            # running back up the rail
            rails[cycleSize - pc] += text[i]
        else:
            rails[pc] += text[i]
            
    # Concatenate the rails
    cipher = ""
    for i in range(railCount):
        cipher += rails[i]
    return cipher

def decrypt( cipher, railCount, offset ):
    railoffset = []
    railsize = []
    
    # fix wild railCount values
    if railCount < 2: railCount = 2
    railCount = railCount % (len(cipher)//2)
    cycleSize = railCount + (railCount-2)

    # fix wild offset values
    if offset < 0: offset = 0
    offset = offset % cycleSize
    
    o = len(cipher) + offset
    fullcycles = o // cycleSize

    # Determine rail counts
    for i in range(railCount):
        railoffset.append(0)
        if (i==0) or (i+1==railCount):
            railsize.append(fullcycles)
        else:
            railsize.append(fullcycles*2)

    # Reduce frontend of rails due to offset
    j=0
    direction = 1
    for i in range(offset):
        railsize[j] -= 1
        j += direction
        if j == railCount:
            direction = -1
            j -= 2
    
    # Add to backend of rails for offset & remaining
    j = 0
    direction = 1
    pc = o % cycleSize     
    for i in range(pc):
        railsize[j] += 1
        j += direction
        if j == railCount:
            direction = -1
            j -= 2
    
    # Calculate the rail sizes
    for i in range(1,railCount):
        railoffset[i] = railoffset[i-1] + railsize[i-1]
        
    text = ""
    j=0
    direction = 1
    for i in range(o):
        # Consume text only after the offset is reduced to 0
        if offset == 0:
            k = railoffset[j]
            railoffset[j] += 1
            text += cipher[k]
        else:
            offset -= 1
        
        # Move to the next rail
        j += direction
        if j == railCount:
            direction = -1
            j -= 2
        if j == 0:
            direction = 1
            
    return text

def selfTest():
    # Loop rail count and offsets
    for rails in range(0,8):
        for offset in range(0,9):
            text = "abcdefghijklmnopqrstuvwxyz"
            cipher = encrypt(text, rails, offset)
            dtext = decrypt(cipher, rails, offset)
            if text != dtext:
                print(text + ":" + cipher + ":" + dtext)
                return False
    
    # Try a couple of quotes with space and different lengths
    text = "'Service over self' - Tulsi Gabbard"
    cipher = encrypt(text, 3, 0)
    dtext = decrypt(cipher, 3, 0)
    if text != dtext:
        print(text + ":" + cipher + ":" + dtext)
        return False
    
    text = "Ask not what your country can do for you, ask what you can do for your country---JFK"
    cipher = encrypt(text, 24, 14)
    dtext = decrypt(cipher, 24, 14)
    if text != dtext:
        print(text + ":" + cipher + ":" + dtext)
        return False
    
    return True

# Module test code
if __name__ == "__main__":
    print( "Tests passed" if selfTest() else "Failed" )
