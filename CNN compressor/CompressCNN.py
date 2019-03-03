import json

#just variables to make it easy when you rename it
_layers = "layers"
_in_depth = "in_depth"
_out_depth = "out_depth"
_out_sx = "out_sx"
_out_sy = "out_sy"
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


#print two files after you make all the processing in the program and store them in the bistring and idstring
def printTofile():
    global biString
    global idString
    global count
    text_file = open("biString.txt", "w")
    text_file.write(biString)
    text_file.close()
    text_file = open("idString.txt", "w")
    text_file.write(idString)
    text_file.close()

#usage of this function to add to the bistring the new value binary and idstring what this value refer to
def output(name,valueInteger):
    global biString
    global idString
    global count
    s = get_bin(valueInteger, 16)
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
#all of the upcomming functions just for reading the json file
def  inputLayer(json):
    outDepth = json[_out_depth]
    outSx = json[_out_sx]
    outSy = json[_out_sy]
    output(_inputLayer + _out_depth, outDepth)
    output(_inputLayer + _out_sx, outSx)
    output(_inputLayer + _out_sx, outSy)

def  reluLayer(json):
    outDepth = json[_out_depth]
    outSx = json[_out_sx]
    outSy = json[_out_sy]
    output(_reluLayer + _out_depth, outDepth)
    output(_reluLayer + _out_sx, outSx)
    output(_reluLayer + _out_sx, outSy)

def  poolLayer(json):
    sx = json[_sx]
    sy = json[_sy]
    stride = json[_stride]
    inDepth = json[_in_depth]
    outDepth = json[_out_depth]
    outSx = json[_out_sx]
    outSy = json[_out_sy]
    pad = json[_pad]

    output(_poolLayer + _sx, sx)
    output(_poolLayer + _sy, sy)
    output(_poolLayer + _stride, stride)
    output(_poolLayer + _in_depth, inDepth)
    output(_poolLayer + _out_depth, outDepth)
    output(_poolLayer + _out_sx, outSx)
    output(_poolLayer + _out_sy, outSy)
    output(_poolLayer + _pad, pad)

def  softmaxLayer(json):
    outDepth = json[_out_depth]
    outSx = json[_out_sx]
    outSy = json[_out_sy]
    numInputs = json[_num_inputs]

    output(_softmaxLayer + _out_sx, outSx)
    output(_softmaxLayer + _out_sy, outSy)
    output(_softmaxLayer + _num_inputs, numInputs)
    output(_softmaxLayer + _out_depth, outDepth)


def  convLayer(json):
    sx = json[_sx]
    sy = json[_sy]
    stride = json[_stride]
    inDepth = json[_in_depth]
    outDepth = json[_out_depth]
    outSx = json[_out_sx]
    outSy = json[_out_sy]
    l1DecayMul = json[_l1_decay_mul]
    l2DecayMul = json[_l2_decay_mul]
    pad = json[_pad]
    output(_convLayer + _sx, sx)
    output(_convLayer + _sy, sy)
    output(_convLayer + _stride, stride)
    output(_convLayer + _in_depth, inDepth)
    output(_convLayer + _out_depth, outDepth)
    output(_convLayer + _out_sx, outSx)
    output(_convLayer + _out_sy, outSy)
    output(_convLayer + _l1_decay_mul, l1DecayMul)
    output(_convLayer + _l2_decay_mul, l2DecayMul)
    output(_convLayer + _pad, pad)
    #todo right in the file before you enter the loop
    coun= 0
    for c in json[_filters]:
        sx = c[_sx]
        sy = c[_sy]
        depth = c[_depth]

        output(_convLayer+ _filters + " '" + str(coun) + "' " + _sx, sx)
        output(_convLayer+ _filters + " '" + str(coun) + "' " + _sy, sy)
        output(_convLayer+ _filters + " '" + str(coun) + "' " + _depth, depth)
        w = c[_w]
        for i in  range(25):
                value = int(w[str(i)]*32768)
                output(_convLayer + _filters + " '" + str(coun) + "' " +_w+  "'" + str(i) + "' " , value)

        coun += 1
    biases= json[_biases]
    biasesSx = biases[_sx]
    biasesSy = biases[_sy]
    biasesDepth = biases[_depth]
    output(_convLayer + _biases + " '" + str(coun) + "' " + _sx, biasesSx)
    output(_convLayer + _biases + " '" + str(coun) + "' " + _sy, biasesSy)
    output(_convLayer + _biases + " '" + str(coun) + "' " + _depth, biasesDepth)
    biasesW = biases[_w]
    for i in range(8):
        value = int(biasesW[str(i)] * 32768)
        output(_convLayer + _biases + " " + _w + "'" + str(i) + "' ", value)

def  fcLayer(json):
    outDepth = json[_out_depth]
    outSx = json[_out_sx]
    outSy = json[_out_sy]
    num_inputs = json[_num_inputs]
    l1DecayMul = json[_l1_decay_mul]
    l2DecayMul = json[_l2_decay_mul]
    output(_fcLayer + _out_depth, outDepth)
    output(_fcLayer + _out_sx, outSx)
    output(_fcLayer + _out_sy, outSy)
    output(_fcLayer + _num_inputs, num_inputs)
    output(_fcLayer + _l1_decay_mul, l1DecayMul)
    output(_fcLayer + _l2_decay_mul, l2DecayMul)
    coun= 0
    for c in json[_filters]:
        sx = c[_sx]
        sy = c[_sy]
        depth = c[_depth]

        output(_fcLayer+ _filters + " '" + str(coun) + "' " + _sx, sx)
        output(_fcLayer+ _filters + " '" + str(coun) + "' " + _sy, sy)
        output(_fcLayer+ _filters + " '" + str(coun) + "' " + _depth, depth)
        w = c[_w]
        for i in  range(1152):
                value = int(w[str(i)]*32768)
                output(_fcLayer + _filters + " '" + str(coun) + "' " +_w+  "'" + str(i) + "' " , value)

        coun += 1
    biases= json[_biases]
    biasesSx = biases[_sx]
    biasesSy = biases[_sy]
    biasesDepth = biases[_depth]
    output(_fcLayer + _biases + " '" + str(coun) + "' " + _sx, biasesSx)
    output(_fcLayer + _biases + " '" + str(coun) + "' " + _sy, biasesSy)
    output(_fcLayer + _biases + " '" + str(coun) + "' " + _depth, biasesDepth)
    biasesW = biases[_w]
    for i in range(10):
        value = int(biasesW[str(i)] * 32768)
        output(_fcLayer + _biases + " " + _w + "'" + str(i) + "' ", value)

if __name__ == "__main__":
    #two strings to write in them the binary code and identification for that code
    biString = ""
    idString = ""
    #count to print the count of the row in the id file
    count = 0
    #read json file
    with open("CNN_info_Sample.json","r") as f:
        cnn = json.load(f)
    #get the layers from json file
    c =  cnn["layers"]
    #write them in file as you want
    inputLayer(c[0])
    reluLayer(c[2])
    poolLayer(c[3])
    softmaxLayer(c[5])
    convLayer(c[1])
    fcLayer(c[4])
    #print to the file
    printTofile()

