# Tenet
_Category: misc, reverse_

## Description
> You have to start looking at the world in a new way.
> 
> `nc 52.192.42.215 9427`
> [tenet-1050118538f6f01c2ad0049587dc0828e8a4f132e539e110f0cb04a8c17b78bf.tar.gz](tenet-1050118538f6f01c2ad0049587dc0828e8a4f132e539e110f0cb04a8c17b78bf.tar.gz)

## Short Solution

We need to provide the server shellcode that when run fowards, zeros out some memory containing a secret cookie, and restores the secret cookie when run backwards.
This can be achieved by smuggling the secret cookie within the AVX2 YMM register, which is not cleared between the program running.

## Solution

The archive we are given contains `server.rb` and `timemachine`. We need to understand these before we can begin solving the challenge.

### server.rb

When run, the server code asks for the length of your shellcode, then the shellcode itself. This shellcode is added to some hard-coded ELF content to produce an executable file.
The program that is created is then passed to the `timemachine`.
For the purposes of the challenge, the specifics of the rest of the script aren't relevant, and we didn't spend any time figuring them out (beyond the path to the file the script sends to the timemachine, so that we could verify it was working as intended).

### timemachine

The timemachine is more complicated. Conceptually, it forks to run your program/shellcode and attaches to the process with ptrace. Before the program is run, a secret cookie is injected into the childs memory with ptrace.
The timemachine then runs your code, one step at a time. At each step, a check is performed to see whether the next instruction is the `exit` syscall. If so, the child exists this main loop. Otherwise, the child continues performing instructions step by step, until the maximum number of steps (`0xFFF`), at which point the child is killed with an error.
During this main loop, each step results in the `rip` register (the instruction pointer, or program counter) being saved to an array.

Once the child successfully exists the main loop (by using the `exit` syscall), the timemachine verifies whether the secret cookie has been zeroed out of memory. If it has not, an error is produced and execution halts.

The child now has it's registers reset with the ptrace calls `PTRACE_SETREGS` and `PTRACE_SETFPREGS`, with all registers being set to 0.

The timemachine now sets `rip` in the child to the previously executed instruction (as recorded in the `rip` array during the forwards execution), then executes a single step. This continues in a loop until all `rip` values have been executed.

The childs memory is now inspected to verify that the secret cookie is back in the memory where it was first stored.

### Our shellcode

Now we understand what the program does, we can think of some ways to achieve what we need.

Our first thought was to smuggle the value in a memory location not checked by the timemachine, however no such memory exists. While the obvious choice would be the stack itself (since we never need to call a function in our own shellcode), the timemachine prevents us writing any stack values before our shellcode begins.

The solution we ended up trying that worked was to smuggle the value in the registers themselves. While there is a call to clear both the normal registers and floating point registers by the time machine, the ptrace API is such that only 128bits of the AVX registers can be set. This means if we can store a secret in the upper 128bits, it won't be cleared by ptrace. This seems to be a limitation of ptrace itsef.

### Our shellcode: Hacking Edition

Using all our hard-earned reversing knowledge, we can put together the following instructions that will smuggle our value appropriately:
```asm
# Move the secret value into the xmm1 register
movq xmm1, [0x2170000]
# Permute the ymm1 register such that the lower value (xmm1) is moved into the high bits too
VPERM2F128 ymm1, ymm1, ymm1, 0

# Erase the secret from memory when forwards, store the secret into memory when backwards
xor rax, rax
mov [0x2170000], rax

# Move the value from the xmm1 register into rax
movq rax, xmm1
# Permute the ymm1 register such that the higher value is stored into the lower bits
# When forward, this is the secret, and when backwards, this is still the secret, as it's never cleared
VPERM2F128 ymm1, ymm1, ymm1, 1

# Call exit() syscall
mov rax, 60
syscall
```

The script we used to automate creation of this exploit, as well as for testing, is the aptly named [hack.py](hack.py).


