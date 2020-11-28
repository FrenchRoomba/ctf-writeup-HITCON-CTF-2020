# Welcome
_Category: reverse_

## Description
> It's a reverse challenge.
> 
> `ssh welcome@18.176.232.130`
> 
> password: hitconctf

## Solution
1. SSH into the target with the password `hitconctf`
```
ssh welcome@18.176.232.130
```
2. Type everyone's favourite comfort command `ls` and admire the cute ACSII [steam locomotive](https://github.com/mtoyoda/sl) normally associated with `sl`:
```
                      (@@) (  ) (@)  ( )  @@    ()    @     O     @     O      @
                 (   )
             (@@@@)
          (    )
        (@@@)
      ====        ________                ___________
  _D _|  |_______/        \__I_I_____===__|_________|
   |(_)---  |   H\________/ |   |        =|___ ___|      _________________
   /     |  |   H  |  |     |   |         ||_| |_||     _|                \_____A
  |      |  |   H  |__--------------------| [___] |   =|                        |
  | ________|___H__/__|_____/[][]~\_______|       |   -|                        |
  |/ |   |-----------I_____I [][] []  D   |=======|____|________________________|_
__/ =| o |=-~~\  /~~\  /~~\  /~~\ ____Y___________|__|__________________________|_
 |/-=|___|=    ||    ||    ||    |_____/~\___/          |_D__D__D_|  |_D__D__D_|
  \_/      \_O=====O=====O=====O/      \_/               \_/   \_/    \_/   \_/
```
3. "Reverse" `ls` as `sl`
```bash
$ sl
flag
```
4. Ah, the flag is in the file `flag`. Read it with `cat` (backwards, obviously):
```
$ tac galf
hitcon{!0202 ftcnoctih ot emoclew}
$ Connection to 18.176.232.130 closed.
```