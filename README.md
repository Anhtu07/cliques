Maximal cliques of a link stream
=============

Algorithm for computing cliques in link streams

Usage:
```
cat <data_file> | python main.py
```

Where data\_file is a sequence of quadruplets:
```
1 2 3 4
1 1 3 4
...
```
Meaning that between times 1 and 2, nodes 3 and 4 interacted, etc.

There is also a script to compute the delta-cliques:

```
cat <data_file> | python main-delta.py <int:delta>
```

Where data\_file is a sequence of triplets:
```
1 2 3
1 1 3
...
```
Meaning that at time 1, nodes 2 and 3 interacted, etc.


