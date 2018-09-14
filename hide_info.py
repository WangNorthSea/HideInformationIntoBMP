#coding:utf-8
import math
import numpy as np
import struct

FILE_HEADER_SIZE = 14 #standard size of file header
BMPINFO_HEADER_SIZE = 40 #standard size of bmpinfo header
LENGTH_FIELD_SIZE = 16 #size of occupancy in bmp fir the length of hidden data
INFO_UNIT_SIZE = 4 #size of occupancy in bmp for a byte of hidden data

# Read all bytes from a file.
def ReadAllFromFile(file_name):
    load_file = open(file_name, "rb")
    data = np.fromfile(load_file, dtype = np.ubyte)
    load_file.close()
    return data

# Write all data to a file.
def WriteAllToFile(data, file_name):
    save_file = open(file_name, "wb")
    for i in data:
        singleData = struct.pack("B", i)
        save_file.write(singleData)
    save_file.close()

# Output the bmp file
def ProduceImg(file_name, fh, bh, pixel_array):
    data = []
    for i in fh:
        data.append(i)
    for i in bh:
        data.append(i)
    for i in pixel_array:
        data.append(i)
    WriteAllToFile(data, file_name)

# Transform bytes to an integer in a little-endian way.
def _4byte2int(bs):
    count = 0
    loop = 0
    result = 0
    lastTwo = 0
    two0 = 0
    two1 = 0

    for i in range(0, 4):
        result = bs[loop] | 252 #252 = 11111100 step 1 finished
        lastTwo = bs[loop + 1] & 3 #3 = 00000011
        two0 = lastTwo << 2
        two1 = two0 | 243 #243 = 11110011
        result = result & two1 #step2 finished

        lastTwo = bs[loop + 2] & 3 #3 = 00000011
        two0 = lastTwo << 4
        two1 = two0 | 207 #207 = 11001111
        result = result & two1 #step3 finished

        lastTwo = bs[loop + 3] & 3 #3 = 00000011
        two0 = lastTwo << 6
        two1 = two0 | 63 #63 = 00111111
        result = result & two1 #all done

        count += result * math.pow(256, i)
        loop += 4
    
    return count

# Retrieve three parts of the bmp file: file header, bmpinfo header and pixel array. Note the bmp file may contain other parts after the pixel array.
def GetPartsOfBmp(file_name):
    bmp = ReadAllFromFile(file_name)
    file_header = bmp[0:14]
    bmpinfo_header = bmp[14:54]
    pixel_array = bmp[54:]
    return file_header, bmpinfo_header, pixel_array

# Hide information into the pixel array.
def HideText(hide_data, pixel_array):
    loop = 16
    inputTwo = 0
    inputLastTwo0 = 0
    inputLastTwo1 = 0
    p11 = 0
    length = len(hide_data)

    inputLastTwo1 = ((((length % (256 * 256 * 256)) % (256 * 256)) % 256) / 1) | 252 #252 = 11111100
    p11 = pixel_array[0] | 3 #3 = 00000011
    pixel_array[0] = inputLastTwo1 & p11 #step1 finished

    inputTwo = ((((length % (256 * 256 * 256)) % (256 * 256)) % 256) / 1) & 12 #12 = 00001100
    inputLastTwo0 = inputTwo >> 2
    inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
    p11 = pixel_array[1] | 3 #3 = 00000011
    pixel_array[1] = inputLastTwo1 & p11 #step2 finished

    inputTwo = ((((length % (256 * 256 * 256)) % (256 * 256)) % 256) / 1) & 48 #12 = 00110000
    inputLastTwo0 = inputTwo >> 4
    inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
    p11 = pixel_array[2] | 3 #3 = 00000011
    pixel_array[2] = inputLastTwo1 & p11 #step3 finished

    inputTwo = ((((length % (256 * 256 * 256)) % (256 * 256)) % 256) / 1) & 192 #12 = 11000000
    inputLastTwo0 = inputTwo >> 6
    inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
    p11 = pixel_array[3] | 3 #3 = 00000011
    pixel_array[3] = inputLastTwo1 & p11 #all done


    inputLastTwo1 = (((length % (256 * 256 * 256)) % (256 * 256)) / 256) | 252 #252 = 11111100
    p11 = pixel_array[4] | 3 #3 = 00000011
    pixel_array[4] = inputLastTwo1 & p11 #step1 finished

    inputTwo = (((length % (256 * 256 * 256)) % (256 * 256)) / 256) & 12 #12 = 00001100
    inputLastTwo0 = inputTwo >> 2
    inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
    p11 = pixel_array[5] | 3 #3 = 00000011
    pixel_array[5] = inputLastTwo1 & p11 #step2 finished

    inputTwo = (((length % (256 * 256 * 256)) % (256 * 256)) / 256) & 48 #12 = 00110000
    inputLastTwo0 = inputTwo >> 4
    inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
    p11 = pixel_array[6] | 3 #3 = 00000011
    pixel_array[6] = inputLastTwo1 & p11 #step3 finished

    inputTwo = (((length % (256 * 256 * 256)) % (256 * 256)) / 256) & 192 #192 = 11000000
    inputLastTwo0 = inputTwo >> 6
    inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
    p11 = pixel_array[7] | 3 #3 = 00000011
    pixel_array[7] = inputLastTwo1 & p11 #all done


    inputLastTwo1 = ((length % (256 * 256 * 256)) / (256 * 256)) | 252 #252 = 11111100
    p11 = pixel_array[8] | 3 #3 = 00000011
    pixel_array[8] = inputLastTwo1 & p11 #step1 finished

    inputTwo = ((length % (256 * 256 * 256)) / (256 * 256)) & 12 #12 = 00001100
    inputLastTwo0 = inputTwo >> 2
    inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
    p11 = pixel_array[9] | 3 #3 = 00000011
    pixel_array[9] = inputLastTwo1 & p11 #step2 finished

    inputTwo = ((length % (256 * 256 * 256)) / (256 * 256)) & 48 #12 = 00110000
    inputLastTwo0 = inputTwo >> 4
    inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
    p11 = pixel_array[10] | 3 #3 = 00000011
    pixel_array[10] = inputLastTwo1 & p11 #step3 finished

    inputTwo = ((length % (256 * 256 * 256)) / (256 * 256)) & 192 #192 = 11000000
    inputLastTwo0 = inputTwo >> 6
    inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
    p11 = pixel_array[11] | 3 #3 = 00000011
    pixel_array[11] = inputLastTwo1 & p11 #all done


    inputLastTwo1 = (length / (256 * 256 * 256)) | 252 #252 = 11111100
    p11 = pixel_array[12] | 3 #3 = 00000011
    pixel_array[12] = inputLastTwo1 & p11 #step1 finished

    inputTwo = (length / (256 * 256 * 256)) & 12 #12 = 00001100
    inputLastTwo0 = inputTwo >> 2
    inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
    p11 = pixel_array[13] | 3 #3 = 00000011
    pixel_array[13] = inputLastTwo1 & p11 #step2 finished

    inputTwo = (length / (256 * 256 * 256)) & 48 #12 = 00110000
    inputLastTwo0 = inputTwo >> 4
    inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
    p11 = pixel_array[14] | 3 #3 = 00000011
    pixel_array[14] = inputLastTwo1 & p11 #step3 finished

    inputTwo = (length / (256 * 256 * 256)) & 192 #192 = 11000000
    inputLastTwo0 = inputTwo >> 6
    inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
    p11 = pixel_array[15] | 3 #3 = 00000011
    pixel_array[15] = inputLastTwo1 & p11 #all done

    for i in range(0, length):
        inputLastTwo1 = hide_data[i] | 252 #252 = 11111100
        p11 = pixel_array[loop] | 3 #3 = 00000011
        pixel_array[loop] = inputLastTwo1 & p11 #step1 finished

        inputTwo = hide_data[i] & 12 #12 = 00001100
        inputLastTwo0 = inputTwo >> 2
        inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
        p11 = pixel_array[loop + 1] | 3 #3 = 00000011
        pixel_array[loop + 1] = inputLastTwo1 & p11 #step2 finished

        inputTwo = hide_data[i] & 48 #48 = 00110000
        inputLastTwo0 = inputTwo >> 4
        inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
        p11 = pixel_array[loop + 2] | 3 #3 = 00000011
        pixel_array[loop + 2] = inputLastTwo1 & p11 #step3 finished

        inputTwo = hide_data[i] & 192 #192 = 11000000
        inputLastTwo0 = inputTwo >> 6
        inputLastTwo1 = inputLastTwo0 | 252 #252 = 11111100
        p11 = pixel_array[loop + 3] | 3 #3 = 00000011
        pixel_array[loop + 3] = inputLastTwo1 & p11 #all done

        loop += 4

    return pixel_array

# Restore the hidden text from the pixel array.
def ShowText(pixel_array):
    length = _4byte2int(pixel_array[0:16])
    loop = 16
    result = 0
    lastTwo = 0
    two0 = 0
    two1 = 0
    info = []

    for i in range(0, int(length)):
        result = pixel_array[loop] | 252 #252 = 11111100

        lastTwo = pixel_array[loop + 1] & 3 #3 = 00000011
        two0 = lastTwo << 2
        two1 = two0 | 243 #243 = 11110011
        result = result & two1 #step2 finished

        lastTwo = pixel_array[loop + 2] & 3 #3 = 00000011
        two0 = lastTwo << 4
        two1 = two0 | 207 #207 = 11001111
        result = result & two1 #step3 finished

        lastTwo = pixel_array[loop + 3] & 3 #3 = 00000011
        two0 = lastTwo << 6
        two1 = two0 | 63 #63 = 00111111
        result = result & two1 #all done

        info.append(result)
        loop += 4
    
    return info

def HideProcedure(img_file_name, hide_file_name, dest_img_file_name):
    print "Hide %s into %s -> %s" %(hide_file_name, img_file_name, dest_img_file_name)
    file_header, bmpinfo_header, pixel_array = GetPartsOfBmp(img_file_name)
    hide_data = ReadAllFromFile(hide_file_name)
    new_pixel_array = HideText(hide_data, pixel_array)
    ProduceImg(dest_img_file_name, file_header, bmpinfo_header, new_pixel_array)

def ShowProcedure(img_file_name, new_file_name):
    print "Show hidden text from %s, then write it to %s" %(img_file_name, new_file_name)
    _, _, pixel_array = GetPartsOfBmp(img_file_name)
    info = ShowText(pixel_array)
    WriteAllToFile(info, new_file_name)

choice = raw_input("Hide/Show?:")
if choice == "Hide":
    img_file_name = raw_input("Source image file name:")
    hide_file_name = raw_input("Text file name:")
    dest_img_file_name = raw_input("New image file name:")
    HideProcedure(img_file_name, hide_file_name, dest_img_file_name)
elif choice == "Show":
    img_file_name = raw_input("Source image file name:")
    new_file_name = raw_input("New text file name:")
    ShowProcedure(img_file_name, new_file_name)
else:
    print "Error!"