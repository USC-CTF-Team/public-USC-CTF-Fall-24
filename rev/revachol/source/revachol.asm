    
section .text
global _start
global kim

_start:
    ; Store the first byte of the _start subroutine in rdi
    mov rcx, 0
    cmp cl, byte 27
    jg kim
    mov dil, [_start+0x13+rcx*4]
    mov dl, byte 0x43     ; [0] 43h 'C'
    add rax, 0x12345987   ; [1] 59h 'Y'
    cmp al, byte 0x42     ; [2] 42h 'B'
    push 0x4f3d2e         ; [3] 4f  'O'
    add ax, 0xfa52       ; [4] 52  'R'
    cmp ax, 0x0847       ; [5] 47  'G'
    sub al, byte 1
    jnp short 1          ; [6] 7b  '{'
    cmp ax, 0x710b       ; [7] 0b 'v' -- encoded from here out
    add ax, 0xe70c       ; [8] 0c 'o'
    add ax, 0xb011       ; [9] 11 'l'
    cmp ax, 0x010a       ; [10] 0a 'u'
    sub ax, 0xfa12       ; [11] 12 'm'
    add ax, 0x8048       ; [12] 48 '3'
    add ax, 0x4444       ; [13] 44 '7'
    cmp ax, 0xd00f       ; [14] 0f 'r'
    add bl, 0x16       ; [15] 16 'i'
    clc
    sub ax, 0xb318       ; [16] 18 'c'
    mov ax, 0x201c       ; [17] 1c '_'
    and ax, 0xce28       ; [18] 28 'S'
    or ax, 0xc91c       ; [19] 1c '_'
    xor ax, 0x1618       ; [20] 18 'c'
    sub ax, 0xd112       ; [21] 12 'm'
    and ax, 0xa42d       ; [22] 2d 'P'
    and ax, 0x7a0f       ; [23] 0f 'r'
    or ax, 0xa01a       ; [24] 1a 'e'
    sub ax, 0x0808       ; [25] 08 's'
    add ax, 0xbb0f       ; [26] 0f 'r'
    add ax, 0x2002       ; [27] 02 '}'
kim:
    ; Exit with status code
    mov rax, 60
    syscall

encrypt:
    ; Parameters: 
    ; rdi = input character to decode 
    add edi, 0x00000001
    xor rdi, [_start+0xA]
    xor edi, [_start+0x1A]
    ret
    
;decrypt:
;    xor rdi, [_start+0xA]
;    xor edi, [_start+0x1A]
;    sub edi, 0x00000001
;    ret
    
