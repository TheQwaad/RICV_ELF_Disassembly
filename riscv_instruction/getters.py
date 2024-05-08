from riscv_instruction.values import *


def get_abi_reg_name(reg_number):
    return ABI_REGISTER_NAMES.get(reg_number, f"x{reg_number}")


def get_hex(addr):
    return hex(addr)
