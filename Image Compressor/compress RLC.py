import cv2
def outputFile(name):
    text_file = open(name, "w")
    text_file.write(str)
    text_file.close()

def addToStr(count,value):
    global str
    str += get_bin(count, 8)
    str += get_bin(prev, 8)
    str += "\n"

if __name__ == "__main__":
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
    addToStr(0, 161)
    print(c)
    print(rows)
    print(str)
    outputFile("Output.txt")


