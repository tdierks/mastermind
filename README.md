mastermind
==========

A simple python program for solving Mastermind (probably a registered trademark of
someone or other, used without permission, no endorsement expressed or implied).

Results for trying to solve all possible patterns:

Naive "first" chooser (each turn, choose the lexicographically first pattern that's possibly correct):
```
Rounds: Trials
1     : 1
2     : 4
3     : 25
4     : 108
5     : 305
6     : 602
7     : 196
8     : 49
9     : 6
```
(That is, for 49 of the 1,296 possible patterns, it got the answer in 8 tries). Average: 5.76

With a chooser that picks a random possibly-correct answer at each round, it rarely takes more than 7 tries: thus, the lexicographic simplicity of the "first" solver is an unnecessary impediment.

A simple mod that has the chooser prefer possible answers with more colors gives:
```
Rounds: Trials
1     : 1
2     : 13
3     : 101
4     : 406
5     : 521
6     : 215
7     : 39
```
Average: 4.72

With a choosing algorithm that attempts to choose an answer which might be correct, but selects the one which will yield the most info if it is not:
```
Rounds: Trials
1     : 1
2     : 12
3     : 99
4     : 468
5     : 662
6     : 54
```

Average: 4.50. (I'm not sure why this performs worse for some patterns than polychrome.)

And I ran the "best" chooser backwards (pick the least-information choice) to get:
```
Rounds: Trials
1     : 1
2     : 4
3     : 25
4     : 108
5     : 312
6     : 557
7     : 226
8     : 56
9     : 7
```

Average: 5.80 (only slightly worse than the naive "first" chooser).
