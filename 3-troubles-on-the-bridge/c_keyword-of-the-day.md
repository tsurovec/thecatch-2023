## Keyword of the day [4 pts]

Nmap scan shows that many of the ports in range 60000-60495 are open. Visiting some of them shows that there's a code that renders a smiley face which changes about every second.

Let's sample them:
`for port in {60000..60495}; do echo "$port"; curl http://keyword-of-the-day.cns-jv.tcc:$port 2>/dev/null > "r_$port"; done`

And see if we can spot some sample that stands out:

`for f in *; do md5sum $f | cut -d' ' -f1; done | sort | uniq -c`

```
     16 082ab1b047faebf85ec75ffd4d1a3bc4
     17 0a6e3e345350b426ce3ceb0f561207ba
     18 22a4513306bd562a1245bedbcc2d7ae7
     13 4e902189742d7852936d7645829a5dd6
     17 52f6fc16b06d7c6d29210f8ae4ba2f66
     16 57ff4399476cc342c2a61c05d69b1eb8
     10 678896fe0c6f55cc64ed56463da82939
     13 6b1bff17c84171b28f96af8688624cea
     11 78f0fbf5d862ed6777fcf828213f40a8
     14 7c3e132d3a12d32ab685bfff405c146f
     13 8e6ef964e949bc34e30f4ef54d1c00e8
     16 ab47f4c0da50a94bdb5e6964888b9206
      1 ba78fb78b670b1b1a4c15e525bc3000b
     18 babcde6f85e67e948776106a2535f7eb
     12 d2567d2d166c2e641756a0714b6a4905
    262 d41d8cd98f00b204e9800998ecf8427e
     14 fb791334b12ea3e630dced1234c9f390
     15 fd2a6d57e8ffac971c286bd564c281a1
```

The response with hash `ba78fb78b670b1b1a4c15e525bc3000b` stands out and it belongs to port 60257. Visiting that and following to http://keyword-of-the-day.cns-jv.tcc:60257/948cd06ca7/ yields the flag.


`FLAG{DEIE-fiOr-pGV5-8MPc}`
