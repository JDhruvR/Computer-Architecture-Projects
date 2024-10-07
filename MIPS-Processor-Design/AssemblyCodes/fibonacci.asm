.text
.globl main
main:
	lw $s0, 0($0) 		 #M[0] contains Input

	addi $s1,$0,0 		 #fib[0]=0
	addi $s2,$0,1 		 #fib[1]=1
	addi $s3,$0,0 		 #fib[2]=0

	addi $s4,$0,0 		 #i=0
loop:
        
	add $s3, $s1, $s2    #fib[2]=fib[1]+fib[0]
	
	add $s1, $s2, $0     #fib[1]=fib[0]
	add $s2, $s3, $0 	 #fib[2]=fib[1]
	
	add $s4, $s4, 1      #i++ for the loop

	bne $s4, $s0, loop 	 #run this loop from 0 to x
	
	sw $s1, 4($0)		 #Stores fib[0] in M[4]
