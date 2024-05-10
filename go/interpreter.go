package main

import (
	"fmt"
	"slices"
	"strconv"
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

func isDigit(s string) bool {
	_, err := strconv.Atoi(s)
	return err == nil
}

// does not return an error, only use you are sure the string is valid
func toInt(s string) int {
	i, _ := strconv.Atoi(s)
	return i
}

func boolToInt(b bool) int {
	if b {
		return 1
	}
	return 0
}

func verifyregcal(regs []int, ln, rml int, regcal string, imm int) (int, string, error) {
	invalid := Failure{"InvalidRegisterCallError", fmt.Sprintf("invalid register index '%s'", regcal), ln + rml}

	if imm == 1 && isDigit(regcal) {
		i, e := strconv.Atoi(regcal)
		return i, "", e
	} else if imm == 0 && isDigit(regcal) {
		return 0, "", Failure{"InvalidRegisterCallError", fmt.Sprintf("invalid register index '%s'(did you try to use a non-immediate instruction as an immediate instruction?)", regcal), ln + rml}
	} else if imm == 2 && !isDigit(regcal) {
		return 0, regcal, nil
	} else if regcal[:1] == "x" {
		if isDigit(regcal[1:]) {
			i := toInt(regcal[1:])
			if i < len(regs) {
				return i, "", nil
			}
		}
	} else if regcal == "zero" {
		return 0, "", nil
	}

	return 0, "", invalid
}

func callRegister(registers_list []int, labels map[string]int, linenum, rm_lines int, instruction, to, first, second string) ([]int, int, error) {
	immediate := 0
	if strings.HasSuffix(instruction, "i") {
		immediate = 1
	}
	r1, _ /*r1_S*/, err1 := verifyregcal(registers_list, linenum, rm_lines, to, immediate)
	r2, _ /*r2_S*/, err2 := verifyregcal(registers_list, linenum, rm_lines, first, immediate)
	if instruction == "beq" || instruction == "bne" || instruction == "bge" || instruction == "blt" {
		immediate = 2
	}
	r3, _ /*r3_S*/, err3 := verifyregcal(registers_list, linenum, rm_lines, second, immediate)
	if err1 != nil {
		return []int{}, 0, err1
	}
	if err2 != nil {
		return []int{}, 0, err2
	}
	if err3 != nil {
		return []int{}, 0, err3
	}

	switch instruction {
	// immediates
	case "addi":
		registers_list[r1] = registers_list[r2] + r3
	//case "subi":
	//	registers_list[r1] = registers_list[r2] - r3
	case "andi":
		registers_list[r1] = registers_list[r2] & r3
	case "ori":
		registers_list[r1] = registers_list[r2] | r3
	case "xori":
		registers_list[r1] = registers_list[r2] ^ r3
	case "slti":
		registers_list[r1] = boolToInt(registers_list[r2] < r3)
	//case "sgti":
	//	registers_list[r1] = boolToInt(registers_list[r2] > r3)
	case "srli":
		registers_list[r1] = registers_list[r2] >> r3
	case "slli":
		registers_list[r1] = registers_list[r2] << r3

	// non-immediates
	case "add":
		registers_list[r1] = registers_list[r2] + registers_list[r3]
	case "sub":
		registers_list[r1] = registers_list[r2] - registers_list[r3]
	case "and":
		registers_list[r1] = registers_list[r2] & registers_list[r3]
	case "or":
		registers_list[r1] = registers_list[r2] | registers_list[r3]
	case "xor":
		registers_list[r1] = registers_list[r2] ^ registers_list[r3]
	case "slt":
		registers_list[r1] = boolToInt(registers_list[r2] < registers_list[r3])
	//case "sgt":
	//	registers_list[r1] = boolToInt(registers_list[r2] > registers_list[r3])
	case "srl":
		registers_list[r1] = registers_list[r2] >> registers_list[r3]
	case "sll":
		registers_list[r1] = registers_list[r2] << registers_list[r3]
	default:
		return registers_list, linenum, Failure{"UnknownInstructionError", "unknown instruction '" + instruction + "'", linenum + rm_lines}
	}

	return registers_list, linenum, nil
}

func Interpreter(code string) {
	registers := make([]int, 32)
	labels := make(map[string]int)

	idx := 0

	lines := strings.Split(strings.ToLower(strings.ReplaceAll(strings.ReplaceAll(code, ", ", " "), ",", " ")), "\n")

	//var instruction_cache []int

	for idx < len(lines) {
		li := strings.TrimSpace(lines[idx])

		if len(li) < 1 {
			idx += 1
			continue
		} else {
			if li[:1] == "#" {
				idx += 1
				continue
			}
		}

		if strings.ContainsAny(li, "#") {
			str := ""
			c_idx := 0
			for li[c_idx] != '#' {
				str += string(li[c_idx])
				c_idx += 1
			}
			li = strings.TrimSpace(str)
		}

		fmt.Println(li)

		l := strings.Split(li, " ")

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
			var err error
			registers, idx, err = callRegister(registers, labels, idx, 0, l[0], l[1], l[2], l[3])
			if err != nil {
				fmt.Println(err.Error())
				return
			}
			idx += 1
		} else if len(l) > 4 {
			fmt.Println(Failure{"SyntaxError", fmt.Sprintf("unneeded argument '%s' argument for instruction '%s'", l[4], l[0]), idx}.Error())
			return
		}
	}

	fmt.Printf("registers: %v; labels: %v", registers, labels)
}
