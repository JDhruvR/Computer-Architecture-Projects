class MIPSProc:

	def __init__(self, machineCode, dataMemory):
		self.reg=[0]*32; #Initialising of Register File
		self.pc=4194304; #Initialising of PC
		
		self.machineCode=machineCode;
		self.dataMemory=dataMemory;
		self.opcodeReference={'000000':'rFormat', '001000':'addi', '100011':'lw', '101011':'sw', '011100':'mul', '000100':'beq', '000101':'bne', '000010':'j'}; #Reference Dictionary for Instruction Decode
		self.hilo=[0]*2;

		while(self.pc in self.machineCode):
			instruction=MIPSProc.fetchInstruction(self); #IF Stage
			self.pc+=4; #PC=PC+4;
			eval('MIPSProc.'+self.opcodeReference[instruction[0:6]])(self, instruction); #Instruction Decode part of ID Stage
        
	def fetchInstruction(self): #IF Stage
		
		return self.machineCode[self.pc];

	def rFormat(self, instruction):
		#ADD
		if(instruction[26:32]=='100000'):
			#Register Read part of ID Stage

			rs=self.reg[int(instruction[6:11], 2)];
			rt=self.reg[int(instruction[11:16], 2)];

			#ALU Stage

			opResult=rs+rt; #rd=rs+rt

			#MEM Stage is not used

			#WB Stage

			self.reg[int(instruction[16:21], 2)]=opResult;

		#SLT
		elif(instruction[26:32]=='101010'):
			#Register Read part of ID Stage

			rs=self.reg[int(instruction[6:11], 2)];
			rt=self.reg[int(instruction[11:16], 2)];

			#ALU Stage

			if(rs<rt):
				opResult=1;
			else:
				opResult=0;

			#MEM Stage is not used

			#WB Stage

			self.reg[int(instruction[16:21], 2)]=opResult;

		#DIV
		elif(instruction[26:32]=='011010'):
			#Register Read part of ID Stage

			rs=self.reg[int(instruction[6:11], 2)];
			rt=self.reg[int(instruction[11:16], 2)];

			#ALU Stage

			self.hilo[0]=rs%rt;
			self.hilo[1]=rs//rt;

			#MEM Stage is not used

			#WB Stage is not used

		#MFHI
		elif(instruction[26:32]=='010000'):
			#Register Read part of ID Stage is not used

			#ALU Stage is not used.

			#MEM Stage is not used

			#WB Stage

			self.reg[int(instruction[16:21], 2)]=self.hilo[0];

	def addi(self, instruction):
		#Register Read part of ID Stage

		rs=self.reg[int(instruction[6:11], 2)];

		#ALU Stage

		opResult=rs+int(instruction[16::], 2);

		#MEM Stage is not used

		#WB Stage

		self.reg[int(instruction[11:16], 2)]=opResult;

	def lw(self, instruction):
		#Register Read part of ID Stage

		rs=self.reg[int(instruction[6:11], 2)];

		#ALU Part

		opResult=rs+int(instruction[16::], 2);

		#MEM Stage

		opResult=self.dataMemory[268500992+opResult];

		#WB Stage

		self.reg[int(instruction[11:16], 2)]=opResult;

	def sw(self, instruction):
		#Register Read part of ID Stage

		rs=self.reg[int(instruction[6:11], 2)];
		rt=self.reg[int(instruction[11:16], 2)];

		#ALU Part

		opResult=rs+int(instruction[16::], 2);

		#MEM Stage

		self.dataMemory[268500992+opResult]=rt;

		#WB Stage is not used

	def mul(self, instruction):
		#Register Read part of ID Stage

		rs=self.reg[int(instruction[6:11], 2)];
		rt=self.reg[int(instruction[11:16], 2)];

		#ALU Stage

		opResult=rs*rt; #rd=rs+rt

		#MEM Stage is not used

		#WB Stage

		self.reg[int(instruction[16:21], 2)]=opResult;

	def j(self, instruction):
		#Register Read part of ID Stage is not used

		#ALU Stage
		
		self.pc=int(instruction[6::]+'00', 2);

		#MEM Stage is not used

		#WB Stage

	def beq(self, instruction):
		#Register Read part of ID Stage

		rs=self.reg[int(instruction[6:11], 2)];
		rt=self.reg[int(instruction[11:16], 2)];

		#ALU Stage

		if(rs==rt):
			if(instruction[16::][0]=='1'):
				binstr='';
				for char in instruction[16::]:
					if(char=='1'):
						binstr+='0';
					else:
						binstr+='1';
				self.pc-=4*(int(binstr, 2)+1);
			else:
				self.pc+=4*(int(instruction[16::], 2));

		#MEM Stage is not used

		#WB Stage is not used

	def bne(self, instruction):
		#Register Read part of ID Stage

		rs=self.reg[int(instruction[6:11], 2)];
		rt=self.reg[int(instruction[11:16], 2)];

		#ALU Stage

		if(rs!=rt):
			if(instruction[16::][0]=='1'):
				binstr='';
				for char in instruction[16::]:
					if(char=='1'):
						binstr+='0';
					else:
						binstr+='1';
				self.pc-=4*(int(binstr, 2)+1);
			else:
				self.pc+=4*(int(instruction[16::], 2));

		#MEM Stage is not used

		#WB Stage is not used

################################################################################################################################################################

y=int(input("What program do you want to run? (1 for factorial, 2 for fibonacci, 3 for prime, else exit): "));
x=int(input("Enter Input: "));

if(y==1):
	machineCode={ #fact
		4194304:'10001100000100000000000000000000',
		4194308:'00100000000100010000000000000001',
		4194312:'00100000000100100000000000000001',
		4194316:'01110010001100101000100000000010',
		4194320:'00100010010100100000000000000001',
		4194324:'00000010000100100000100000101010',
		4194328:'00010000001000001111111111111100',
		4194332:'10101100000100010000000000000100'
		}
	dataMemory={ #fact
		268500992:x,
		268500996:0
	}

	myproc=MIPSProc(machineCode, dataMemory);
	print(dataMemory[268500996]);

elif(y==2):
	machineCode={ #fib
		4194304:'10001100000100000000000000000000',
		4194308:'00100000000100010000000000000000',
		4194312:'00100000000100100000000000000001',
		4194316:'00100000000100110000000000000000',
		4194320:'00100000000101000000000000000000',
		4194324:'00000010001100101001100000100000',
		4194328:'00000010010000001000100000100000',
		4194332:'00000010011000001001000000100000',
		4194336:'00100010100101000000000000000001',
		4194340:'00010110100100001111111111111011',
		4194344:'10101100000100010000000000000100'
		}
	dataMemory={ #fib
		268500992:x,
		268500996:0
	}

	myproc=MIPSProc(machineCode, dataMemory);
	print(dataMemory[268500996]);

elif(y==3):
	machineCode={ #prime
		4194304:'10001100000100000000000000000000',
		4194308:'00100000000100100000000000000001',
		4194312:'00100000000101000000000000000001',
		4194316:'00010010000000000000000000001011',
		4194320:'00010010000100100000000000001010',
		4194324:'00000010010100101001000000100000',
		4194328:'00010010000100100000000000001001',
		4194332:'00100000000100110000000000000010',
		4194336:'00000010000100110000000000011010',
		4194340:'00000000000000000100100000010000',
		4194344:'00010001001000000000000000000100',
		4194348:'00100010011100110000000000000001',
		4194352:'00010110011100001111111111111011',
		4194356:'00100000000101000000000000000001',
		4194360:'00001000000100000000000000010000',
		4194364:'00100000000101000000000000000000',
		4194368:'10101100000101000000000000000100'
		}
	dataMemory={ #prime
		268500992:x,
		268500996:0
	}

	myproc=MIPSProc(machineCode, dataMemory);
	print(dataMemory[268500996]);


