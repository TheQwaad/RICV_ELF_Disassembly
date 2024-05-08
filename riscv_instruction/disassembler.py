from riscv_instruction.decoders import *
from riscv_instruction.getters import *


def get_mnemonic(opcode, funct3=0, funct7=0):
    return INSTRUCTIONS.get(opcode | (funct7 << 25) | (funct3 << 12), INVALID_INSTRUCTION)['mnemonic']


def format_reg(reg_id):
    return get_abi_reg_name(reg_id)


def handle_fence(instruction):
    beb = "iorw"
    pred = bin(instruction)[2:6]
    succ = bin(instruction)[6:10]
    pred_res, succ_res = ("".join(beb[i] for i in range(4) if pred[i] == '1'),
                          "".join(beb[i] for i in range(4) if succ[i] == '1'))
    return 'fence', pred_res or "none", succ_res or "none"


def handle_branch(instruction, addr, labels, label_references, base_len, opcode):
    imm, funct3, rs1, rs2 = decode_b_instruction(instruction)
    target_addr = addr + imm
    label = labels.setdefault(target_addr, f"L{len(labels) - base_len}")
    label_references[addr] = label
    return get_mnemonic(opcode, funct3), get_abi_reg_name(rs1), format_reg(rs2), get_hex(target_addr), f"<{label}>"


def handle_jump_and_link(mnemonic, rd, addr, imm, labels, label_references, base_len):
    target_addr = addr + imm
    label = labels.setdefault(target_addr, f"L{len(labels) - base_len}")
    label_references[addr] = label
    return mnemonic, get_abi_reg_name(rd), get_hex(target_addr), f"<{label}>"


def disassemble_instruction(instruction, addr, labels, label_references, base_len):
    opcode = instruction & 0b1111111
    instr_type = TYPES[opcode]

    if instr_type == "R":
        rd, funct3, rs1, rs2, funct7 = decode_r_instruction(instruction)
        mnemonic = get_mnemonic(opcode, funct3, funct7)
        return mnemonic, format_reg(rd), format_reg(rs1), format_reg(rs2)

    elif instr_type == "I":
        rd, funct3, funct7, rs1, imm = decode_i_instruction(instruction)
        mnemonic = get_mnemonic(opcode, funct3)
        if mnemonic == 'srli':
            mnemonic = get_mnemonic((funct7 << 25) | opcode | (funct3 << 12))
        rd, rs1 = format_reg(rd), format_reg(rs1)

        if mnemonic in ["jalr", "lb", "lbu", "lh", "lhu", "lw"]:
            return mnemonic, rd, f'{imm}({rs1})'
        elif mnemonic in ["ecall", "fence.i"]:
            return mnemonic,
        elif mnemonic == "fence":
            return handle_fence(instruction)
        return mnemonic, rd, rs1, imm

    elif instr_type == "S":
        imm, funct3, rs1, rs2 = decode_s_instruction(instruction)
        mnemonic = get_mnemonic(opcode, funct3)
        return mnemonic, format_reg(rs2), f"{imm}({format_reg(rs1)})"

    elif instr_type == "B":
        return handle_branch(instruction, addr, labels, label_references, base_len, opcode)

    elif instr_type == "U":
        rd, imm = decode_u_instruction(instruction)
        mnemonic = INSTRUCTIONS.get(opcode, INVALID_INSTRUCTION)['mnemonic']
        return mnemonic, format_reg(rd), hex(imm)

    elif instr_type == "J":
        rd, imm = decode_j_instruction(instruction)
        mnemonic = INSTRUCTIONS.get(opcode, INVALID_INSTRUCTION)['mnemonic']
        return handle_jump_and_link(mnemonic, rd, addr, imm, labels, label_references, base_len)

    return UNKNOWN


