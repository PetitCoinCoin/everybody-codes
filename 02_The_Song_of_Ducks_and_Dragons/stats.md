|Quest|Part|Global Rank|Global Score|Global Time|Local Time|
|---|---|---|---|---|---|
|1|I|207|0|5h 34m 29s 469ms|6m 43s 994ms|
|1|II|193|0|5h 36m 20s 675ms|8m 35s 200ms|
|1|III|188|0|5h 40m 14s 050ms|12m 28s 575ms|
|2|I|59|0|11m 33s 106ms|11m 27s 945ms|
|2|II|69|32|49m 32s 892ms|49m 27s 731ms|
|2|III|72|79|55m 45s 836ms|55m 40s 675ms|
|3|I|51|0|4m 11s 764ms|4m 09s 753ms|
|3|II|62|39|7m 58s 374ms|7m 56s 363ms|
|3|III|68|83|14m 18s 017ms|14m 16s 006ms|
|4|I|134|0|24m 38s 533ms|13m 03s 802ms|
|4|II|119|0|27m 01s 441ms|15m 26s 710ms|
|4|III|95|56|33m 10s 394ms|21m 35s 663ms|
|5|I|58|0|12m 54s 046ms|12m 52s 005ms|
|5|II|68|33|21m 14s 581ms|21m 12s 540ms|
|5|III|68|83|45m 10s 342ms|45m 08s 301ms|
|6|I|89|0|5m 26s 839ms|5m 26s 139ms|
|6|II|79|22|7m 09s 517ms|7m 08s 817ms|
|6|III|108|43|56m 40s 404ms|56m 39s 704ms|
|7|I|48|3|6m 56s 870ms|6m 42s 904ms|
|7|II|36|65|8m 10s 526ms|7m 56s 560ms|
|7|III|53|98|28m 32s 749ms|28m 18s 783ms|

Nice start with quest 1! Naive approaches are still enough at this point :sweat_smile:

So I tried this crazy idea for quest 2: go to bed, set an alarm 2min before midnight, and solve the quest with a fuzzy mind :laughing:. Not sure this will work for harder quests (python integer division already gave me a hard time here), but yeay 59/69/72 :tada:.
Then back to bed, and clean up in the morning.
It looks like `namedtuple` are really nice to ease the reading and comprehension, but they are less performant (part 3 runtime gets x2 with used of `namedtuple`). But on EC's Discord I discovered `Pypy` and wow. That's fast!

Q3 was surprinsingly easy. Even if I panicked on part 3, thinking it would be a DP problem. But absolutely not.

Once again, I panicked and over thought way too much Q4P1 until I realized it was simple.

Python negative indexes are really nice until they aren't. I lost so much time on Q6P3. I also had a non-bruteforce approach, but with an off-by-one error, so it didn't work. Luckily I was able to submit the correct solution thanks to bruteforce (which ran in about 5min) and debugged the other way in the morning.

Bruteforce Q7 to get my best result so far. But reworked this as part 3 took between 3 and 4 sec. Using `itertools`' `pairwise` in validity checked already improved significantly. I ended up with some "clever" bruteforce by calculating only what needed to be. It runs in about 350ms which is far from great from what I see on Discord, but already enough for me!
