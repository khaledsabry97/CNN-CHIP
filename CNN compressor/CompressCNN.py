import json
from bitstring import Bits
#just variables to make it easy when you rename it


_layers = "layers"
_in_depth = "in_depth"
_out_depth = "out_depth"
_out_sx = "out_sx"
_out_sy = "out_sy"
_in_sx = "in_sx"
_sx = "sx"
_sy = "sy"
_stride = "stride"
_pad = "pad"
_num_inputs = "num_inputs"
_l1_decay_mul = "l1_decay_mul"
_l2_decay_mul = "l2_decay_mul"
_filters = "filters"
_biases = "biases"
_w = "w"
_depth = "depth"
_inputLayer = "Input Layer "
_reluLayer = "Relu Layer "
_poolLayer = "Pool Layer "
_softmaxLayer = "Soft Max Layer "
_convLayer = "Conv Layer "
_fcLayer = "Fc Layer "
#function to convert integer number to binary
get_bin = lambda x, n: format(x, 'b').zfill(n)
countBits = 2
sizeOfCompression = 14 #should be able to divide by 2
floatDigits = 9
intDigits = 4
global moCompress
global arrs
global it
it = 16383
arrs = ["ZZZZZZZZZZZZZZZZ"] *16384



def newAddress():
    global biString
    global idString
    global count
    global tempString

    if tempString != "":
        biString +=tempString
        biString += "\n"

    tempString =""
    if count != 0:
        idString += "\n"
    idString += str(count)
    idString += " : "
    count+=1

def allCnn(cnn):
    c = cnn["layers"]
    newAddress()
    output("num Of Layers", len(c))
    newAddress()
    convJson = c[1]
    poolJson = c[3]
    fcJson = c[4]
    sx = convJson[_sx]
    inDepth = convJson[_in_depth]
    outDepth = convJson[_out_depth]
    outSx = convJson[_out_sx]
    l1DecayMul = convJson[_l1_decay_mul]
    l2DecayMul = convJson[_l2_decay_mul]
    pad = convJson[_pad]
    output(_convLayer + _sx, sx)
    output(_convLayer + _in_depth, inDepth)
    output(_convLayer + _out_depth, outDepth)
    output(_convLayer + _out_sx, outSx)
    output(_convLayer + _l1_decay_mul, l1DecayMul)
    output(_convLayer + _l2_decay_mul, l2DecayMul)
    output(_convLayer + _pad, pad)
    output(_convLayer + "Filter count", len(convJson[_filters]))
    output(_convLayer + "id", 1)
    newAddress()
    biases = convJson[_biases]
    biasesDepth = biases[_depth]
    output(_convLayer + _biases + _depth, biasesDepth)
    biasesW = biases[_w]
    for i in range(8):
        if biasesW[str(i)] > 1 or biasesW[str(i)] < -1:
            print(biasesW[str(i)])
        value = biasesW[str(i)]
        output(_convLayer + _biases + " " + _w + "'" + str(i) + "' ", value)

    newAddress()
    coun = 0
    for c in convJson[_filters]:
        w = c[_w]
        for i in range(25):
            if  w[str(i)] > 1 or w[str(i)] < -1:
                print(w[str(i)])

            value = w[str(i)]
            output(_convLayer + _filters + " '" + str(coun) + "' " + _w + "'" + str(i) + "' ", value)
        coun += 1
    newAddress()
    sx = poolJson[_sx]
    inDepth = poolJson[_in_depth]
    outDepth = poolJson[_out_depth]
    outSx = poolJson[_out_sx]
    pad = poolJson[_pad]

    output(_poolLayer + _sx, sx)
    output(_poolLayer + _in_depth, inDepth)
    output(_poolLayer + _out_depth, outDepth)
    output(_poolLayer + _out_sx, outSx)
    output(_poolLayer + _in_sx, convJson[_out_sx])
    output(_poolLayer + _pad, pad)
    output(_poolLayer + "id", 2)

    newAddress()



    num_inputs = fcJson[_num_inputs]

    output(_fcLayer + _num_inputs, num_inputs)
    newAddress()
    biases = fcJson[_biases]
    biasesW = biases[_w]
    for i in range(10):
        if biasesW[str(i)] > 1 or biasesW[str(i)] < -1:
            print(biasesW[str(i)])
        value = biasesW[str(i)]
        output(_fcLayer + _biases + " " + _w + "'" + str(i) + "' ", value)

    newAddress()

    for i in range(num_inputs):
        coun = 1
        for c in fcJson[_filters]:
            w = c[_w]
            if  w[str(i)] > 1 or w[str(i)] < -1:
                print(w[str(i)])
            value = w[str(i)]
            output(_fcLayer + _filters + " '" + str(coun) + "' " + _w + "'" + str(i) + "' ", value)
            coun +=1
    newAddress()


def addToArrs(count,value):
    global it
    global arrs
    strs = ""
    strs+= get_bin(count, 8)
    strs += get_bin(value, 8)
    arr[it] = strs
    it -=1

def output16bits(t):
    global it
    global arrs
    cur = 0
    while cur < len(t):
        arrs[it] =t[cur:cur+16]
        cur = cur + 16
        it -=1

def outpusdfsdf16bits(t):
    global  moCompress
    cur = 0
    while cur < len(t):
        moCompress +=t[cur:cur+16]
        moCompress +="\n"
        cur = cur +16

def outputDecending():
    global moCompress
    global arrs
    moCompress = "// memory data file (do not edit the following line - required for mem load use)" +"\n"
    moCompress +="// instance=/iochip/i/ramcpu_1"+"\n"
    moCompress +="// format=mti addressradix=h dataradix=b version=1.0 wordsperline=1 noaddress"+"\n"
    for ka in range(len(arrs)):
        moCompress += arrs[ka]
        moCompress += "\n"

def compress(s):
    global wholeLength
    global compressedLength
    if len(s) <=1:
        return ""

    numsTimes = pow(2,countBits) -1
    count  =numsTimes -1
    temp = ""
    current = s[0:sizeOfCompression]
    for i in range(sizeOfCompression,len(s)-1,sizeOfCompression):
        if s[i:i + sizeOfCompression] != current or count == 0:
            temp += str(get_bin(numsTimes - count, countBits))
            temp += current
            count = numsTimes
       # if s[i:i+sizeOfCompression] == current:
          #  count -= 1
        current = s[i:i+sizeOfCompression]
        count -=1

    temp += str(get_bin(numsTimes - count, countBits))
    temp += current

    output16bits(temp)
    wholeLength += len(s)
    compressedLength += len(temp)
    return temp

def check(compressed,str2):
    global countBits
    global sizeOfCompression
    arr1 = compressed.split("\n")
    arr2 = str2.split("\n")
    for k in range(len(arr1)):
        i = arr1[k]
        temp = ""
        for j in range(0,len(i),countBits+sizeOfCompression):
            a = Bits(bin=i[j:j+countBits])
            count =a.uint
            for _ in range(count):
                temp += i[j+countBits:j+countBits+sizeOfCompression]

        if temp != arr2[k]:
            print("didn't compress right")
            return

    print("successfully compressed")
#print two files after you make all the processing in the program and store them in the bistring and idstring
def printTofile(bi):
    global biString
    global idString
    global count
    global moCompress
    text_file = open("biString.txt", "w")
    text_file.write(bi)
    text_file.close()
    text_file = open("mobiString.txt", "w")
    text_file.write(moCompress)
    text_file.close()
    text_file = open("biOriginalString.txt", "w")
    text_file.write(biString)
    text_file.close()
    text_file = open("idString.txt", "w")
    text_file.write(idString)
    text_file.close()


#usage of this function to add to the bistring the new value binary and idstring what this value refer to
def outputS(name,valueInteger):
    global biString
    global idString
    global tempString
    global count
    s = get_bin(valueInteger, sizeOfCompression)
    sr = list(s)
    if sr[0] == '-':
        sr[0] = '1'
        s = "".join(sr)
    biString += s
    biString += "\n"

    idString += str(count)
    idString += " : "
    idString += name
    idString += "\n"

    count += 1
def twosComplement(vaueInteger):
    a = Bits(int=vaueInteger,length=sizeOfCompression)
    return  a.bin



def output(name,valueInteger):
    global biString
    global idString
    global count
    global tempString

    tempString += transformToBits(valueInteger)
    idString += name
    idString += ","









def twos(val,minus):
    if( minus == False):
        return val
    newVal = ""
    for i in range(len(val)):
        if val[i] == "0":
            newVal +="1"
        else:
            newVal +="0"

    intVal = int(newVal, 2) + 1
    if(intVal > 16383):
        numberTwos = Bits(uint=0, length=14)
    else:
        numberTwos = Bits(uint=intVal, length=14)
    n = str(numberTwos.bin)
    return n



def transformToBits(val):
        originalVal = val
        setSignBit =0

        if(val < 0):
            setSignBit = get_bin(0,1) # I put that 0
            val = val * -1
        else:
            setSignBit = get_bin(0,1) # I put that 0


        if(isinstance(val, int)):
            setIntBits = get_bin(val,13)
            setFloatBits = ""

        elif (isinstance(val, float) and val < 1 and val >-1):
            setIntBits = get_bin(0, 3)
            setFloatBits = ""
            currentVal = 0
            for i in range(1,11):
                if currentVal + pow(2,-1 * i)<=val:
                    currentVal += pow(2,-1*i)
                    setFloatBits += "1"
                else:
                    setFloatBits +="0"
        else:
            print("integer and float")


        number = str(setSignBit)+str(setIntBits)+str(setFloatBits)
        if(originalVal < 0):
            twoss = twos(number,True)
        else:
            twoss = twos(number, False)

        with open("ValueVsBits", "a") as binary_file:
            binary_file.write(str(twoss)+"     :     "+str(number)+"     :     "+str(originalVal)+"\n")

        return twoss



if __name__ == "__main__":
    with open("ValueVsBits", "w") as binary_file:
        binary_file.write("")
    #transformToBits(1)
    #two strings to write in them the binary code and identification for that code
    biString = ""
    moCompress = ""
    biString2 = ""
    biStringCompressed = ""
    idString = ""
    idString2 = ""
    tempString =""
    wholeLength = 0
    compressedLength = 0
    #count to print the count of the row in the id file
    count = 0
    #read json file
    with open("CNN_info_Sample.json","r") as f:
        cnn = json.load(f)
    allCnn(cnn)

    #print to the file
    arr = biString.split("\n")
    for i in range( len(arr)):
        biStringCompressed += compress(arr[i])
        if i != len(arr) -1:
            biStringCompressed +="\n"
            output16bits("0000000000000001")
    output16bits("0000000000000000")

    check(biStringCompressed,biString)
    print((compressedLength/wholeLength)*100)

    arr = biStringCompressed.split("\n")
    biStringCompressed = ""
    for i in range(len(arr)):
        if(arr[i] == ""):
            continue
        print(len(arr[i])%16)
        biStringCompressed += arr[i]
        biStringCompressed +="\n"
        biStringCompressed +="0000000000000001"
        biStringCompressed += "\n"
    biStringCompressed += "0000000000000000"
    biStringCompressed += "\n"

    outputDecending()
    printTofile(biStringCompressed)

