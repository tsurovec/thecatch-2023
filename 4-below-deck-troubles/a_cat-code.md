## Cat code [3 pts]

Looking at the entry point, the code only accepts "kittens" word. Then it sums up ASCII values for all letters which is 770 and passes it to the `meow` function.
What `meow` function does is that it recursively computes Fibonacci number for its output. The result is then passed to the `meowmeow` function which decodes the `meeow` list of digit coordinates to put together ASCII values for flag letters.
The quickest way to the flag is just look up the 770th Fibonacci number (e.g. https://oeis.org/A000045/b000045.txt) and plug it directly to the `meowmeow` function: -> `FLAG{YcbS-IAbQ-KHRE-BTNR}`
