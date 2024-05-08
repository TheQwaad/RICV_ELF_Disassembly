TYPES = {
    0b0110011: 'R',
    0b0000011: 'I',
    0b0010011: 'I',
    0b1100111: 'I',
    0b1110011: 'I',
    0b0001111: 'I',
    0b0100011: 'S',
    0b1100011: 'B',
    0b0010111: 'U',
    0b0110111: 'U',
    0b1101111: 'J',
    0b0101111: 'R'
}

RV32I_INSTRUCTIONS = {
    0x37: {"mnemonic": "lui", "type": "U"},
    0x17: {"mnemonic": "auipc", "type": "U"},
    0x6F: {"mnemonic": "jal", "type": "J"},
    0x67: {"mnemonic": "jalr", "type": "I"},
    0x63: {"mnemonic": "beq", "type": "B"},
    0x1063: {"mnemonic": "bne", "type": "B"},
    0x4063: {"mnemonic": "blt", "type": "B"},
    0x5063: {"mnemonic": "bge", "type": "B"},
    0x6063: {"mnemonic": "bltu", "type": "B"},
    0x7063: {"mnemonic": "bgeu", "type": "B"},
    0x03: {"mnemonic": "lb", "type": "I"},
    0x1003: {"mnemonic": "lh", "type": "I"},
    0x2003: {"mnemonic": "lw", "type": "I"},
    0x4003: {"mnemonic": "lbu", "type": "I"},
    0x5003: {"mnemonic": "lhu", "type": "I"},
    0x23: {"mnemonic": "sb", "type": "S"},
    0x1023: {"mnemonic": "sh", "type": "S"},
    0x2023: {"mnemonic": "sw", "type": "S"},
    0x13: {"mnemonic": "addi", "type": "I"},
    0x2013: {"mnemonic": "slti", "type": "I"},
    0x3013: {"mnemonic": "sltiu", "type": "I"},
    0x4013: {"mnemonic": "xori", "type": "I"},
    0x6013: {"mnemonic": "ori", "type": "I"},
    0x7013: {"mnemonic": "andi", "type": "I"},
    0x1013: {"mnemonic": "slli", "type": "I"},
    0x5013: {"mnemonic": "srli", "type": "I"},
    0x40005013: {"mnemonic": "srai", "type": "I"},
    0x33: {"mnemonic": "add", "type": "R"},
    0x40000033: {"mnemonic": "sub", "type": "R"},
    0x1033: {"mnemonic": "sll", "type": "R"},
    0x2033: {"mnemonic": "slt", "type": "R"},
    0x3033: {"mnemonic": "sltu", "type": "R"},
    0x4033: {"mnemonic": "xor", "type": "R"},
    0x5033: {"mnemonic": "srl", "type": "R"},
    0x40005033: {"mnemonic": "sra", "type": "R"},
    0x6033: {"mnemonic": "or", "type": "R"},
    0x7033: {"mnemonic": "and", "type": "R"},
    0x73: {"mnemonic": "ecall", "type": "I"},
    0x1073: {"mnemonic": "ebreak", "type": "I"},
    0x2073: {"mnemonic": "csrrw", "type": "I"},
    0x3073: {"mnemonic": "csrrs", "type": "I"},
    0x4073: {"mnemonic": "csrrc", "type": "I"},
    0x5073: {"mnemonic": "csrrwi", "type": "I"},
    0x6073: {"mnemonic": "csrrsi", "type": "I"},
    0x7073: {"mnemonic": "csrrci", "type": "I"}
}

RV32M_INSTRUCTIONS = {
    0x02000033: {"mnemonic": "mul", "type": "R"},
    0x02001033: {"mnemonic": "mulh", "type": "R"},
    0x02002033: {"mnemonic": "mulhsu", "type": "R"},
    0x02003033: {"mnemonic": "mulhu", "type": "R"},
    0x02004033: {"mnemonic": "div", "type": "R"},
    0x02005033: {"mnemonic": "divu", "type": "R"},
    0x02006033: {"mnemonic": "rem", "type": "R"},
    0x02007033: {"mnemonic": "remu", "type": "R"}
}

ZIFENCE_INSTRUCTIONS = {
    0x0F: {"mnemonic": "fence", "type": "I"},
    0x100F: {"mnemonic": "fence.i", "type": "I"}
}

ZIHINTPAUSE_INSTRUCTIONS = {
    0x10500073: {"mnemonic": "pause", "type": "I"}
}


INSTRUCTIONS = {**RV32I_INSTRUCTIONS, **RV32M_INSTRUCTIONS, **ZIFENCE_INSTRUCTIONS, **ZIHINTPAUSE_INSTRUCTIONS}

INVALID_INSTRUCTION = {"mnemonic": "invalid_instruction"}

ABI_REGISTER_NAMES = {
    0: "zero",
    1: "ra",
    2: "sp",
    3: "gp",
    4: "tp",
    5: "t0",
    6: "t1",
    7: "t2",
    8: "s0",
    9: "s1",
    10: "a0",
    11: "a1",
    12: "a2",
    13: "a3",
    14: "a4",
    15: "a5",
    16: "a6",
    17: "a7",
    18: "s2",
    19: "s3",
    20: "s4",
    21: "s5",
    22: "s6",
    23: "s7",
    24: "s8",
    25: "s9",
    26: "s10",
    27: "s11",
    28: "t3",
    29: "t4",
    30: "t5",
    31: "t6",
}

UNKNOWN = "UNKNOWN"
