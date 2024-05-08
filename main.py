from elf.parsers import *
import sys


elf_bytes = open(sys.argv[1], 'rb').read()

sections = read_elf_sections(elf_bytes)

symtab = parse_symtab_to_string(sections['.symtab'], sections['.strtab'])
text = parse_text(sections['.text'], sections['.text']['start_address'], sections['.symtab'], sections['.strtab'])

with open(sys.argv[2], "w") as file:
    file.write(text)
    file.write('\n')
    file.write('\n')
    file.write(symtab)
