
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
if len(sys.argv) != 1:
    sys.stderr.write(
        "Usage: cat <stream> | python main.py\
        \n\n")
    sys.exit(1)

omega = None
old_b = None
old_e = 0

# Read stream sorted by b, then e
for line in sys.stdin:
    contents = line.split()
    b = float(contents[0])
    e = float(contents[1])
    u = contents[2].strip()
    v = contents[3].strip()

    # Update value of omega
    if omega == None or omega < e:
        omega = e


    link = frozenset([u, v])
    time = (b, b)

    # This a new instance
    Cm.addClique(Clique((link, time), set([])))

    # Populate data structures
    if link not in times:
        times[link] = []
    times[link].append((b,e))

    if u not in nodes:
        nodes[u] = set()

    if v not in nodes:
        nodes[v] = set()

    nodes[u].add(v)
    nodes[v].add(u)

    assert(b <= e)
    assert( (old_b == None) or (b >= old_b) )
    if b == old_b:
        assert(e >= old_e)

    (old_b,old_e) = (b,e)
    nb_lines = nb_lines + 1

Cm._times = times
Cm._nodes = nodes
sys.stderr.write("Processed " + str(nb_lines) + " from stdin\n")

# Start execution
R = Cm.getMaximalCliques(omega)
Cm.printCliques()
