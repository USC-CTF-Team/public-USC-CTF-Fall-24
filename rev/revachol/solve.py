flag_bytes = [0x43, 0x59, 0x42, 0x4F, 0x52, 0x47, 0x7B, 0x0B, 0x0C, 0x11, 0x0A, 0x12, 0x48, 0x44, 0x0F, 0x16, 0x18, 0x1C, 0x28, 0x1C, 0x18, 0x12, 0x2D, 0x0F, 0x1A, 0x08, 0x0F, 0x02]
# Reverse the order of the XOR bytes here because of little-endian order
xor1bytes = 0x00_40_10_13_8D_3C_8A_40
xor2bytes = 0x2E_68_42_3C

def decode(byte):
    byte ^= xor2bytes
    byte ^= xor1bytes
    byte -= 1
    return byte % 0x100
  
print("CYBORG{", end="")
print("".join([chr(decode(b)) for b in flag_bytes[6:]]))