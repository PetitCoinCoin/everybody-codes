|Quest|Part|Global Rank|Global Time|Local Time|
|---|---|---|---|---|
|1|I|41|9h 31m 15s 186ms|2h 22m 34s 372ms|
|1|II|39|9h 42m 57s 140ms|2h 34m 16s 326ms|
|1|III|33|10h 05m 26s 734ms|2h 56m 45s 920ms|
|2|I|37|6h 18m 51s 115ms|3m 20s 308ms|
|2|II|34|6h 42m 16s 573ms|26m 45s 766ms|
|2|III|30|8h 47m 02s 377ms|2h 31m 31s 570ms|

For Q1P3, I thought "6 among 20 is only 38 760 possibilities, this shouldn't take to long!". But I forgot the permutations too XD. Nevertheless, I didn't have time to find a clever solution now (it appears I'm supposed to work), so let's go bruteforcing and let it run... but it completed in about 90sec!

Of course Q2P3 wouldn't be possible with bruteforce! Thought of linked list, but it seemed worst than my naive approach. I thought of recursion (but this made no sense). And I remembered about deque. Since it's based on linked list I assume my first implementation wasn't right. Anyway, it runs in about 10sec. It could probably be improved.
I kept my solution for part 2 for archive purpose, but of course it could be replaced (using the deque solution reduce about 30% runtime)
