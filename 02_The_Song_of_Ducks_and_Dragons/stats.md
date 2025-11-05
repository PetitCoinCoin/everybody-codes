|Quest|Part|Global Rank|Global Score|Global Time|Local Time|
|---|---|---|---|---|---|
|1|I|207|0|5h 34m 29s 469ms|6m 43s 994ms|
|1|II|193|0|5h 36m 20s 675ms|8m 35s 200ms|
|1|III|188|0|5h 40m 14s 050ms|12m 28s 575ms|
|2|I|59|0|11m 33s 106ms|11m 27s 945ms|
|2|II|69|32|49m 32s 892ms|49m 27s 731ms|
|2|III|72|79|55m 45s 836ms|55m 40s 675ms|

Nice start with quest 1! Naive approaches are still enough at this point :sweat_smile:

So I tried this crazy idea for quest 2: go to bed, set an alarm 2min before midnight, and solve the quest with a fuzzy mind :laughing:. Not sure this will work for harder quests (python integer division already gave me a hard time here), but yeay 59/69/72 :tada:.
Then back to bed, and clean up in the morning.
It looks like `namedtuple` are really nice to ease the reading and comprehension, but they are less performant (part 3 runtime gets x2 with used of `namedtuple`). But on EC's Discord I discovered `Pypy` and wow. That's fast!
