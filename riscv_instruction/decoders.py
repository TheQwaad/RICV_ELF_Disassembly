def sign_extend(imm, bits):
    if (imm >> (bits - 1)) & 1:
        return imm | ((-1) << bits)
    else:
        return imm


def extract_fields(instruction, *field_specs):
    values = []
    for (shift, mask) in field_specs:
        value = (instruction >> shift) & mask
        values.append(value)
    return values


def decode_r_instruction(instruction):
    rd, funct3, rs1, rs2, funct7 = extract_fields(
        instruction,
        (7, 0x1F), (12, 0x7), (15, 0x1F), (20, 0x1F), (25, 0x7F)
    )
    return rd, funct3, rs1, rs2, funct7


def decode_i_instruction(instruction):
    rd, funct3, rs1, imm = extract_fields(
        instruction,
        (7, 0x1F), (12, 0x7), (15, 0x1F), (20, 0xFFF)
    )
    imm = sign_extend(imm, 12)
    funct7 = (instruction >> 25) & 0x7F
    return rd, funct3, funct7, rs1, imm


def decode_s_instruction(instruction):
    imm_4_0, funct3, rs1, rs2, imm_11_5 = extract_fields(
        instruction,
        (7, 0x1F), (12, 0x7), (15, 0x1F), (20, 0x1F), (25, 0x7F)
    )
    imm = (imm_11_5 << 5) | imm_4_0
    imm = sign_extend(imm, 12)
    return imm, funct3, rs1, rs2


def decode_b_instruction(instruction):
    imm_11, imm_4_1, funct3, rs1, rs2, imm_10_5, imm_12 = extract_fields(
        instruction,
        (7, 0x1), (8, 0xF), (12, 0x7), (15, 0x1F), (20, 0x1F), (25, 0x3F), (31, 0x1)
    )
    imm = (imm_12 << 12) | (imm_11 << 11) | (imm_10_5 << 5) | (imm_4_1 << 1)
    imm = sign_extend(imm, 13)
    return imm, funct3, rs1, rs2


def decode_u_instruction(instruction):
    rd, imm = extract_fields(
        instruction,
        (7, 0x1F), (12, 0xFFFFF)
    )
    imm = sign_extend(imm, 20)
    return rd, imm


def decode_j_instruction(instruction):
    rd, imm_19_12, imm_11, imm_10_1, imm_20 = extract_fields(
        instruction,
        (7, 0x1F), (12, 0xFF), (20, 0x1), (21, 0x3FF), (31, 0x1)
    )
    imm = (imm_20 << 20) | (imm_19_12 << 12) | (imm_11 << 11) | (imm_10_1 << 1)
    imm = sign_extend(imm, 21)
    return rd, imm
