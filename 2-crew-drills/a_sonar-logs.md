## Sonar logs 

Points: 2

Looking at the sonar log, the messages consist of a) timestamp in various timezones and b) message.
Some messages conspicuously seem to contain a hex encoded letter (<em>Object detected in depth ...</em>). Greping the file tells us that there are exactly 25 such lines which matches with the number of characters in a FLAG{...} string. So the goal seems to be order these lines in chronologic order and read out the flag.

`grep 'Object detected' sonar.log > input.txt`

It seemed that manually adjusting 25 timetamps will be faster than an automated approach so I did that and got flag in unexpected form `FLAG{3YAG-2rb-KWoZ-LwWmj}` which was indeed incorrect.
I double checked the adjustments and then went for automated solution in Python only to get the same result -_-

By then there was a new hint telling to use pytz library version 2020.4 appeared which indeed solved the issue: `FLAG{3YAG-2rbj-KWoZ-LwWm}`

The problematic value was from America/Mazatlan which is GMT-7 as of 2023. Mexico abolished DST in 2022 and previously Mazatlan probably had GMT-6 on Oct 2.
