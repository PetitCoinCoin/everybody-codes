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
|8|I|54|0|3m 53s 641ms|3m 52s 436ms|
|8|II|96|5|32m 17s 593ms|32m 16s 388ms|
|8|III|82|69|49m 41s 279ms|49m 40s 074ms|
|9|I|108|0|14m 37s 958ms|14m 37s 242ms|
|9|II|137|0|1h 23m 02s 049ms|1h 23m 01s 333ms|
|9|III|198|0|9h 36m 49s 494ms|9h 36m 48s 778ms|
|10|I|64|0|15m 21s 121ms|15m 20s 457ms|
|10|II|88|13|1h 08m 39s 510ms|1h 08m 38s 846ms|
|10|III|110|41|11h 01m 40s 554ms|11h 01m 39s 890ms|
|11|I|192|0|6h 08m 15s 523ms|20m 29s 349ms|
|11|II|183|0|6h 10m 36s 634ms|22m 50s 460ms|
|11|III|152|0|8h 34m 31s 175ms|2h 46m 45s 001ms|
|12|I|180|0|5h 52m 41s 984ms|10m 59s 450ms|
|12|II|176|0|5h 55m 43s 131ms|14m 00s 597ms|
|12|III|153|0|6h 08m 50s 898ms|27m 08s 364ms|
|13|I|186|0|6h 38m 51s 592ms|5m 16s 566ms|
|13|II|180|0|6h 43m 47s 418ms|10m 12s 392ms|
|13|III|174|0|6h 49m 18s 301ms|15m 43s 275ms|
|14|I|85|0|18m 41s 257ms|18m 40s 162ms|
|14|II|83|18|19m 33s 521ms|19m 32s 426ms|
|14|III|63|88|58m 11s 123ms|58m 10s 028ms|
|15|I|46|5|20m 18s 191ms|20m 17s 557ms|
|15|II|37|64|21m 10s 483ms|21m 09s 849ms|
|15|III|149|2|23h 15m 01s 805ms|23h 15m 01s 171ms|
|16|I|34|17|2m 53s 846ms|2m 53s 210ms|
|16|II|49|52|13m 39s 889ms|13m 39s 253ms|
|16|III|48|103|38m 22s 048ms|38m 21s 412ms|

Nice start with quest 1! Naive approaches are still enough at this point :sweat_smile:

So I tried this crazy idea for quest 2: go to bed, set an alarm 2min before midnight, and solve the quest with a fuzzy mind :laughing:. Not sure this will work for harder quests (python integer division already gave me a hard time here), but yeay 59/69/72 :tada:.
Then back to bed, and clean up in the morning.
It looks like `namedtuple` are really nice to ease the reading and comprehension, but they are less performant (part 3 runtime gets x2 with used of `namedtuple`). But on EC's Discord I discovered `Pypy` and wow. That's fast!

Q3 was surprinsingly easy. Even if I panicked on part 3, thinking it would be a DP problem. But absolutely not.

Once again, I panicked and over thought way too much Q4P1 until I realized it was simple.

Python negative indexes are really nice until they aren't. I lost so much time on Q6P3. I also had a non-bruteforce approach, but with an off-by-one error, so it didn't work. Luckily I was able to submit the correct solution thanks to bruteforce (which ran in about 5min) and debugged the other way in the morning.

Bruteforce Q7 to get my best result so far. But reworked this as part 3 took between 3 and 4 sec. Using `itertools`' `pairwise` in validity checked already improved significantly. I ended up with some "clever" bruteforce by calculating only what needed to be. It runs in about 350ms which is far from great from what I see on Discord, but already enough for me!

I'm disappointed with Q8 as P3 runs in 15sec (first implem was 40sec, but doing it "the python way" improved a lot). I would want to rework this and find the clever way, but let's be honest, I won't.

I overthought Q9 and how to find who is a child of who. Simple bruteforce seemed to be the way. And then, even though I do like for/else structure, it gets messy at 2AM. I had to debug this in the morning. Also, pypy to the request (3.5sec for part 3 instead of 35sec with python). But most of it is identifying children and parents.

Q10 was the last day I woke up during the night to start at release time. It now takes too long to solve (even more with a fuzzy brain).
For P3, I tried BFS, DFS... ended taking a look at some hint and ended with DP (which is a nice exercise for me as I still struggle with this). P3 runs in ~40sec (but 4-5 minutes with pypy !)

Q11 was fun, especially P3. I knew it would run for hours if I didn't find the trick. Anyway, P2 is now the slowest part, with ~10sec (python) and ~0.5sec (pypy) runtimes. Also, 152nd for P3... so close to getting a point even if being late to the party :smiling_face_with_tear:

Surprised by Q12, which was relatively easy (especially  after Q10 !). Anyway P3 is not optimal, but it works in a reasonnable amount of time, so that's enough. And again, so close to getting a point (153rd !)

Q13 was also surprinsingly easy. P3 could probably be optimized (runs in ~8sec). But I prefered to refactor the code in order to use exactly the same code for all 3 parts.

I like when it's not just code, but also analyzing the input. Q14P3 was fun in that way!

Q15 was epic! My best time for P1, second best for P2. It took me a whole day (literally) to get p3, and I still got 2 tiny points! Also, I discovered `operators` library and it is a nice discovery to handle operators and avoid big if/else structure.

So happy with Q16. Fast solving, fast runtime!
