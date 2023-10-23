## Signal flags [5 pts]

There are 90 images with different ships showing messages in naval alphabet. Instead of developing an automated solution I used the good old hard work - just went through the images and stored the information in database.

Then I groupped the transmissions by ship, ordered by time, concatenated the messages  starting with `0x` and decoded. The flag comes from the Finnish ship:

```
sqlite3 signalizations.sqlite "select signal_content from signalizations where ship_affiliation='FIN' order by timestamp_gmt;" \
| sed -n 's/0x\(.*\)/\1/p' | tr -d '\n' \
| python3 -c "print(bytes.fromhex(input()).decode('utf-8'))"
```
->
`CNS Josef , are your nets ok, too? ;-)CNS J, you can  them by RkxBR3tsVHJHLTNvWG4tYW9aTi1aNHFNfQ== !osef`


`FLAG{lTrG-3oXn-aoZN-Z4qM}`
