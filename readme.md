# RISCY
A successor to an older project called 'Asmpy', meant to be actually in line with RISC-V.

I made Asmpy when I was less experienced with making interpreters and Python in general, so it's badly written.

RISCY is much better written since I have way more experience now!(if you're a Python expert reading this, I'm so sorry)

And not only that, it is(or will be, at least) be written in multiple languages.



## Actually interesting stuff
The only things that are different from RISC-V are the 'n'(Next) register<br>
```
# adds x0 + 10 to the next register that is 0
ADDI n, x0, 10

# adds x1 + 22 to the next register that is 20
ADDI n20, x1, 22

# if the given number to check for doesn't exist in any register, then it will default to zero and print a warning to the console

# using the 'n' register is completely optional, of course
```

And that commas nor capitalization of instructions are needed.
```
# valid
ADDI x0, x0, 10

# also valid
addi x1 x1 10

# things like this are also valid but that's just disgusting
# aDdI, x2  X2,    10
```

<br><br>

### Instructions currently implemented

Inst | Name | Summary
--- | --- | ---
add | ADD | rd = rs1 + rs2
sub | SUB | rd = rs1 - rs2
and | AND | rd = rs1 & rs2
or | OR | rd = rs1 | rs2
xor | XOR | rd = rs1 ^ rs2
sll | Shift Left Logical | rd = rs1 << rs2
srl | Shift Right Logical | rd = rs1 >> rs2
slt | Set Less Than | rd = (rs1 < rs2)?1:0
addi | ADD Immediate | rd = rs1 + imm
andi | AND Immediate | rd = rs1 & imm
ori | OR Immediate | rd = rs1 | imm
xori | XOR Immediate | rd = rs1 ^ imm
slli | Shift Left Logical Imm | rd = rs1 << imm
srli | Shift Right Logical Imm | rd = rs1 >> imm
slti | Set Less Than Imm | rd = (rs1 < imm)?1:0
beq | Branch == | if(rs1 == rs2) PC += imm or label
bne | Branch != | if(rs1 != rs2) PC += imm or label
blt | Branch < | if(rs1 < rs2) PC += imm or label
bqe | Branch >= | if(rs1 >= rs2) PC += imm or label

<!--
#### Non-standard/custom instructions
Inst | Name | Summary
--- | --- | ---
-->


## Interpreters
Currently, the only interpreter I've made is in Python, but I'll be making one in Go later.<br>
I might also make some in other languages(maybe in Rust? 😜).

## CRISP
The CRISP(no, I'm not British) format is a bytecode format for the RISCY interpreters.<br>
While yes, it is entirely useless, it does have *some* perks.<br>
It's smaller than a normal .s file because it forfeits all those useless things like 'spaces' and 'comments'(ew), allowing for less space used.

TL;DR, it's like Java bytecode, but it's not Java so it's automatically superior.
<br><br><br>
Currently the only CRISP compiler I've made is in Python, etc etc.

<br>

## Too be honest, I don't really know what I'm doing?
I honestly don't really understand a lot of stuff.<br>
Like, why does the [SAR_example](/asm/SAR_example.s) not use any registers lower than x18?<br>
And what does the `LUI` instruction do, exactly?<br>
so if you have the explaination, I would appreciate if you made an issue about it!