SYMBOL_TYPES = {
    0: 'NOTYPE',
    1: 'OBJECT',
    2: 'FUNC',
    3: 'SECTION',
    4: 'FILE',
}

SYMBOL_BINDS = {
    0: 'LOCAL',
    1: 'GLOBAL',
    2: 'WEAK',
}

SYMBOL_VISIBILITIES = {
    0: 'DEFAULT',
    1: 'INTERNAL',
    2: 'HIDDEN',
    3: 'PROTECTED',
}

SPECIAL_INDEXES = {
    0: 'UNDEF',
    0xFFF1: 'ABS',
    0xFFF2: 'COMMON',
}

UNKNOWN = 'UNKNOWN'

SYMTAB_ENTRY_SIZE = 16
