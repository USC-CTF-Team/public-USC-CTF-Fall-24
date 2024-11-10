from periodictable import elements
import re

ciphertext = open("message.txt").read().strip()
elems = re.split("([A-Z][a-z]*)", ciphertext) # split element abbreviations string into list
atomic_numbers = []
for el in elems:
    try:
        atomic_numbers.append(getattr(elements, el).number) # get the atomic number of an element
    except AttributeError:
        pass
ascii_list = list(map(chr, atomic_numbers)) # atomic number -> ASCII char
hex_list = [i+j for i,j in zip(ascii_list[::2], ascii_list[1::2])] # the ASCII chars are two digit hex numbers
flag = "".join(map(lambda x: chr(int(x, 16)), hex_list)) # hex ints -> ASCII
print(flag)
