from __future__ import print_function
import os
import copy



def getBits(circuit_File):
    netFile = open(circuit_File, 'r')
    inputBit = 0
    for line in netFile:
        if line[0:5] == "INPUT":
            inputBit = inputBit + 1
    return inputBit

def Fault_Input(circuit, fault):
    x=3
    y=5
    fault=fault.split("-")
    if(len(fault)==x):
        circuit["wire_"+ fault[0]][2]= True
        circuit["wire_"+ fault[0]][3]= fault[2]
    elif(len(fault)==5):
        lst=[]
        lst=["wire_" + fault[0], "wire_" + fault[2], fault[4]]
    return circuit


def printCkt(circuit):
    print("INPUT LIST:")
    for x in circuit["INPUTS"][1]:
        print(x + "= ", end='')

        print(circuit[x])

    print("\nOUTPUT LIST:")


    for x in circuit["OUTPUTS"][1]:
        print(x + "= ", end='')

        print(circuit[x])


    print("\nGATE list:")

    for x in circuit["GATES"][1]:
        print(x + "= ", end='')
        print(circuit[x])
    print()


flipflopDict = {}


def FaultList(netName):
    # Open circuit file

    netFile = open(netName, 'r')

    # Create variables to store data and so to save circuit elements and faults

    inputs = []
    outputs = []
    gates = []
    Faultsl = []
    counter = 0
    # Create a dictionary for the circuit to check the correctness of the circuit.bench file

    circuit = {}

    # print("Input reading")

    # Circuit read
    for line in netFile:

        if (line == '\n'):
            continue

        if (line[0] == '#'):
            continue

        line = line.replace(" ", "")
        line = line.replace("\n", "")

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

            line = line.replace("wire_", "")

            Response_Fault = line + "-SA-0"
            counter += 1
            Faultsl.append(Response_Fault)
            Response_Fault = line + "-SA-1"
            Faultsl.append(Response_Fault)
            counter += 1
            continue

        if line[0:6] == "OUTPUT":
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

        Response_Fault = line + "-SA-0"
        Faultsl.append(Response_Fault)
        counter += 1
        Response_Fault = line + "-SA-1"
        Faultsl.append(Response_Fault)
        counter += 1
        ref_wire = lineSpliced[0]

        lineSpliced = lineSpliced[1].split("(")

        logic = lineSpliced[0].upper
        lineSpliced[1] = lineSpliced[1].replace(")", "")

        terms = lineSpliced[1].split(",")

        for x in terms:
            Response_Fault = ref_wire + "-IN-" + x + "-SA-0"
            Faultsl.append(Response_Fault)
            counter += 1
            Response_Fault = ref_wire + "-IN-" + x + "-SA-1"
            Faultsl.append(Response_Fault)
            counter += 1
            continue

        terms = ["wire_" + x for x in terms]

        circuit[gateOut] = [logic, terms, False, 'U']
    line = '\n# total faults: %d' % counter
    Faultsl.append(line)
    # circuit["INPUT_WIDTH"] = ["input width:", counter]
    # circuit["INPUTS"] = ["Input list", inputs]
    # circuit["OUTPUTS"] = ["Output list", outputs]
    # circuit["GATES"] = ["Gate list", gates]
    # circuit["FAULTS"] = ["Full Faults", Faults1]
    return Faultsl


def reset_mode(circuit):
    for i in circuit:
        if (i[0:5] == "wire_"):
            if (circuit[i][0] != "DFF"):
                circuit[i][2] = False
                circuit[i][3] = 'U'
    return circuit


def NetReader(netName):
    # Open circuit file

    netFile = open(netName, 'r')

    # Create variables to store data and so to save circuit elements and faults

    inputs = []
    outputs = []
    gates = []
    inputBits = 0
    # Create a dictionary for the circuit to check the correctness of the circuit.bench file

    circuit = {}

    # Circuit read
    for line in netFile:

        if (line == '\n'):
            continue

        if (line[0] == '#'):
            continue

        line = line.replace(" ", "")
        line = line.replace("\n", "")

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
            inputBits += 1
            # add this wire as an entry to the circuit dictionary
            circuit[line] = ["INPUT", line, False, 'U']
            print(circuit[line])

            continue

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

        lineSpliced = lineSpliced[1].split("(")  # splicing the line again at the "("  to get the gate logic
        logic = lineSpliced[0].upper()

        lineSpliced[1] = lineSpliced[1].replace(")", "")
        terms = lineSpliced[1].split(",")  # Splicing the the line again at each comma to the get the gate terminals
        # Turning each vals into an integer before putting it into the circuit dictionary
        terms = ["wire_" + x for x in terms]

        # add the gate output wire to the circuit dictionary with the dest as the i
        if (logic == "DFF"):
            circuit[gateOut] = [logic, terms, True, '0']
            flipflopDict[gateOut] = terms
        else:
            circuit[gateOut] = [logic, terms, False, 'U']
        print(gateOut)

        print(circuit[gateOut])



        circuit["INPUT_WIDTH"] = ["input width:", inputBits]
        circuit["INPUTS"] = ["Input list", inputs]
        circuit["OUTPUTS"] = ["Output list", outputs]
        circuit["GATES"] = ["Gate list", gates]
    return circuit


def gateCalc(circuit, node):
    # terminal will contain all the input wires of this logic gate (node)
    terminals = list(circuit[node][1])

    # If the node is an Inverter gate output, solve and return the output
    if circuit[node][0] == "NOT":
        if circuit[terminals[0]][3] == '0':
            circuit[node][3] = '1'
        elif circuit[terminals[0]][3] == '1':
            circuit[node][3] = '0'
        elif circuit[terminals[0]][3] == "U":
            circuit[node][3] = "U"
        else:  # Should not be able to come here
            return -1
        return circuit
    # Added the DFF GATE LOGIC. Basically it takes whatever is stored in it as the output
    if circuit[node][0] == "DFF":
        circuit[node][3] = circuit[terminals[0]][3]
        circuit = copy.deepcopy(circuit)
        return circuit

    # If the node is an AND gate output, solve and return the output
    elif circuit[node][0] == "AND":
        # Initialize the output to 1
        circuit[node][3] = '1'
        # Initialize also a flag that detects a U to false
        unknownTerm = False  # This will become True if at least one unknown terminal is found

        # if there is a 0 at any input terminal, AND output is 0. If there is an unknown terminal, mark the flag
        # Otherwise, keep it at 1
        for vals in terminals:
            if circuit[vals][3] == '0':
                circuit[node][3] = '0'
                break
            if circuit[vals][3] == "U":
                unknownTerm = True

        if unknownTerm:
            if circuit[node][3] == '1':
                circuit[node][3] = "U"
        return circuit

    # If the node is a NAND gate output, solve and return the output
    elif circuit[node][0] == "NAND":
        # Initialize the output to 0
        circuit[node][3] = '0'
        # Initialize also a variable that detects a U to false
        unknownTerm = False  # This will become True if at least one unknown terminal is found

        # if there is a 0 terminal, NAND changes the output to 1. If there is an unknown terminal, it
        # changes to "U" Otherwise, keep it at 0
        for vals in terminals:
            if circuit[vals][3] == '0':
                circuit[node][3] = '1'
                break
            if circuit[vals][3] == "U":
                unknownTerm = True
                break

        if unknownTerm:
            if circuit[node][3] == '0':
                circuit[node][3] = "U"
        return circuit

    # If the node is an OR gate output, solve and return the output
    elif circuit[node][0] == "OR":
        # Initialize the output to 0
        circuit[node][3] = '0'
        # Initialize also a variable that detects a U to false
        unknownTerm = False  # This will become True if at least one unknown terminal is found

        # if there is a 1 terminal, OR changes the output to 1. Otherwise, keep it at 0
        for vals in terminals:
            if circuit[vals][3] == '1':
                circuit[node][3] = '1'
                break
            if circuit[vals][3] == "U":
                unknownTerm = True

        if unknownTerm:
            if circuit[node][3] == '0':
                circuit[node][3] = "U"
        return circuit

    # If the node is an NOR gate output, solve and return the output
    if circuit[node][0] == "NOR":
        # Initialize the output to 1
        circuit[node][3] = '1'
        # Initialize also a variable that detects a U to false
        unknownTerm = False  # This will become True if at least one unknown terminal is found

        # if there is a 1 terminal, NOR changes the output to 0. Otherwise, keep it at 1
        for vals in terminals:
            if circuit[vals][3] == '1':
                circuit[node][3] = '0'
                break
            if circuit[vals][3] == "U":
                unknownTerm = True
        if unknownTerm:
            if circuit[node][3] == '1':
                circuit[node][3] = "U"
        return circuit

    # If the node is an XOR gate output, solve and return the output
    if circuit[node][0] == "XOR":
        # Initialize a variable to zero, to count how many 1's in the terms
        count = 0

        # if there are an odd number of terminals, XOR outputs 1. Otherwise, it should output 0
        for vals in terminals:
            if circuit[vals][3] == '1':
                count += 1  # For each 1 bit, add one count
            if circuit[vals][3] == "U":
                circuit[node][3] = "U"
                return circuit

        # check how many 1's we counted
        if count % 2 == 1:  # if more than one 1, we know it's going to be 0.
            circuit[node][3] = '1'
        else:  # Otherwise, the output is equal to how many 1's there are
            circuit[node][3] = '0'
        return circuit

    # If the node is an XNOR gate output, solve and return the output
    elif circuit[node][0] == "XNOR":
        # Initialize a variable to zero, to count how many 1's in the terms
        count = 0

        # if there is a single 1 terminal, XNOR outputs 0. Otherwise, it outputs 1
        for vals in terminals:
            if circuit[vals][3] == '1':
                count += 1  # For each 1 bit, add one count
            if circuit[vals][3] == "U":
                circuit[node][3] = "U"
                return circuit

        # check how many 1's we counted
        if count % 2 == 1:  # if more than one 1, we know it's going to be 0.
            circuit[node][3] = '1'
        else:  # Otherwise, the output is equal to how many 1's there are
            circuit[node][3] = '0'
        return circuit
    elif circuit[node][0] == "BUFF":
        if circuit[terminals[0]][3] == '0':
            circuit[node][3] = '0'
        elif circuit[terminals[0]][3] == '1':
            circuit[node][3] = '1'
        elif circuit[terminals[0]][3] == "U":
            circuit[node][3] = "U"
        else:  # Should not be able to come here
            return -1
        return circuit
    # Error detection... should not be able to get at this point
    return circuit[node][0]


# Input reader
def inputRead(circuit, line):
    if len(line) < circuit["INPUT_WIDTH"][1]:
        print("Not enough bits")
        return -1

    # Getting the proper number of bits:
    line = line[(len(line) - circuit["INPUT_WIDTH"][1]):(len(line))]

    # Adding the inputs to the dictionary
    # Since the for loop will start at the most significant bit, we start at input width N
    i = circuit["INPUT_WIDTH"][1] - 1
    inputs = list(circuit["INPUTS"][1])
    # dictionary item: [(bool) If accessed, (int) the value of each line, (int) layer number, (str) origin of U value]
    for bitVal in line:
        bitVal = bitVal.upper()  # in the case user input lower-case u
        circuit[inputs[i]][3] = bitVal  # put the bit value as the line value
        circuit[inputs[i]][2] = True  # and make it so that this line is accessed

        # In case the input has an invalid character (i.e. not "0", "1" or "U"), return an error flag
        if bitVal != "0" and bitVal != "1" and bitVal != "U":
            return -2
        i -= 1  # continuing the increments

    return circuit


def FaultReader(line):
    if not "-SA-" in line:
        print("Error in the format")
        return -1

    # This condition allows to accept inputs with a name long no more than 5 characters
    if (len(line) > 10):
        line = line.replace("-SA", "")
        line = line.replace("IN-", "")
        line = line.split("-")
        flag = 'I'
        line.append(flag)
        fault = line
    else:
        line = line.replace("-SA", "")
        line = line.split("-")
        flag = 'S'
        line.append(flag)
        fault = line
    return fault
def good_sim(circuit, n):
    queue = list(circuit["GATES"][1])
    i = 1
    print("\n______________")
    print("* Cycle " + str(n) + " *")
    print("______________")

    while True:
        i -= 1
        if len(queue) == 0:
            break

        # Remove the first element of the queue and assign it to a variable for us to use
        curr = queue[0]
        queue.remove(curr)

        print(curr)
        print("\nCurrent gate information:")
        print(circuit[curr])

        # initialize a flag, used to check if every terminal has been accessed
        term_has_value = True

        # Check if the terminals have been accessed
        for vals in circuit[curr][1]:
            if not circuit[vals][2]:
                term_has_value = False
                break
                ##part2 skip this cuz this is a SA wire
        if circuit[curr][2] == True:
            print("________________________________________________________________________________________")
            continue

        if term_has_value:
            circuit[curr][2] = True
            circuit = gateCalc(circuit, curr)
            print(" Displaying Results  ")
            print()
            print(circuit[curr])


            # ERROR Detection if LOGIC does not exist
            if isinstance(circuit, str):
                print(circuit)
                return circuit

        else:
            # If the terminals have not been accessed yet, append the current node at the end of the queue
            queue.append(curr)

    return circuit

def bad_sim(circuit, fault):
    queue = list(circuit["GATES"][1])
    out_wire = ""
    while True:
        flag = False
        if len(queue) == 0:
            break

        if fault[2] == 'S':
            bad_wire = "wire_" + fault[0]
        elif fault[3] == 'I':
            bad_wire = "wire_" + fault[1]
            out_wire = "wire_" + fault[0]
        else:
            print("Error in the fault format")
            return -1

        curr = queue[0]
        queue.remove(curr)

        if (bad_wire == curr) and (fault[2] == 'S'):
            circuit[curr][3] = fault[1]
            circuit[curr][2] = True

        else:
            if (bad_wire in circuit[curr][1]) and (out_wire == curr):
                flag = True
                Corr_Input = circuit[bad_wire][3]
                circuit[bad_wire][3] = fault[2]

            term_has_value = True

            # Check if the terminals have been accessed
            for vals in circuit[curr][1]:
                # wire presence check
                if not circuit[vals][2]:
                    term_has_value = False
                    break

            if term_has_value:

                circuit[curr][2] = True

                circuit = gateCalc(circuit, curr)

                # ERROR Detection if LOGIC does not exist
                if isinstance(circuit, str):
                    print(circuit)
                    return circuit

                if flag == True:
                    circuit[bad_wire][3] = Corr_Input
                    flag = False

                # print("Progress: updating " + curr + " = " + circuit[curr][3] + " as the output of " + circuit[curr][
                #       0] + " for:")
                # for vals in circuit[curr][1]:
                #   print(vals + " = " + circuit[vals][3])

                # If the terminals have not been accessed yet, append the current node at the end of the queue
            else:
                queue.append(curr)

    return circuit

def main():

    # **************************************************************************************************************** #
    # NOTE: UI code; Does not contain anything about the actual simulation

    # menu
    # Used for file access
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

    # Select circuit benchmark file, default is circuit.bench
    while True:
        print("Sequential Circuit Simulator by Imran Babar, Arsalan Babar, Syed Khalid \n")
        print("_____________________________________________________________________________\n")
        circuit_File = "s27.bench"
        print("\n Read circuit benchmark file: use " + circuit_File + "?" + " Enter to accept or type filename: ")

        user_input = input()
        if user_input == "":
            break
        else:
            circuit_File = os.path.join(script_dir, user_input)
            if not os.path.isfile(circuit_File):
                print("File does not exist. \n")
            else:
                break
    circuit = NetReader(circuit_File)

    while (True):
        response_tv = input("\nEnter a Test Vector to test(INTEGER): ")
        ckt_file = open(circuit_File, "r")
        bits = getBits(circuit_File)
        response_tv = int(response_tv)

        if response_tv >= 0:
            response_tv = "{0:b}".format(response_tv).zfill(bits)
            response_tv = response_tv[int(len(response_tv)) - bits:]
        else:
            response_tv = bin(response_tv + (2 ** bits))[2:].zfill(bits)

        break

    ckt_file.close()

    while (True):
        cycles = int(input("\nEnter number of cycles to run(Integer): "))
        if cycles > -1:
            break
        else:
            continue

    newCircuit = circuit

    print("\n ----- We are ready to simulate---- " + response_tv)

    output = ""
    k = 0

    if circuit == -1:
        print("Bits used are not valid")
        circuit = newCircuit
        print("...move on to next input\n")
        return
    elif circuit == -2:
        print("Input value is not valid. ")
        circuit = newCircuit
        print("Moving onto the next input\n")
        return

    print("---------------")
    print('\n')
    print("Good Circuit Simulation")
    print()

    while k < cycles:

        circuit = inputRead(circuit, response_tv)
        circuit = good_sim(circuit, k + 1)
        print("Cycle #" + str(k + 1) + "\n" " Results:" + "\n")
        print(circuit)
        print('\n')
        print('\n')


        for keeys, vals in flipflopDict.items():
            circuit[keeys][3] = circuit[vals[0]][3]

        for y in circuit["OUTPUTS"][1]:
            if not circuit[y][2]:
                output = "ERROR \"" + y + "\""
                break
            output = str(circuit[y][3]) + output

        reset_mode(circuit)
        k += 1
    reset_mode(circuit)

    for keeys, vals in flipflopDict.items():
        circuit[keeys][3] = "U"

    first_input_line = circuit["INPUTS"][1][0].split("_")

    Response_Fault = input(
        "Enter fault to test: ")

    print("-------------")
    print('\n')

    print(" Faulty Circuit Simulation")

    print()


if __name__ == "__main__":
    main()