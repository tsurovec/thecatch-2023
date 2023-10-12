## Captain’s password 

Points: 2

We're given two files - a Keepass database and a memory dump.

Quick research revelas that it's possible to get Keepass master password from a crash dump:

https://github.com/vdohney/keepass-password-dumper (needs .NET7.0)

`dotnet run ../crashdump.dmp` -> 

```
Password candidates (character positions):
Unknown characters are displayed as "●"
1.:     ●
2.:     ), ÿ, a, :, |, í, W, 5, , r, ¸, 
3.:     s, 
4.:     s, 
5.:     w, 
6.:     o, 
7.:     r, 
8.:     d, 
9.:     4, 
10.:    m, 
11.:    y, 
12.:    p, 
13.:    r, 
14.:    e, 
15.:    c, 
16.:    i, 
17.:    o, 
18.:    u, 
19.:    s, 
20.:    s, 
21.:    h, 
22.:    i, 
23.:    p, 
Combined: ●{), ÿ, a, :, |, í, W, 5, , r, ¸}ssword4mypreciousship
```

We have to guess the first 2 letters but it's pretty easy guess here. `password4mypreciousship` is the master password for the Keepass database the flag is stored in <em>Inernal ship systems -> Main Flag System</em>

`FLAG{pyeB-941A-bhGx-g3RI}`

(todo more about keepass vulnerable ver)