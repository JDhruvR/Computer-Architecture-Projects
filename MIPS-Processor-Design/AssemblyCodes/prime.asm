.text
.globl main
main:
	lw $s0, 0($0) 		#M[0] contains Input

	addi $s2,$0,1 		#1
	addi $s4,$0,1 		#flag=1

	beq  $s0,$0,flag  	#if inp=0
	beq  $s0,$s2,flag 	#if inp=1
	add $s2, $s2, $s2 	#s2=2
	beq  $s0, $s2,check #if inp==2 

	addi $s3,$0,2 		#i=2

loop:
	div $s0,$s3			#hi=s0/s3
	mfhi $t1			#t1=s0%s3
	beq $t1,$0,flag
	add $s3, $s3, 1     #i++ for the loop
	bne $s3, $s0, loop 	#run this loop from 0 to x
	addi $s4,$0,1 		#flag=1
	j   check
flag:
	addi $s4,$0,0		#flag=0
check:
	sw $s4, 4($0) 		#store the output
