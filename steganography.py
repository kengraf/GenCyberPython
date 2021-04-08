# Python3 program to illustrate Iamge based stebanogrphy
# This code was written to support a Python security lab
# in UNH's 2021 GenCyber camp

# Read/Write images using OpenCV-Python.
# It is a library of Python bindings designed to solve computer vision problems. 
import cv2
import numpy

EOM = "<EOM>" # you can use any string as the end of message delimeter

def messageToBinary(message):
    if type(message) == str:
        return ''.join([ format(ord(i), "08b") for i in message ])
    elif type(message) == bytes or type(message) == numpy.ndarray:
        return [ format(i, "08b") for i in message ]
    elif type(message) == int or type(message) == numpy.uint8:
        return format(message, "08b")
    else:
        raise TypeError("Input type not supported")


def hideData(image, secret_message, key):

    # calculate the maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("Maximum bytes to encode:", n_bytes)

    #Check if the number of bytes to encode is less than the maximum bytes in the image
    if len(secret_message) > n_bytes:
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")

    secret_message += EOM 
    keyColor = key[0]
    keyBit = 8 - int(key[1])
    
    data_index = 0
    # convert input data to binary format using messageToBinary() fucntion
    binary_secret_msg = messageToBinary(secret_message)

    data_len = len(binary_secret_msg) #Find the length of data that needs to be hidden
    for values in image:
        for pixel in values:
            # Break out of the loop once all the data is encoded
            if data_index >= data_len:
                break
            
            # convert RGB values to binary format
            r, g, b = messageToBinary(pixel)

            if( keyColor == 'R' or keyColor == 'r' ):
                x = r[:keyBit] + binary_secret_msg[data_index] + r[keyBit+1:];
                pixel[0] = int(x, 2)
            if( keyColor == 'G' or keyColor == 'g' ):
                x = g[:keyBit] + binary_secret_msg[data_index] + r[keyBit+1:];
                pixel[1] = int(x, 2)
            if( keyColor == 'B' or keyColor == 'b' ):
                x = b[:keyBit] + binary_secret_msg[data_index] + r[keyBit+1:];
                pixel[2] = int(x, 2)
                
            data_index += 1
            
    return image

def showData(image, key):

    binary_data = ""
    keyColor = key[0]
    keyBit = 8 - int(key[1])
    
    for values in image:
        for pixel in values:
            r, g, b = messageToBinary(pixel)
            if( keyColor == 'R' or keyColor == 'r' ):
                binary_data += r[keyBit]
            if( keyColor == 'G' or keyColor == 'g' ):
                binary_data += g[keyBit]
            if( keyColor == 'B' or keyColor == 'b' ):
                binary_data += b[keyBit]

    # convert from bits to characters
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == EOM: #check if we have reached the end of message
            break

    # remove the delimeter and return the original hidden message
    return decoded_data[:-5] 

# hide 'data' in 'image_name' 
# 'key' format is 'XY', X = is R,G, or B: Y is bit position 1 for LSB
def encode(image_name, data, key): 
    image = cv2.imread(image_name) 

    #details of the image
    print("The shape of the image is: ",image.shape) #check the shape of image to calculate the number of bytes in it

    if (len(data) == 0): 
        raise ValueError('Data is empty')

    encoded_image = hideData(image, data, key) # call the hideData function to hide the secret message into the selected image
    return encoded_image
    
# Decode image
def decode(image_name, key ):
    image = cv2.imread(image_name) #read the image
    text = showData(image, key)
    return text

# wirte the encoded image data to filename
def write(filename, encoded_image ):
    return cv2.imwrite(filename, encoded_image)
    
    
# Try simple message on small image, changing the low red bit
def selfTest(): 
    message = "Into the valley of death rode the 600 hundred"
    coverFilename = "Charge600.jpg"
    secretFilename = "secret.png"
    key = 'R1'
    
    secretData = encode( coverFilename, message, key )
    if( len(secretData) == 0 ): return False
    
    success = write(secretFilename, secretData )
    if( success == False ):
        print("failed to write file: " + secretFilename )
        return False

    # Reverse the process
    dtext = decode( secretFilename, key )
    return dtext == message

# Module test code
if __name__ == "__main__":
    print( "Tests passed" if selfTest() else "Failed" )
