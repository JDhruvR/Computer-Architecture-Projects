class IAS:
	def __init__(self, memory):
		# initialisation of different registers of the processor
		self.memory=memory;
		self.ac=0;
		self.mq=0;
		self.pc=1;
		self.mar='';
		self.mbr='';
		self.ir='';
		self.ibr='';
		self.isleft=True;
		# loop to execute all the instructions in the right order. conidition is that if 
		while(True): # self.memory[1][0][self.pc][0:8]!='00000000' or self.memory[1][1][self.pc][0:8]!='00000000' i.e it breaks if instruction is HALT

			if(self.ibr!=''): # if ibr is not empty then ir<-ibr[0:8] mar<-ibr[8::] pc++ and we empty the ibr. 
				self.ir=self.ibr[0:8];
				self.mar=self.ibr[8::];
				self.pc+=1;
				
				self.ibr='';

			else: # if ibr is empty... mar<-pc and mbr<- leftinstruction[pc] + rightinstruction[pc]
				self.mar=self.pc;
				self.mbr=[memory[1][0][self.mar], memory[1][1][self.mar]];

				if(self.isleft): # if left instruction is required... ibr<-rightinstruction[pc] and ir<-leftinstruction[0:8] and mar<-leftinstruction[pc][8::]
					self.ibr=self.mbr[1];
					self.ir=self.mbr[0][0:8];
					self.mar=self.mbr[0][8::];

				else: # if left instruction is not required... ir<-rightinstruction[pc][0:8] and mar<-rightinstruction[8::]. we return back is isleft=True for the next iteration. pc++.
					self.ir=self.mbr[1][0:8];
					self.mar=self.mbr[1][8::];
					self.isleft=True;
					self.pc+=1;

			print(f'pc- {self.pc} mbr- {self.mbr} ibr- {self.ibr} ir- {self.ir} mar- {self.mar} '); # printing to show updated value of a few important, frequently changed registers

			# this is the decode-ir part of the processor. below if elif elif.... else block is self explanatory. calling respective functions.
			if(self.ir=='00001010'):
				print('LOAD');
				
				IAS.load(self);
		
			elif(self.ir=='00100001'):
				print('STOR');
				
				IAS.stor(self);
		
			elif(self.ir=='00001100'):
				print('DIV');
				
				IAS.div(self);
		
			elif(self.ir=='00001110'):
				print('JUMPRIGHT');
				
				IAS.jumpright(self);
		
			elif(self.ir=='00001111'):
				print('JUMPPLUSLEFT');
				
				IAS.jumpplusleft(self);
		
			elif(self.ir=='00000101'):
				print('ADD');
				
				IAS.add(self);
		
			elif(self.ir=='10000000'):
				print('COMPARE1');
				
				IAS.compare1(self);
		
			elif(self.ir=='10000001'):
				print('COMPARE2');
				
				IAS.compare2(self);
		
			elif(self.ir=='00000000'): # HALTing by putting a break statement. no function has been made for this.
				print('HALT');

				break;

	def load(self): # mbr<-M(X) ac<-mbr
		self.mbr=self.memory[0][int(self.mar, 2)];
		self.ac=self.mbr;
		
		print("mbr-", bin(self.mbr)[2::], " ac-", self.ac);

	def stor(self): # mbr<-ac M(x)<-mbr
		self.mbr=self.ac;
		self.memory[0][int(self.mar, 2)]=int(self.mbr);
		
		print(f'mbr- {bin(self.mbr)[2::]} M({int(self.mar, 2)})- {self.mbr}');

	def jumpright(self): # pc<-X
		self.isleft=False;
		self.pc=int(self.mar, 2)-5;
		self.ibr='';
		
		print("pc-", self.pc);

	def jumpplusleft(self):
		if(self.ac>=0): # check if ac is non-negative. if True: pc=X else do nothing.
			self.isleft=True;
			self.pc=int(self.mar, 2)-5;
			self.ibr='';

		else:
			pass;

		print("pc-", self.pc);

	def div(self): # ac=ac%M(x) mq=ac/M(X)
		self.ac=self.ac%(self.memory[0][int(self.mar, 2)]);
		self.mq=self.ac//(self.memory[0][int(self.mar, 2)]);
		
		print("ac-", self.ac, "mq-", self.mq);

	def add(self): # ac=ac+M(X)
		self.ac+=self.memory[0][int(self.mar, 2)];
		
		print("ac-", self.ac);

	def compare1(self): # check if ac>M(X) if true ac=1 else ac=-1
		if(self.ac>self.memory[0][int(self.mar, 2)]):
			self.ac=1;
		else:
			self.ac=-1;
		
		print("ac-", self.ac);

	def compare2(self): # check if ac>=M(X) if true ac=1 else ac=-1
		if(self.ac>=self.memory[0][int(self.mar, 2)]):
			self.ac=1;
		else:
			self.ac=-1;
		
		print("ac-", self.ac);

#################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
# input number to be checked for prime
a=int(input()); 
# this list represents the datapart of our IAS Processor Memory
datapart=[0,a,0,1,0,0]; 
# this list represents the instruction part of our IAS Processor Memory. this list consists of two lists, 0th represents list of left instructions. 1th is list of rightinstruction
instructionpart=[['leftinstruction','0000101000001', '0000111101001', '0010000100100', '0000101000010', '0000101000011', '0010000100000', '0000111110011', '0000110000000', '0000111110001', '0010000100101', '0010000100100', '0000101000000', '0010000100000', '0000101000011', '0000000000000'], ['rightinstruction', '1000000000011', '0000101000010', '0000111010100', '0010000100101', '0000010100011', '1000000100001', '0000101000001', '1000000000010', '0000101000011', '0000101000010', '0000111010100', '0000010100011', '0000111001011', '0010000100100', '0000000000000']]
# feeding the datapart and instruction part to memory for our processor
iasProcessor=IAS([datapart, instructionpart]);
# printing the output of our program. 0 if a is not a prime and 1 if it is.
print(iasProcessor.memory[0][4]);