from elf.values import *


def get_symbol_type(st_info):
    return SYMBOL_TYPES.get(st_info, UNKNOWN)


def get_symbol_bind(st_info):
    return SYMBOL_BINDS.get(st_info, UNKNOWN)


def get_symbol_visibility(st_other):
    return SYMBOL_VISIBILITIES.get(st_other, UNKNOWN)


def get_symbol_index(st_shndx):
    return SPECIAL_INDEXES.get(st_shndx, str(st_shndx))
