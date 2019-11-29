from __future__ import print_function
import os
#****************IMPORTANT FOR RUNNING THE FILE ***********************************
#******GRADERS PLEASE RENAME THIS FILE TO "P1_1.py"

def getInput(netName):

    netFile=open(netName, 'r')
    input=0
    for line in netFile:
        if line[0:5]=='INPUT':
            input=input+1
    return input

def FaultList(netName):

    #Open circuit file & read it

    netFile = open(netName,'r')

    #Create variables to store data and so to save circuit elements and faults
    #empty lits 

    inputs = []
    outputs = []
    gates = []
    faultList = []
    faults = 0
    #Create a dictionary for the circuit to check the correctness of the circuit.bench file

    circuit = {}
    #It will return a list of lines in file. 
    #We can iterate over that list and strip() the new line character then print the line i.e
    
    #Circuit read
    for line in netFile:

        if (line == '\n'):
            continue

        if(line[0] == '#'):
            continue

        line = line.replace(" ","")
        line = line.replace("\n","")

        if (line[0:5] == "INPUT"):
            
            line = line.replace("INPUT", "")
            line = line.replace("(", "")
            line = line.replace(")", "")

            # Format the variable name to wire_*VAR_NAME*
            line = "wire_" + line

            # Error detection: line being made already exists
            if line in circuit:
                msg = "NETLIST ERROR: INPUT LINE \"" + line + "\" ALREADY EXISTS PREVIOUSLY IN NETLIST"
                print(msg + "\n")
                return msg

            # Appending to the inputs array and update the inputBits
            inputs.append(line)
            # add this wire as an entry to the circuit dictionary
            circuit[line] = ["INPUT", line, False, 'U']

            line = line.replace("wire_","")

            newLine = line + "-SA-0"
            faultList.append(newLine)
            line4 = line + "-SA-1"
            faultList.append(line4)
            faults += 2
            continue


        print(inputs)
        if line[0:6] == "OUTPUT":
            
            # Removing everything but the numbers
            line = line.replace("OUTPUT", "")
            line = line.replace("(", "")
            line = line.replace(")", "")

            # Appending to the output array[
            outputs.append("wire_" + line)
            continue

        lineSpliced = line.split("=")  # splicing the line at the equals sign to get the gate output wire

        gateOut = "wire_" + lineSpliced[0]
        if gateOut in circuit:
            msg = "NETLIST ERROR: GATE OUTPUT LINE \"" + gateOut + "\" ALREADY EXISTS PREVIOUSLY IN NETLIST"
            print(msg + "\n")
            return msg

            # Appending the dest name to the gate list
        gates.append(gateOut)

        line = lineSpliced[0]

        line2 = line + "-SA-0"
        faultList.append(line2)
        line2 = line + "-SA-1"
        faultList.append(line2)
        faults += 2
        index = lineSpliced[0]

        lineSpliced = lineSpliced[1].split("(")

        logic = lineSpliced[0].upper
        lineSpliced[1] = lineSpliced[1].replace(")", "")

        terms = lineSpliced[1].split(",")

        i = 0

        while(i<len(terms)):   # Used while loop here that run until terms length where term has the variable that come after "-IN-" .
            line3 = index + "-IN-" + str(terms[i]) + "-SA-0"
            faultList.append(line3)
            line3 = index + "-IN-" + str(terms[i]) + "-SA-1"
            faultList.append(line3)
            faults += 2
            i = i + 1
            continue

        terms = ["wire_" + x for x in terms]

        # add the gate output wire to the circuit dictionary with the dest as the key
        circuit[gateOut] = [logic, terms, False, 'U']
    line = '\n# total faults: %d' % faults
    faultList.append(line)
    return faultList

def TVgenA(seed, fileTV_A, numInputs):
    for i in range(0, 255):
        temp = bin(int(seed) + i)
        temp = temp[2:]
        a=len(temp)-numInputs
        if len(temp)>numInputs:
            temp = temp[a:]
        fileTV_A.write(format(int(temp), "0" + str(numInputs)) + "\n")

def TVgenB(seed, fileTV_B, numInputs):
    i = 0
    for counter in range(0, 255):
        if int(seed)+i > 255:
            seed = -i

        temp = bin(int(seed) + i)

        temp = temp[2:]
        temp = format(int(temp), "08")
        num = temp
        while len(temp) < int(numInputs):
            temp = num + temp

        fileTV_B.write(temp[len(temp) - numInputs: len(temp)] + "\n")
        i += 1


def TVgenC(seed, fileTV_C, numInputs):
    i = 0
    for counter in range(0, 255):
        if int(seed)+i > 255:
            seed = -i
        tv = ""
        hold = i
        while len(tv) < int(numInputs):
            temp = bin(int(seed) + i)
            temp = temp[2:]
            temp = format(int(temp), "08")
            tv = temp + tv
            i += 1
        i = hold
        fileTV_C.write(tv[len(tv) - numInputs: len(tv)] + "\n")
        i += 1


def LSFR(inp):
    inp = list(reversed(inp))
    inp2 = ['0', '0', '0', '0', '0', '0', '0', '0']

    inp2[0] = inp[7]
    inp2[1] = inp[0]
    inp2[2] = int(inp[1]) ^ int(inp[len(inp)-1])
    inp2[3] = int(inp[2]) ^ int(inp[len(inp)-1])
    inp2[4] = int(inp[3]) ^ int(inp[len(inp)-1])
    inp2[5] = int(inp[4]) ^ int(inp[len(inp)-1]) #added taps at 5 and 6 as well for checking
    inp2[6] = int(inp[5]) ^ int(inp[len(inp)-1])
    inp2[7] = inp[6]

    inp2 = list(reversed(inp2))

    return int("".join(map(str, inp2)))


def TVgenD(seed, fileTV_D, numInputs):
    temp = bin(int(seed))
    temp = temp[2:]
    i=0
    for counter in range(0, 255):
        if int(seed)+i > 255:
            seed = -i
        if i > 0:
            temp = LSFR(str(temp))

        temp = str(format(int(temp), "08"))
        num = temp
        while len(temp) < int(numInputs):
            temp = num + temp

        fileTV_D.write(temp[len(temp) - numInputs: len(temp)] + "\n")
        i += 1


def TVgenE(seed, fileTV_E, numInputs):
    nextStart = 0
    i = 0

    for counter in range(0, 255):
        if int(seed) + i > 255:
            seed = -i
        tv = ""
        hold = i
        if i == 0:
            temp = bin(int(seed))
            temp = temp[2:].zfill(8)
            nextInp = temp
        if i > 0:
            nextInp = nextStart
            i = 0
        while len(tv) < int(numInputs):
            if i > 0:
                temp = LSFR(str(nextInp))
                temp = format(int(temp), "08")

            else:
                i += 1
                temp = format(int(nextInp), "08")

            nextInp = temp

            if len(tv) == 0:
                nextStart = format(LSFR(str(temp)), "08")
            tv = temp + tv
            print(len(tv))

        fileTV_E.write(tv[len(tv) - numInputs: len(tv)] + "\n")
        i = hold
        i += 1



def part1():

    print("Full fault list generator\n")

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

    while True:
        cktFile = "c432.bench"
        print("\n Read circuit benchmark file: use " + cktFile + "?" + " Enter to accept or type filename: ")
        userInput = input()
        if userInput == "":
            break
        else:
            cktFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(cktFile):
                print("File does not exist. \n")
            else:
                break
    while True:
        seed = ""
        print("\n Enter Seed s0 Value: ")
        userInput = input()
        if userInput != "":
            seed = userInput;
            break


    print("Detection possible faults...\n")

    faultList = FaultList(cktFile)

    print(faultList)

    while True:
        outputName = "f_list.txt"
        print("\n Write output file: use " + outputName + "?" + " Enter to accept or type filename: ")
        userInput = input()
        if userInput == "":
            break
        else:
            outputName = os.path.join(script_dir, userInput)
            break

    outputFile = open(outputName, 'w')
    outputFile.write("# circuit.bench \n# full SSA list\n\n")

    for line in faultList:
        outputFile.write("%s\n" % line)

    file_TV_A = open("TV_A.txt", "w")
    file_TV_B = open("TV_B.txt", "w")
    file_TV_C = open("TV_C.txt", "w")
    file_TV_D = open("TV_D.txt", "w")
    file_TV_E = open("TV_E.txt", "w")

    numInputs = getInput(cktFile)


    TVgenA(seed, file_TV_A, numInputs)
    TVgenB(seed, file_TV_B, numInputs)
    TVgenC(seed, file_TV_C, numInputs)
    TVgenD(seed, file_TV_D, numInputs)
    TVgenE(seed, file_TV_E, numInputs)

    outputFile.close()



