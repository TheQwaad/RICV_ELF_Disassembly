import struct
from riscv_instruction.disassembler import *
from elf.getters import *
from elf.values import *


def unpack_from(offset, elf_bytes, fmt):
    return struct.unpack_from(fmt, elf_bytes, offset)[0]


def read_null_terminated_string(bytes, offset):
    end = bytes.find(b'\x00', offset)
    return bytes[offset:end]


def get_string_from_strtab(index, strtab):
    end = strtab.find(b'\x00', index)
    return strtab[index:end].decode('utf-8')


def read_elf_sections(elf_bytes):
    sections = {'text': None, 'strtab': None, 'symtab': None}
    e_shoff = unpack_from(32, elf_bytes, '<I')
    e_shentsize = unpack_from(46, elf_bytes, '<H')
    e_shnum = unpack_from(48, elf_bytes, '<H')
    e_shstrndx = unpack_from(50, elf_bytes, '<H')
    shstrtab_header_offset = e_shoff + e_shstrndx * e_shentsize
    shstrtab_offset = unpack_from(shstrtab_header_offset + 16, elf_bytes, '<I')
    shstrtab_size = unpack_from(shstrtab_header_offset + 20, elf_bytes, '<I')
    shstrtab = elf_bytes[shstrtab_offset:shstrtab_offset + shstrtab_size]

    for i in range(e_shnum):
        section_offset = e_shoff + i * e_shentsize
        section_name_offset = unpack_from(section_offset, elf_bytes, '<I')
        section_name = read_null_terminated_string(shstrtab, section_name_offset).decode('utf-8')
        section_type = unpack_from(section_offset + 4, elf_bytes, '<I')
        if section_name in ['.strtab', '.symtab', '.text']:
            data_offset = unpack_from(section_offset + 16, elf_bytes, '<I')
            data_size = unpack_from(section_offset + 20, elf_bytes, '<I')
            section_data = elf_bytes[data_offset:data_offset + data_size]
            if section_name == '.text':
                start_address = unpack_from(section_offset + 12, elf_bytes, '<I')
                sections[section_name] = {'data': section_data, 'start_address': start_address}
            else:
                sections[section_name] = section_data

    return sections


def parse_symtab_to_string(symtab, strtab):
    res = ".symtab\n"
    res += "\nSymbol Value              Size Type     Bind     Vis       Index Name\n"

    for i in range(0, len(symtab), SYMTAB_ENTRY_SIZE):
        if i + SYMTAB_ENTRY_SIZE > len(symtab):
            break

        entry = symtab[i:i + SYMTAB_ENTRY_SIZE]
        st_name, st_value, st_size, st_info, st_other, st_shndx = struct.unpack('<IIIBBH', entry)
        name = get_string_from_strtab(st_name, strtab)
        symbol_type = get_symbol_type(st_info & 0xf)
        symbol_bind = get_symbol_bind((st_info >> 4) & 0xf)
        symbol_vis = get_symbol_visibility(st_other)
        symbol_index = get_symbol_index(st_shndx)

        res += "[%4i] 0x%-15X %5i %-8s %-8s %-8s %6s %s\n" % (i // SYMTAB_ENTRY_SIZE, st_value, st_size, symbol_type,
                                                              symbol_bind, symbol_vis, symbol_index, name)

    return res


def parse_symtab(symtab, strtab):
    symbols = {}
    for i in range(0, len(symtab), SYMTAB_ENTRY_SIZE):
        entry = symtab[i:i + SYMTAB_ENTRY_SIZE]
        st_name, st_value, st_size, st_info, st_other, st_shndx = struct.unpack('<IIIBBH', entry)
        name = get_string_from_strtab(st_name, strtab)
        symbols[st_value] = name
    return symbols


def format_instruction(disassm, addr, instruction):
    if len(disassm) == 1:
        return f"   {addr:05x}:\t{instruction:08x}\t{disassm[0]}\n"
    args = ", ".join(disassm[1:])
    return f"   {addr:05x}:\t{instruction:08x}\t{disassm[0]:7s}\t{args}\n"


def format_text_section(instructions, labels):
    res = ".text\n"
    for disassm, addr, instruction in instructions:
        label = labels.get(addr, "")
        if label:
            res += f"\n{addr:08x} \t<{label}>:\n"
        disassm = [str(item) for item in disassm]
        formatted_instruction = format_instruction(disassm, addr, instruction)
        res += formatted_instruction

    return res


def parse_text(text_section, text_start_address, symtab, strtab):
    labels = parse_symtab(symtab, strtab)
    instructions = []

    for i in range(0, len(text_section['data']), 4):
        addr = text_start_address + i
        instruction = struct.unpack_from('<I', text_section['data'], i)[0]
        disassembled = disassemble_instruction(instruction, addr, labels, {}, len(labels))
        if "invalid_instruction" in disassembled:
            disassembled = ("invalid_instruction",)
        instructions.append((disassembled, addr, instruction))

    return format_text_section(instructions, labels)
