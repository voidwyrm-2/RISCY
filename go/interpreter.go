package main

import (
	"fmt"
	"slices"
	"strings"
)

var OPCODES = map[string]int{
	"sep":  0,
	"addi": 1,
	"andi": 2,
	"ori":  3,
	"xori": 4,
	"slti": 5,
	"srli": 6,
	"slli": 7,
	"add":  8,
	"sub":  9,
	"and":  10,
	"or":   11,
	"xor":  12,
	"slt":  13,
	"srl":  14,
	"sll":  15,
	"beq":  16,
	"bne":  17,
	"bge":  18,
	"blt":  19,

	"label":               20,
	"inside_label":        21,
	"imm":                 22,
	"idx_register_call":   23,
	"nxt_register_call":   24,
	"illegal_instruction": 25,
}

type Failure struct {
	Error_type string
	Details    string
	Line       int
}

func (f Failure) Error() string {
	out := ""
	if f.Details != "" {
		out = fmt.Sprintf("%s: %s", f.Error_type, f.Details)
		out = strings.TrimSpace(out)
	} else {
		out = f.Error_type
	}
	if f.Line >= 0 {
		out += fmt.Sprintf(" on line %d", f.Line+1)
	}
	return out
}

func callRegister(registers_list []int, labels map[string]int, linenum, rm_lines int, instruction, to, first, second string) ([]int, int, error) {

	return registers_list, linenum, nil
}

func Interpreter(code string) {
	//registers := make([]int, 32)
	idx := 0

	lines := strings.Split(strings.ToLower(strings.ReplaceAll(strings.ReplaceAll(code, ", ", " "), ",", " ")), "\n")

	//var instruction_cache []int

	for {
		l := strings.Split(strings.TrimSpace(lines[idx]), " ")

		for slices.Index(l, "") > -1 {
			i := slices.Index(l, "")
			l = slices.Delete(l, i, i+1)
		}

		if len(l) == 0 {
			idx++
			continue
		} else if len(l) < 4 {
			fmt.Println(Failure{"SyntaxError", fmt.Sprintf("not enough arguments for instruction '%s'", l[0]), idx}.Error())
			return
		} else if len(l) == 4 {
			return
		} else if len(l) > 4 {
			fmt.Println(Failure{"SyntaxError", fmt.Sprintf("unneeded argument '%s' argument for instruction '%s'", l[4], l[0]), idx}.Error())
			return
		}
	}
}
