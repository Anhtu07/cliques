
from CliqueMaster import CliqueMaster
from Clique import Clique
import sys

# Initiate
Cm = CliqueMaster()
times = dict()
nodes = dict()
nb_lines = 0
resurrect = False

# Read arguments from command line
if len(sys.argv) != 2:
    sys.stderr.write(
        "Usage: cat <stream> | python main.py <delta>\
        \n\n")
    sys.exit(1)

omega = None
delta = float(sys.argv[1])
old_t = None

# Read stream sorted by b, then e
for line in sys.stdin:
    contents = line.split()
    t = float(contents[0])
    u = contents[1].strip()
    v = contents[2].strip()

    # Update value of omega
    if omega == None or omega < t:
        omega = t

    link = frozenset([u, v])
    time = (t-delta/2, t-delta/2)


    # Populate data structures
    if link not in times:
        times[link] = []
        # this is a new link
        times[link].append((t-delta/2, t+delta/2))
        # this corresponds to a trivial clique
        Cm.addClique(Clique((link, time), set([])))

    else:
        # get last link
        (cur_b, cur_e) = times[link][-1]
        # print(u,v,t, cur_b, cur_e)
        if t-delta/2 <= cur_e:
            # continuation of an existing link, merge
            times[link][-1] = (cur_b, t+delta/2)
        else:
            # this is a new link
            times[link].append((t-delta/2, t+delta/2))
            # this corresponds to a trivial clique
            Cm.addClique(Clique((link, time), set([])))


    if u not in nodes:
        nodes[u] = set()

    if v not in nodes:
        nodes[v] = set()

    nodes[u].add(v)
    nodes[v].add(u)


    
    assert( (old_t == None) or (t >= old_t) )

    old_t = t
    nb_lines = nb_lines + 1


#Debug: print all links in dataset
# for link in times:
#     for time in times[link]:
#         for v in link:
#             sys.stdout.write("%s "%v)
#         print(time[0], time[1])
    
Cm._times = times
Cm._nodes = nodes
sys.stderr.write("Processed " + str(nb_lines) + " from stdin\n")

## Start execution
R = Cm.getMaximalCliques(omega+delta/2)
Cm.printCliques()
