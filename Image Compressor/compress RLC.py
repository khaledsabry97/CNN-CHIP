import cv2

from bitstring import Bits

global arr
global it

arr = ["ZZZZZZZZZZZZZZZZ"] *1024


#to check if the image compressed successfully
def check(compressed):
    global gray_img
    global str
    temp =current = ""
    for i in range(28):
        for j in range(28):
                current += get_bin(gray_img[i, j], 8)


    arr1 = compressed.splitlines()

    for i in range(len(arr1)):

        value = Bits(bin= arr1[i][0:8]).uint
        count = arr1[i][8:16]
        for j in range(count):
            temp += value


    if temp != current:
        print("didn't compress right")
        return


    print("successfully compressed")

def outputFile(name):
    str = ""
    str = "// memory data file (do not edit the following line - required for mem load use)" +"\n"
    str +="// instance=/iochip/i/ramcpu_1"+"\n"
    str +="// format=mti addressradix=h dataradix=b version=1.0 wordsperline=1 noaddress"+"\n"

    for ka in range(len(arr)):
        str += arr[ka]
        str += "\n"
    text_file = open(name, "w")
    text_file.write(str)
    text_file.close()
''' 
def outputFile(name):
    text_file = open(name, "w")
    text_file.write(str)
    text_file.close()
'''


def addToStr(count,value):
    global it
    global arr
    strs = ""
    strs+= get_bin(count, 8)
    strs += get_bin(value, 8)
    arr[it] = strs
    it -=1

'''
def addToStr(count,value):
    global str
    str += get_bin(count, 8)
    str += get_bin(value, 8)
    str += "\n"
'''
if __name__ == "__main__":
    it = 1023
    str = ""
    # read image
    img = cv2.imread('Input_Sample.bmp')
    # change it to BGR
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # iniatialize prev with -1
    prev = -1
    count = 0
    get_bin = lambda x, n: format(x, 'b').zfill(n)
    rows = 0
    c = 0
    for i in range(28):
        for j in range(28):
            current = gray_img[i, j]
            # if the count is more than the limit of 8 bit then print the previous value and the count and reset count to zero
            if count == 255:
                print(count, prev)
                addToStr(count,prev)
                count = 0
                rows += 1
            if current == prev or prev == -1:
                count += 1
            else:
                if count != 0:
                    print(count, prev)
                    addToStr(count, prev)
                    rows += 1
                c += count
                count = 1
            prev = current
    c += count
    # print the last values
    print(count, prev)
    addToStr(count, prev)
    # to indicate that last of the file
    addToStr(1, 0)
    addToStr(0, 0)

    print(c)
    print(rows)
    print(str)
    #check(str)
    outputFile("Output.txt")


