## Web protocols [2 pts]

Scanning web-protocols.cns-jv.tcc tells us that ports 5009, 5011, 5020, 8011 and 8020 are open.

Trying `curl` (which uses HTTP/1.1) on those:
- 5009 -> unsupported protocol
- 5011 and 8011 -> serves a base64 encoded PNG and `Set-Cookie: SESSION=LXJ2YnEtYWJJ` -> `-rvbq-abI`
- 5020 -> serves similar content and `Set-Cookie: SESSION=Ui00MzNBfQ==` -> `R-433A}`
- 8020 -> `400 Bad request`

Since I didn't find a way to make `curl` use other HTTP versions, I used `netcat` to try them.
Trying port 5009 with `echo "GET / HTTP/0.9" | nc 10.99.0.122 5009` yielded an answer starting with `SESSION=RkxBR3trckx0` -> `FLAG{krLt`

When put together I got the flag `FLAG{krLt-rvbq-abIR-433A}`
