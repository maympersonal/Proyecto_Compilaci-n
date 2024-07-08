main:
move $t1, $fp
move $fp, $sp
addiu $sp, $sp, -4
sw $sp, 0($ra)
addiu $sp, $sp, -4
sw $t1, 0($sp)
addiu $sp, $sp, -4
li $t5, 3
sw $t5, 0($fp)
lw $a0, 0($fp)
li $v0, 1
syscall
li $v0, 10
syscall