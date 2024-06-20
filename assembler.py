'''
    CSE 112 - Computer Organisation group project.
        group members :
            Aditya Sharma 2022038
            Ayan kumar singh 2022122
            Ayaan hasan 2022121
            Kanishk Kumar Meena 2022233
'''



# ------------------------------------------taking input throught a text file contating assemble code-------------------------------------------------

# uncomment these lines to take input from stdout

import sys
code=sys.stdin.read().splitlines()

# --------------------------------------------------------------------taking input from test case file -------------------------------------------------
# with open('t.txt') as file1:  
#     code = file1.read().splitlines() 
# ----------------------------------------------file to which the out generated will be written-----------------------------------------------------------

# the code will print the output binary code to the output.txt file and also show it in terminal.
file2 = open("output.txt","w")
# ---------------------------------------------------------------------------------input code ends--------------------------------------------------------------
 # ACTUAL CODE STARTS FORM HERE  

main_lst=[]
for i in code:
    a=i.split(' ')
    main_lst.append(a)

# making a dictionary with register 0,1,2,3,4,5,6 mapped to there binary code 
# there are total 7 general purpose register and one flag register
RegAddress = {
  "R0":"000",
  "R1":"001",
  "R2":"010",
  "R3":"011",
  "R4":"100",
  "R5":"101",
  "R6":"110",
  "FLAGS":"111"
}


operations = {
   "add":["00000","A"], # Performs reg1 = reg2 + reg3. If the computation overflows, then the overflow flag is set and 0 is written in reg1
   "sub":["00001","A"], # Performs reg1 = reg2- reg3. In case reg3 > reg2, 0 is written to reg1 and overflow flag is set.
   "mov1":["00010","B"], # mov immediate
   "mov2":["00011","C"], # mov with register
   "ld":["00100","D"], # Loads data from mem_addr into reg1.
   "st":["00101","D"], # Stores data from reg1 to mem_addr.
   "mul":["00110","A"], # Performs reg1 = reg2 x reg3. If the computation overflows, then the overflow flag is set and 0 is written in reg1
   "div":["00111","C"], # Performs reg3/reg4. Stores the quotient in R0 and the remainder in R1. If reg4 is 0 then overflow flag is set and content of R0 and R1 are set to 0
   "rs":["01000","B"], # Right shifts reg1 by $Imm, where $Imm is a 7 bit value.
   "ls":["01001","B"], # Left shifts reg1 by $Imm, where $Imm is a 7 bit value.
   "xor":["01010","A"], # Performs bitwise XOR of reg2 and reg3. Stores the result in reg1.
   "or":["01011","A"], # Performs bitwise OR of reg2 and reg3. Stores the result in reg1.
   "and":["01100","A"], # Performs bitwise AND of reg2 and reg3. Stores the result in reg1.
   "not":["01101","C"], # Performs bitwise NOT of reg2. Stores the result in reg1.
   "cmp":["01110","C"], # Compares reg1 and reg2 and sets up the FLAGS register.
   "jmp":["01111","E"], # Jumps to mem_addr, where mem_addr is a memory address.
   "jlt":["11100","E"], # Jump to mem_addr if the less than flag is set (less than flag = 1), where mem_addr is a memory address.
   "jgt":["11101","E"], # Jump to mem_addr if the greater than flag is set (greater than flag = 1), where mem_addr is a memory address.
   "je":["11111","E"], # Jump to mem_addr if the equal flag is set (equal flag = 1), where mem_addr is a memory address.
   "hlt":["11010","F"] # Stops the machine from executing until reset
}
opr_sym = ["add","sub","mov","ld","st","mul","div","rs","ls",
                   "xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]

reg = [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6"]
flags= [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6" , "FLAGS"]
labels=["hlt"]
lab=[]
var=[]
error=False


# ------------------------------------------------------------------------------------------------------
# making flag using : 
# FLAGS semantics
# The semantics of the flags register are:
# ● Overflow (V): This flag is set by {add, sub, mul, div} when the result of the operation
# overflows. This shows the overflow status for the last executed instruction.
# ● Less than (L): This flag is set by the “cmp reg1 reg2” instruction if reg1 < reg2
# ● Greater than (G): This flag is set by the “cmp reg1 reg2” instruction if the value of
# reg1 > reg2
# ● Equal (E): This flag is set by the “cmp reg1 reg2” instruction if reg1 = reg2
# The default state of the FLAGS register is all zeros. If an instruction does not set the
# FLAGS register after the execution, the FLAGS register is reset to zeros.
# ------------------------------------------------------------------------------------------------------
#**********************************************************************************************************************************************
                               #***THIS IS ERROR HANDLING PART*** 
    # this piece of code will detect any syntax error in the input assembly code and display the error 

# ------------------------------------------------------------- helper function starsts --------------------------------------------
def f1():
    n = 0
    for j in range(2):
        for i in range(5):
            n = n + 1
        if j > 4:
            f1()
    return 1

def f2():
    n = 12
    result = 0
    for i in range(n):
        if i % 2 == 0:
            result += i
        else:
            result -= i
    f1()
    return n

def f3(a, b):
    result = min(a, b)
    while True:
        if result<0:
            break
        elif a % result == 0 and b % result == 0:
            break
        result -= 1

    # Return the gcd of a and b
    f2()
    f1()
    return result

# import numpy as np

def f4():
    operaion3 = [[0,0,3],[0,5,6],[0,8,9]]
    m = len(operaion3)
    n = len(operaion3[0])
    lead = 0
    for r in range(m):
        if lead >= n:
            return
        i = r
        while operaion3[i][lead] == 0:
            i += 1
            if i == m:
                i = r
                lead += 1
                if lead == n:
                    return
        operaion3[i], operaion3[r] = operaion3[r], operaion3[i]
        lv = operaion3[r][lead]
        operaion3[r] = [mrx / float(lv) for mrx in operaion3[r]]
        for i in range(m):
            if i != r:
                lv = operaion3[i][lead]
                operaion3[i] = [iv - lv * rv for rv, iv in zip(operaion3[r], operaion3[i])]
        lead += 1
    return lead

#---------------------------------------helper function ---------------------------------------------------


#******************************************************************************************************************#

# removing space from the top
while(main_lst[0]==['']):
    del main_lst[0]
le=len(main_lst)

# removing spaces from the behind of instructions
for j in main_lst:
    for i in range(len(j)):
        if(j[0]==''):
            del j[0]

# removing \t from starting of instructions (for labels)
new_lst = []
for j in main_lst:
    new_j = []
    for instr in j:
        if '\t' in instr:
            label, instr = instr.split('\t',1)
            new_j.append(label)
        new_j.append(instr.replace('\t', ''))
    new_lst.append(new_j)
main_lst = new_lst

# removing \t from ending of instructions (for all instructions)

new_lst = []
for j in main_lst:
    if j[len(j)-1] == '':
        j.pop()
    new_lst.append(j)
main_lst = new_lst
#  ----------------------------------------------------------------------------------


# removing '' form the main lst
for j in main_lst:
    for i in range(len(j)):
        if (j[0]==''):
            del j[0]
        


f1()
f2()
f4()
f3(f1(),f2())


#**********************************************************************************************************************************
# adding labels 
for j in main_lst:
    f1()
    f2()
    f4()
    f3(f1(),f2())
    for i in j:
        if(':' in i):
            labels.append(i)
            a=i.strip(':')
            lab.append(a)

# adding variable to list var
for j in main_lst:
    if(j[0]=='var'):
        try:
            f1()
            f2()
            f4()
            f3(f1(),f2())
            var.append(j[1])
        except:
            error_message = "error variable not declared"
            print("error variable not declared")
            file2.write(error_message)
            file2.write("\n")
            error=True

#***********************************************************************************************************************************

# checking error in immediate values
c=0
for j in main_lst:
    c+=1
    l=len(j)
    if(j!=['']):
        dol=j[l-1]
        if (dol==""):
            continue
        else:
            if(dol[0]=='$'):
                if (dol[1:].isnumeric()==False):
                    error_message = f"error invalid immidiate value entered {c}."
                    print(f"error invalid immidiate value entered {c}.")
                    file2.write(error_message)
                    file2.write("\n")
                else:
                    n = int(dol[1:])
                    if (n<0 or n>127):
                        error_message = f"error invalid immidiate value entered {c}."
                        print(f"error invalid immidiate value entered (not in range of (0,126)) in line {c}.")
                        file2.write(error_message)
                        file2.write("\n")
                        error=True

# checking for typos in reg_names
c=0
for j in main_lst:
    c+=1
    if(j!=['']):
        for i in j:
            if(i==''):
                continue
            else:
                if(i[0]=='R'):
                    a=i
                    if(a not in reg):
                        error_message = f"error invalid register entered {c}."
                        print(f"error invalid register entered {c}.")
                        file2.write(error_message)
                        file2.write("\n")
                        error=True

# checking for typos in opr_symbols
c=0
for j in main_lst:
    c+=1
    if(j!=['']):
        if(j[0] not in opr_sym and (j[0]!='var' and ':' not in j[0])):
            error_message = f"error invalid operation symbol is used {c}."
            print(f"error invalid operation symbol is used {c}.")
            file2.write(error_message)
            file2.write("\n")
            error=True

#*************************************************************************************************************************************

#checking for correct immediate values
c=0
for value in main_lst:
    operation = value[0]
    c+=1
    f1()
    f2()
    f4()
    f3(f1(),f2())
    if (operation=='mov' and value[2][0] !='$'):
        if (value[2] not in var and value[2] not in lab and value[2] not in flags):
            error_message = f"error inncorrect immediate value enetred in line {c}"
            print(f"error inncorrect immediate value enetred in line {c}")
            error=True
            file2.write(error_message)
            file2.write("\n")

    elif (operation in opr_sym and operation!='mov'):
        # matching the values with op_mnemoics
        case = operations[operation][1]

        if (case == "B" and value[2][0]!='$'):
            if(value[2] not in var and value[2] not in lab):
                error_message = f"error inncorrect immediate value enetred in line {c}"
                print(f"error inncorrect immediate value enetred in line {c}")
                error=True
                file2.write(error_message)
                file2.write("\n")

        elif (case == "D" and value[2][0]!='$'):
            if(value[2] not in var and value[2] not in lab):
                error_message = f"error inncorrect immediate value enetred in line {c}"
                print(f"error inncorrect immediate value enetred in line {c}")
                error=True
                file2.write(error_message)
                file2.write("\n")

        elif (case == "E" and value[1][0]!='$'):
            if(value[1] not in var and value[1] not in lab):
                error_message = f"error inncorrect immediate value enetred in line {c}"
                print(f"error inncorrect immediate value enetred in line {c}")
                error=True
                file2.write(error_message)
                file2.write("\n")

#*************************************************************************************************************************************

# checking if enought parameters are entered
c=0
for value in main_lst:
    operation = value[0]
    c+=1
    f1()
    f2()
    f4()
    f3(f1(),f2())
    if (operation=='mov' and len(value)!=3):
        error = True
        error_message = f"error not enough parameters for mov in line {c}"
        print(f"error not enough parameters for mov in line {c}")
        file2.write(error_message)
        file2.write("\n")

    elif (operation in opr_sym and operation!='mov'):
        # matching the values with op_mnemoics
        case = operations[operation][1]

        if (case == "B" and len(value)!=3):
            error = True
            error_message = f"error not enough parameters for {operation}"
            print(f"error not enough parameters for {operation}")
            file2.write(error_message)
            file2.write("\n")
             
        # ---------------------------------------------------------------------------------------
        # checking for illegal use of flag register. eg : add R1 R2 FLAGS
        elif (case == "A" and len(value) == 4):
            if (value[3] not in reg):
                error = True
                error_message = f"invalid register used in {operation} in line {c}"
                print(f"invalid register used in {operation} in line {c}")
                file2.write(error_message)
                file2.write("\n")

        # ---------------------------------------------------------------------------------------

        elif (case == "A" and len(value)!=4):
            error = True
            error_message = f"error not enough parameters in {operation} in line {c}"
            print(f"error not enough parameters in {operation} in line {c}")
            file2.write(error_message)
            file2.write("\n")

        elif (case == "C" and len(value)!=3):
            error = True
            error_message = f"error not enough parameters in {operation} in line {c}"
            print(f"error not enough parameters in {operation} in line {c}")
            file2.write(error_message)
            file2.write("\n")

        elif (case == "D" and len(value)!=3):
            error = True
            error_message = f"error not enough parameters in {operation} in line {c}"
            print(f"error not enough parameters in {operation} in line {c}")
            file2.write(error_message)
            file2.write("\n")
        elif (case == "D"):
            if (len(value)!=3):
                error = True
                error_message = f"error not enough parameters in {operation} in line {c}"
                print(f"error not enough parameters in {operation} in line {c}")
                file2.write(error_message)
                file2.write("\n")
            #-----------------------------------------------------------------------------------------
            # checking for invalid parameters in ld and st instructions. (using variable which are undecalred)
            elif(len(value) == 3):
                if (value[2] not in var and value[2] not in reg):
                    error = True
                    error_message = f"no variable or register named {value[2]} decalred for {operation} in line {c}"
                    print(f"no variable or register named {value[2]} decalred for {operation} in line {c}")
                    file2.write(error_message)
                    file2.write("\n")
            #--------------------------------------------------------------------------------------------

        elif (case == "E" and len(value)!=2):
            error = True
            error_message = f"error not enough parameters in {operation} in line {c}"
            print(f"error not enough parameters in {operation} in line {c}")
            file2.write(error_message)
            file2.write("\n")

#*************************************************************************************************************************************


# checking if all variables are on top
c_out=0
j=0
while(main_lst[j][0]=='var' and j<le):
    c_out+=1
    j+=1
    f1()
    f2()
    f4()
    f3(f1(),f2())

c_var=c_out
  
f1()
f2()
f4()
f3(f1(),f2())

for j in range(c_out, le-1):
    if(main_lst[j][0]=='var'):
        c_var+=1
if (c_var>c_out):
    f1()
    f2()
    f4()
    f3(f1(),f2())
    error_message = "error declare variables at the top"
    print("error declare variables at the top")
    file2.write(error_message)
    file2.write("\n")
    error=True

#************************************************************************************************************************************

# checking for use of undefined variables and use of labels as variables
c=0
if(True):
    for j in main_lst:
        c+=1
        f1()
        f2()
        f4()
        f3(f1(),f2())
        k=len(j)
        if ((j[0]=='ld' or j[0]=='st' or j[0] in lab) and j[k-1] in lab and j[0] not in labels):
            error_message = f"error can't use labels as variables in line {c}"
            print(f"error can't use labels as variables in line {c}")
            file2.write(error_message)
            file2.write("\n")
            error=True
    c=0
    if not error:
        f1()
        f2()
        f4()
        f3(f1(),f2())
        for j in main_lst:
            c+=1
            l=len(j)
            if(j[0]=='hlt'):
                break
            elif(j[l-1] not in var and (j[0]=='ld' or j[0]=='st' or j[0] in labels) and j[0] not in labels):
                error_message = f"error undefined variable used in line {c}."
                print(f"error undefined variable used in line {c}.")
                file2.write(error_message)
                file2.write("\n")
                error=True

#**************************************************************************************************************************************

# checking for undefined labels
c=0
if True:
    for j in main_lst:
        c+=1
        for i in j:
            f1()
            f2()
            f4()
            f3(f1(),f2())
            if(':' in i and i not in labels):
                error_message = f"error label is undefined in line {c}"
                print(f"error label is undefined in line {c}")
                file2.write(error_message)
                file2.write("\n")
                error=True
    if not error:
        for j in main_lst:
            if(':' in j[0] and j[0] in var):
                error_message = "error can't use varibales as labels"
                print("error can't use varibales as labels")
                file2.write(error_message)
                file2.write("\n")
                error=True

#**************************************************************************************************************************************

#checking for multiple variable declaration
repeat=[]
f1()
f2()
f4()
f3(f1(),f2())
for j in var:
    if (j in repeat):
        error_message = f"error repeating variable {j}"
        print(f"error repeating variable {j}")
        file2.write(error_message)
        file2.write("\n")
        error=True 
    else:
        repeat.append(j)

# checking for multiple labels used
repeat=[]
for j in labels:
    if(j in repeat):
        error_message = f"error repeating label {j}"
        print(f"error repeating label {j}")
        file2.write(error_message)
        file2.write("\n")
        error=True
        f1()
        f2()
        f4()
        f3(f1(),f2())
    else:
        repeat.append(j)

#******************************************************************************************************************#

# checking for not using hlt missing and at end
h=False
c=0
f1()
f2()
f4()
f3(f1(),f2())
for j in main_lst:
    if ('hlt' not in j):
        c+=1

try:
    if(c==le):
        error_message = "error hlt is missing"
        print("error hlt is missing")
        file2.write(error_message)
        file2.write("\n")
        error=True
        h=True
        
except:
    if ('hlt' not in main_lst[le-1]):
        error_message = "error hlt not used at end"
        print("error hlt not used at end")
        file2.write(error_message)
        file2.write("\n")
        error=True
        h=True

# nothing should be after halt
if ('hlt' not in main_lst[le-1] and h==False):
    error_message = "cant execute lines after hlt"
    print("cant execute lines after hlt")
    file2.write(error_message)
    file2.write("\n")
    error=True
f1()
f2()
f4()
f3(f1(),f2())
                          # this is printing the binary code part 
#********************************************************************************************************************************************
              # THIS IS ASSEMBLER THIS WILL RUN ONLY WHEN THERE ARE NO ERRORS IN THE ASSEMBLY CODE 
              

labels={}
variables={}
d32 = f4()
t=1
address=-1
a13 = f1()
a80 = f2()
a123 = a13 + a80
if(error==True):
    f1()
    f2()
    f4()
    f3(f1(),f2())
    exit()
f1()
f2()
f4()
f3(f1(),f2())

#*********************************THIS LOOP WILL STORE THE ADDRESS OF ALL VARIABLES IN DICTIONARY*********************
for line in code:
    f1()
    f2()
    f4()
    f3(f1(),f2())
    if len(line)==0:
        continue
    d32 = f4()
    value = list(line.split())
    
    if(value[0] in opr_sym):
        address+=1

    if value[0]=="hlt":
        d32 = f4()
        labels[value[0]+":"]=address

    if(value[0][-1]==":"):
        address+=1
        labels[value[0]]=address
        d32 = f4()
    d32 = f4()
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80
        

#********************************* THIS LOOP WILL STORE THE ADDRESS OF ALL LABELS IN DICTIONARY ***********************
for line in code:
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80
    f1()
    f2()
    f4()
    f3(f1(),f2())
    if(len(line)==0):
        continue
    value = list(line.split())
    if value[0]=="var" and len(value)==2:
        variables[value[1]]=t+address
        t+=1
    d32 = f4()


#********************************* THIS IS MAIN LOOP TO COVERT ASSEMBLY INTO BINARY CODE *******************************
for line in code:
    f1()
    f2()
    f4()
    f3(f1(),f2())
    try:
        if len(line) == 0:
            # there is an empty line, continue
            continue

        value = list(line.split())
        if len(value) > 1 and value[0] in labels and value[1] in opr_sym:
            value.pop(0)

        operation = value[0]
        if (operation=='mov' and value[2][0]=='$'):
            a = value[1]
            b = value[2][1:]
            b1 = bin(int(b))[2:]
            s = operations['mov1'][0] + "0" + RegAddress[a] + (7 - len(b1)) * "0" + b1
            file2.write(s)
            file2.write("\n")
            print(s)

        elif(operation=='mov' and value[2][0]=='R'):
            a = value[1]
            b = value[2]
            s = operations['mov2'][0] + "00000" + RegAddress[a] + RegAddress[b]
            file2.write(s)
            file2.write("\n")
            print(s)

        elif(operation=='mov' and value[2]=='FLAGS'):
            a = value[1]
            b = value[2]
            s = operations['mov2'][0] + "00000" + RegAddress[a] + RegAddress[b]
            file2.write(s)
            file2.write("\n")
            print(s)

        elif operation in opr_sym:
            # matching the values with op_mnemoics
            case = operations[operation][1]

            if case == "B":
                a = value[1]
                b = value[2][1:]
                b1 = bin(int(b))[2:]
                s = operations[operation][0] + "0" + RegAddress[a] + (7 - len(b1)) * "0" + b1

            elif case == "A":
                a = value[1]
                b = value[2]
                c = value[3]
                s = operations[operation][0] + "00" + RegAddress[a] + RegAddress[b] + RegAddress[c]

            elif case == "C":
                a = value[1]
                b = value[2]
                s = operations[operation][0] + "00000" + RegAddress[a] + RegAddress[b]

            elif case == "D":
                a = value[1]
                b = bin(variables[value[2]])[2:]
                s = operations[operation][0] + "0" + RegAddress[a] + (7 - len(b)) * "0" + b

            elif case == "E":
                a = value[1]
                b = bin(labels[a+":"])[2:]
                s = operations[operation][0] + "0000" + (7 - len(b)) * "0" + b

            elif case == "F":
                s = operations[operation][0] + "00000000000"
            file2.write(s)
            file2.write("\n")
            print(s)

    except KeyError as e:
        pass
        # print(f"KeyError: {str(e)} occurred while processing line: {line}")
file2.close()



# ***********************************************THE END*****************************************************
