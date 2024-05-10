from random import randint
import os



OPCODES = {
    'sep':                 0,
    'addi':                1,
    'andi':                2,
    'ori':                 3,
    'xori':                4,
    'slti':                5,
    'srli':                6,
    'slli':                7,
    'add':                 8,
    'sub':                 9,
    'and':                 10,
    'or':                  11,
    'xor':                 12,
    'slt':                 13,
    'srl':                 14,
    'sll':                 15,
    'beq':                 16,
    'bne':                 17,
    'bge':                 18,
    'blt':                 19,

    'label':               20,
    'inside_label':        21,
    'imm':                 22,
    'idx_register_call':   23,
    'nxt_register_call':   24,
    'illegal_instruction': 25
}

OPCODES_REV = {OPCODES[instruct]: instruct for instruct in list(OPCODES)}



TO_ASCII = {chr(i): i for i in range(128)}
FROM_ASCII = {i: chr(i) for i in range(128)}



class failure:
    def __init__(self, error_type: str, details: str = None, line: int = None) -> None:
        self.type = str(error_type)
        self.details = details
        if isinstance(self.details, str): self.details = details.strip()
        if isinstance(self.details, str) and isinstance(line, int): self.details += f' on line {line+1}'
    def __repr__(self) -> str: return f"{self.type}: {self.details}" if self.details else self.type


def verifyregcal(regs: list[int], ln: int, rml: int, regcal: str | int, imm: int):
    invalid = failure("InvalidRegisterCallError", f"invalid register index '{regcal}'", ln+rml)
    if imm == 1 and regcal.isdigit():
        return int(regcal)
    elif imm == 0 and regcal.isdigit():
        return failure("InvalidRegisterCallError", f"invalid register index '{regcal}'(did you try to use a non-immediate instruction as an immediate instruction?)", ln+rml)
    elif imm == 2 and not regcal.isdigit():
        return regcal
    elif regcal.startswith('x'):
        if regcal.removeprefix('x').isdigit():
            if int(regcal.removeprefix('x')) < len(regs):
                return int(regcal.removeprefix('x'))
    elif regcal == 'zero':
        return 0
    elif regcal.startswith('n'):
        check = None
        if regcal == 'n': check = 0
        else:
            if regcal.removeprefix('n').isdigit():
                check = int(regcal.removeprefix('n'))
            else: return invalid
        if check == None: return invalid
        for i, r in enumerate(regs):
            if r == check: return i
        print(f"WARNING FROM LINE {ln+rml+1}: could not find register with value of '{check}', defaulting to x0")
        return 0
    elif regcal == None: return None
    return invalid

def callregister(registers_list: list[int], labels: dict[str, int], linenum: int, rm_lines: int, instruction: str, to: str, first: str, second: str):
    immediate = 0
    if instruction.endswith('i'): immediate = 1
    r1 = verifyregcal(registers_list, linenum, rm_lines, to, immediate)
    r2 = verifyregcal(registers_list, linenum, rm_lines, first, immediate)
    if instruction in ('beq', 'bne', 'bge', 'blt'): immediate = 2
    r3 = verifyregcal(registers_list, linenum, rm_lines, second, immediate)
    if isinstance(r1, failure): return registers_list, linenum, r1
    if isinstance(r2, failure): return registers_list, linenum, r2
    if isinstance(r3, failure): return registers_list, linenum, r3
    #print(instruction, to, first, second, immediate)

    match instruction:
        # immediates
        case 'addi': registers_list[r1] = registers_list[r2] + r3
        #case 'subi': registers_list[r1] = registers_list[r2] - r3
        case 'andi': registers_list[r1] = registers_list[r2] & r3
        case 'ori': registers_list[r1] = registers_list[r2] | r3
        case 'xori': registers_list[r1] = registers_list[r2] ^ r3
        case 'slti': registers_list[r1] = int(registers_list[r2] < r3)
        #case 'sgti': registers_list[r1] = int(registers_list[r2] > r3)
        case 'srli': registers_list[r1] = registers_list[r2] >> r3
        case 'slli': registers_list[r1] = registers_list[r2] << r3

        # non-immediates
        case 'add': registers_list[r1] = registers_list[r2] + registers_list[r3]
        case 'sub': registers_list[r1] = registers_list[r2] - registers_list[r3]
        case 'and': registers_list[r1] = registers_list[r2] & registers_list[r3]
        case 'or': registers_list[r1] = registers_list[r2] | registers_list[r3]
        case 'xor': registers_list[r1] = registers_list[r2] ^ registers_list[r3]
        case 'slt': registers_list[r1] = int(registers_list[r2] < registers_list[r3])
        #case 'sgt': registers_list[r1] = int(registers_list[r2] > registers_list[r3])
        case 'srl': registers_list[r1] = registers_list[r2] >> registers_list[r3]
        case 'sll': registers_list[r1] = registers_list[r2] << registers_list[r3]

        # branches
        case 'beq':
            if registers_list[r1] == registers_list[r2]:
                if isinstance(r3, int): linenum = r3
                else:
                    line = labels.get(r3, None)
                    if line == None: return registers_list, linenum, failure('MissingLabelError', f"label '{r3}' does not exist", linenum+rm_lines)
                    linenum = line
        case 'bne':
            if registers_list[r1] != registers_list[r2]:
                if isinstance(r3, int): linenum = r3
                else:
                    line = labels.get(r3, None)
                    if line == None: return registers_list, linenum, failure('MissingLabelError', f"label '{r3}' does not exist", linenum+rm_lines)
                    linenum = line
        case 'bge':
            if registers_list[r1] >= registers_list[r2]:
                if isinstance(r3, int): linenum = r3
                else:
                    line = labels.get(r3, None)
                    if line == None: return registers_list, linenum, failure('MissingLabelError', f"label '{r3}' does not exist", linenum+rm_lines)
                    linenum = line
        case 'blt':
            if registers_list[r1] < registers_list[r2]:
                if isinstance(r3, int): linenum = r3
                else:
                    line = labels.get(r3, None)
                    if line == None: return registers_list, linenum, failure('MissingLabelError', f"label '{r3}' does not exist", linenum+rm_lines)
                    linenum = line

        case x: return registers_list, linenum, failure('UnknownInstructionError', f"unknown instruction '{instruction}'", linenum+rm_lines)
    
    return registers_list, linenum, None



def cache_instruct(cache: list[int], li: list[str], labels: dict[str, int]):
    ascii_convert = lambda x: [TO_ASCII[y] for y in x]
    if li[0] in list(labels.keys()):
        cache.append(OPCODES['label'])
        cache.extend(cache.extend(ascii_convert(li[0].removesuffix(':'))))
        #cache.append(OPCODES['sep'])
    elif li[0] in ('beq', 'bne', 'bge', 'blt'):
        cache.append(OPCODES.get(li[0], OPCODES['illegal_instruction']))
        #cache.append(OPCODES['sep'])

        if li[1] == 'n': cache.append(OPCODES['nxt_register_call'])
        else: cache.append(OPCODES['idx_register_call']); cache.append(int(li[1].removeprefix('x')))
        #cache.append(OPCODES['sep'])
        
        if li[2] == 'n': cache.append(OPCODES['nxt_register_call'])
        else: cache.append(OPCODES['idx_register_call']); cache.append(int(li[2].removeprefix('x')))
        #cache.append(OPCODES['sep'])

        if li[3].isdigit(): cache.append(OPCODES['imm']); cache.append(int(li[3]))
        else: cache.append(OPCODES['label']); cache.append(ascii_convert(li[3]))
        #cache.append(OPCODES['sep'])
    else:
        imm = False
        if li[0].endswith('i'): imm = True
        cache.append(OPCODES.get(li[0], OPCODES['illegal_instruction']))
        #cache.append(OPCODES['sep'])

        if li[1] == 'n': cache.append(OPCODES['nxt_register_call']); cache.append(0)
        elif li[1].startswith('n') and li[1].removeprefix('n').isdigit(): cache.append(OPCODES['nxt_register_call']); cache.append(int(li[1].removeprefix('n')))
        else: cache.append(OPCODES['idx_register_call']); cache.append(int(li[1].removeprefix('x')))
        #cache.append(OPCODES['sep'])

        if li[2] == 'n': cache.append(OPCODES['nxt_register_call']); cache.append(0)
        elif li[2].startswith('n') and li[2].removeprefix('n').isdigit(): cache.append(OPCODES['nxt_register_call']); cache.append(int(li[2].removeprefix('n')))
        else: cache.append(OPCODES['idx_register_call']); cache.append(int(li[2].removeprefix('x')))
        #cache.append(OPCODES['sep'])

        if imm: cache.append(OPCODES['imm']); cache.append(int(li[3]))
        else:
            if li[3] == 'n': cache.append(OPCODES['nxt_register_call']); cache.append(0)
            elif li[3].startswith('n') and li[3].removeprefix('n').isdigit(): cache.append(OPCODES['nxt_register_call']); cache.append(int(li[3].removeprefix('n')))
            else: cache.append(OPCODES['idx_register_call']); cache.append(int(li[3].removeprefix('x'))) 
        #cache.append(OPCODES['sep'])

    cache.append(OPCODES['sep'])
    return cache



def parser(lines: list[str]):
    remove = [i for i, l in enumerate(lines) if l.startswith('#')]
    remove.reverse()
    for r in remove: del lines[r]
    labels = {}
    ignored = []
    ln = 0
    while ln < len(lines):
        l = lines[ln].replace('zero', 'x0')
        if not l.startswith(('\t', '    ')): l = l.strip()
        if '#' in l: l = l.split('#', 1)[0]
        if l.endswith(':') and not l.startswith(('beq', 'bne', 'bge', 'blt')): labels[l.removesuffix(':')] = ln; ignored.append(ln)
        lines[ln] = l
        ln += 1
    return labels, lines, ignored, len(remove)


def interpreter(code: str, compile_mode: bool = False, savename: str = None):
    registers = [0 for _ in range(32)]
    ln = 0
    lines = code.casefold().replace(', ', ' ').replace(',', ' ').split('\n')
    labels = {}
    ignored_lines = []
    removed_lines = 0
    labels, lines, ignored_lines, removed_lines = parser(lines)

    if compile_mode: instructions_cache = []
    while ln < len(lines):
        #print(ln, lines[ln])
        if ln in ignored_lines:
            if compile_mode: instructions_cache = cache_instruct(instructions_cache, lines[ln].strip().split(' '), labels)
            ln += 1
            while lines[ln].startswith(('\t', '    ')):
                if compile_mode: instructions_cache.append(OPCODES['inside_label']); instructions_cache = cache_instruct(instructions_cache, lines[ln].strip().split(' '), labels)
                ln += 1
        if not lines[ln].isascii():
            print(failure('InvalidCharacterError', f'line {ln+removed_lines} contains non-ASCII characters')); return
        l = lines[ln].strip().split(' ')
        while '' in l: l.remove('')
        if len(l) == 0: ln += 1; continue
        elif len(l) < 4:
            print(failure('SyntaxError', f"not enough arguments for instruction '{l[0]}'", ln+removed_lines)); return
        elif len(l) == 4:
                regs, lnum, err = callregister(registers, labels, ln, removed_lines, l[0], l[1], l[2], l[3])
                if isinstance(err, failure): print(err); return
                registers = regs
                ln = lnum
                ln += 1
                if compile_mode: instructions_cache = cache_instruct(instructions_cache, l, labels)
        elif len(l) > 4:
            print(failure('SyntaxError', f"unneeded argument '{l[4]}' argument for instruction '{l[0]}'", ln+removed_lines)); return
        else:
            print(failure('InterpreterError', f"somehow len(l) is not 4, not < 4, and not > 4, len is instead '{len(l)}';\ncurrent line is '0i{ln+removed_lines}', and content is '{l}'")); return
    
    if not compile_mode: print(f'registers: {registers}; labels: {labels}')
    if compile_mode:
        if instructions_cache[-1] == 0: del instructions_cache[-1]
        #print(instructions_cache)
        path = f'crisp/{savename}.crisp'
        if os.path.exists(path): os.remove(path)
        with open(path, 'xb') as comp_out:
            comp_out.write(bytearray(instructions_cache))



def collect_until_sep(bytes: bytes | bytearray, c_idx: int):
    out = ''
    idx = c_idx + 1
    while idx < len(bytes) and bytes[idx] != 0:
        out += FROM_ASCII.get(bytes[idx], '_')
        idx += 1
    return out, idx


def crisp_decompiler(crisp_bytes: bytes | bytearray):
    out = ''
    idx = 0
    while idx < len(crisp_bytes):
        b = crisp_bytes[idx]
        if b == 0: out += '\n'; idx += 1
        elif b < 20: out += OPCODES_REV[b] + ' '; idx += 1
        elif b < 25:
            op = OPCODES_REV[b]
            match op:
                case 'label':
                    lt, idx = collect_until_sep(crisp_bytes, idx)
                    out += lt + ':'
                case 'inside_label': out += '\t'
                case 'imm': idx += 1; out += f'{crisp_bytes[idx]} '
                case 'idx_register_call': idx += 1; out += f'x{crisp_bytes[idx]} '
                case 'nxt_register_call':
                    idx += 1
                    out += 'n ' if OPCODES_REV[b] == 0 else f'n{OPCODES_REV[b]} '
            idx += 1
        else:
            out += f'{randint(TO_ASCII["A"], TO_ASCII['z']+1)}{randint(TO_ASCII["A"], TO_ASCII['z']+1)}{randint(TO_ASCII["A"], TO_ASCII['z']+1)} x0, x0, x0\n'
            idx += 1
    final = []
    for o in out.split('\n'): o = o.rstrip() if o.startswith('\t') else o.strip(); final.append(o)
    return '\n'.join(final)