def binconverter(a): #for instruction line number, converts it to a unique binary code.
	if(len(a)<5):
		return ((5-len(a))*'0')+a;
	else:
		return a;

assemblycodefile=open("IMT2023032_assemblycode.txt","r")
codelist=assemblycodefile.readlines();
leftinstruction=[];
rightinstruction=[];
for s in codelist: #s contains a line of two instructions. 
	a=s.split(" "); #breaks it into 4 parts. 0th and 2nd are opcode parts and 1st and 3rd are address parts
	#encode starts for left instructions
	if("LOAD"==a[0]):
		leftinstruction.append("00001010"+str(a[1][2:7]));
	elif("JUMP"==a[0]):
		leftinstruction.append("00001110"+binconverter(str(bin(int(a[1][2:4])+5))[2::]));
	elif("JUMP+"==a[0]):
		leftinstruction.append("00001111"+binconverter(str(bin(int(a[1][2:4])+5))[2::]));
	elif("STOR"==a[0]):
		leftinstruction.append("00100001"+str(a[1][2:7]));
	elif("DIV"==a[0]):
		leftinstruction.append("00001100"+str(a[1][2:7]));
	elif("ADD"==a[0]):
		leftinstruction.append("00000101"+str(a[1][2:7]));
	elif("COMPARE1"==a[0]):
		leftinstruction.append("10000000"+str(a[1][2:7]));
	elif("COMPARE2"==a[0]):
		leftinstruction.append("10000001"+str(a[1][2:7]));
	elif("HALT"==a[0]):
		leftinstruction.append("0000000000000");
	#encode for right instructions
	if("LOAD"==a[2]):
		rightinstruction.append("00001010"+str(a[3][2:7]));
	elif("JUMP"==a[2]):
		rightinstruction.append("00001110"+binconverter(str(bin(int(a[3][2:4])+5))[2::]));
	elif("JUMP+"==a[2]):
		rightinstruction.append("00001111"+binconverter(str(bin(int(a[3][2:4])+5))[2::]));
	elif("STOR"==a[2]):
		rightinstruction.append("00100001"+str(a[3][2:7]));
	elif("DIV"==a[2]):
		rightinstruction.append("00001100"+str(a[3][2:7]));
	elif("ADD"==a[2]):
		rightinstruction.append("00000101"+str(a[3][2:7]));
	elif("COMPARE1"==a[2]):
		rightinstruction.append("10000000"+str(a[3][2:7]));
	elif("COMPARE2"==a[2]):
		rightinstruction.append("10000001"+str(a[3][2:7]));
	elif("HALT"==a[2]):
		rightinstruction.append("0000000000000");

#to get the instruction in list form to hardcode into our processor.
#print(leftinstruction);
#print(rightinstruction); 

for i in range(len(leftinstruction)): #printing the left and right instruction
	print(leftinstruction[i], " ", rightinstruction[i]);

assemblycodefile.close();

#jump will be in binary convert it to int 
