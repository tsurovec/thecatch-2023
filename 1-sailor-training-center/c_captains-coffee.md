## Captain's coffee [1 pt]

Coffee maker API is at http://coffee-maker.cns-jv.tcc/

curl to it tells us to see `/docs` and that in turn leads to `/openapi.json`.
There are 2 paths of interest:
- `/coffeeMenu` with _GET_
- `/makeCoffee` with _POST_ `drink_id`

`curl http://coffee-maker.cns-jv.tcc/coffeeMenu` -> Naval Espresso With Rum has ID 501176144
`curl -v -XPOST http://coffee-maker.cns-jv.tcc/makeCoffee/ --data '{"drink_id": 501176144}' -H 'content-type: application/json'` -> `{"message":"Your Naval Espresso with rum is ready for pickup","validation_code":"Use this validation code FLAG{ccLH-dsaz-4kFA-P7GC}"}`


`FLAG{ccLH-dsaz-4kFA-P7GC}`
