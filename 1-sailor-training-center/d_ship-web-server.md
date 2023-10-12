##  Ship web server 

Points: 1

Visiting http://www.cns-jv.tcc/ redirects us to a https using self-signed certificate.
Checking the certificate in browser, we can see that there are multiple SANs:
	www.cns-jv.tcc
	documentation.cns-jv.tcc
	home.cns-jv.tcc
	pirates.cns-jv.tcc
	structure.cns-jv.tcc

At the bottom of http://www.cns-jv.tcc/ page there's this base64 string `RkxBR3sgICAgLSAgICAtICAgIC0gICAgfQ==` -> `FLAG{    -    -    -    }`

DNS server doesn't resolve any of the other names so I just added them to `/etc/hosts` to resolve to 10.99.0.64 and visited them from browser to gather flag pieces:
https://documentation.cns-jv.tcc/style.css
-> `RkxBR3sgICAgLSAgICAtICAgIC1nTXdjfQ==` = `FLAG{    -    -    -gMwc}`

https://home.cns-jv.tcc/?user=suzan
-> `RkxBR3tlamlpLSAgICAtICAgIC0gICAgfQ==` = `FLAG{ejii-    -    -    }`

https://pirates.cns-jv.tcc/
-> `RkxBR3sgICAgLSAgICAtUTUzQy0gICAgfQ==` = `FLAG{    -    -Q53C-    }`

https://structure.cns-jv.tcc/
-> `RkxBR3sgICAgLXBsbVEtICAgIC0gICAgfQ==` = `FLAG{    -plmQ-    -    }`


Put together: `FLAG{ejii-plmQ-Q53C-gMwc}`
