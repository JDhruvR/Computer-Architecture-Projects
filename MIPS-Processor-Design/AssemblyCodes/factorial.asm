.text
.globl main

main:
	lw $s0,0($0)		#value of n
	
	addi $s1,$0,1		#ans
	
	addi $s2,$0,1		#i	
	
loop:

	mul $s1,$s1,$s2
	addi $s2,$s2,1
	ble $s2,$s0,loop
	
	sw $s1,4($0)
