'''
    CSE 112 - Computer Organisation group project.
        group members :
            Aditya Sharma
            Ayaan kumar
            Aayan hasan
            Kanishk kumar meena
'''


# ------------------------------------------taking input throught a text file contating assemble code------------------------------------------------------
with open('test_case1.txt') as f:  
    code = f.read().splitlines() 

# -----------------------------------------------input code ends---------------------------------------------
 # ACTUAL CODE STARTS FORM HERE  


main_lst=[]
for i in code:
    a=i.split(' ')
    main_lst.append(a)
le=len(main_lst)


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
   "mov2":["00011","C"], # mov immediate but with register
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

import numpy as np


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
    return 

#---------------------------------------helper function ---------------------------------------------------


#******************************************************************************************************************#

# checking error in immediate values

c=0
for j in main_lst:
    c+=1
    l=len(j)
    if(j!=['']):
        dol=j[l-1]
        if (dol[0]=='$'):
            n = int(dol[1:])
            if (n<0 or n>256):
                print(f"error invalid immidiate value entered {c}.")

# checking for typos in reg_names and opr_symbols
c=0
for j in main_lst:
    c+=1
    if(j!=['']):
        for i in j:
            if(i[0]=='R'):
                a=i
                if(a not in reg):
                    print(f"error invalid register entered {c}.")

# checking for typos in opr_symbols
c=0
for j in main_lst:
    c+=1
    if(j!=['']):
    #var not declred at top how
        if(j[0] not in opr_sym and (j[0]!='var' and ':' not in j[0])):
            print(f"error invalid operation symbol is used {c}.")

#*************************************************************************************************************************************
# adding labels 

for j in main_lst:
    for i in j:
        if(':' in i):
            labels.append(i)
            a=i.strip(':')
            lab.append(a)

# adding variable to list var
for j in main_lst:
    if(j[0]=='var'):
        try:
            var.append(j[1])
        except:
            print("error variable not declared")

#***********************************************************************************************************************************

# checking if all variables are on top
c_out=0
j=0
while(main_lst[j][0]=='var' and j<le):
    c_out+=1
    j+=1

c_var=c_out

for j in range(c_out, le-1):
    if(main_lst[j][0]=='var'):
        c_var+=1
if (c_var>c_out):
    print("error declare variables at the top")

#************************************************************************************************************************************

# checking for use of undefined variables and use of labels as variables
c=0
try:
    for j in main_lst:
        c+=1
        k=len(j)
        if ((j[0]=='ld' or j[0]=='st' or j[0] in lab) and j[k-1] in lab and j[0]!='end:'):
            print(f"error can't use labels as variables in line {c}")
except:
    for j in main_lst:
        c+=1
        l=len(j)
        if(j[l-1] not in var and (j[0]=='ld' or j[0]=='st' or j[0] in labels) and j[0]!='end:'):
            print(f"error undefined variable used in line {c}.")

#**************************************************************************************************************************************

# checking for undefined labels
c=0
try:
    for j in main_lst:
        c+=1
        for i in j:
            if(':' in i and i not in labels):
                print(f"error label is undefined in line {c}")
except:
    for j in main_lst:
        if(':' in j[0] and j[0] in var):
            print("error can't use varibales as labels")

#**************************************************************************************************************************************

#checking for multiple variable declaration
repeat=[]
for j in var:
    if (j in repeat):
        print(f"error repeating variable {j}") 
    else:
        repeat.append(j)

# checking for multiple labels used

repeat=[]
for j in labels:
    if(j in repeat):
        print(f"error repeating label {j}")
    else:
        repeat.append(j)

#******************************************************************************************************************#

# checking for not using hlt missing and at end
c=0
for j in main_lst:
    if ('hlt' not in j):
        c+=1

try:
    if(c==le):
        print("error hlt is missing")
except:
    if ('hlt' not in main_lst[le-1]):
        print("error hlt not used at end")


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
    exit()


#*********************************THIS LOOP WILL STORE THE ADDRESS OF ALL VARIABLES IN DICTIONARY*********************
for line in code:
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
    if(len(line)==0):
        continue
    value = list(line.split())
    if value[0]=="var" and len(value)==2:
        variables[value[1]]=t+address
        t+=1
    d32 = f4()


#********************************* THIS IS MAIN LOOP TO COVERT ASSEMBLY INTO BINARY CODE *******************************
for line in code:
    try:
        if len(line) == 0:
            # there is an empty line, continue
            continue

        value = list(line.split())
        if len(value) > 1 and value[0] in labels and value[1] in opr_sym:
            value.pop(0)

        operation = value[0]
        if operation in opr_sym:
            # matching the values with op_mnemoics
            case = operations[operation][1]

            if case == "B":
                a = value[1]
                b = value[2][1:]
                b1 = bin(int(b))[2:]
                s = operations[operation][0] + RegAddress[a] + (8 - len(b1)) * "0" + b1

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
                s = operations[operation][0] + RegAddress[a] + (8 - len(b)) * "0" + b

            elif case == "E":
                a = value[1]
                b = bin(labels[a+":"])[2:]
                s = operations[operation][0] + "000" + (8 - len(b)) * "0" + b

            elif case == "F":
                s = operations[operation][0] + "00000000000"

            print(s)

    except KeyError as e:
        pass
        # print(f"KeyError: {str(e)} occurred while processing line: {line}")



# ***********************************************THE END*****************************************************
