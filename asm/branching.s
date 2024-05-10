# test for branching

addi x0, x0, 10 # x0 = 0x + 10
# x0 is 10
addi x1, x1, 10 # x1 = 1x + 15
# x1 is 10


bne x0, x1, test



test:
    add x2, x0, x1


addi x2, x3, 10