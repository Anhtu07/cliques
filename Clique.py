# -*-coding:utf8*-


class Clique:

    def __init__(self, c, candidates=set([])):
        (X, (tb, te)) = c
        self._X = X
        self._tb = tb
        self._te = te
        self._candidates = candidates

    def __eq__(self, other):
        if self._X == other._X and self._tb == other._tb and self._te == other._te:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self._X, self._tb, self._te))

    def __str__(self):
        return ','.join(map(str, list(self._X))) + " " + \
            str(self._tb) + "," + str(self._te)

    def getAdjacentNodes(self, times, nodes):
        if self._te - self._tb == 0:
            for u in self._X:
                neighbors = nodes[u]
                for n in neighbors:
                    self._candidates.add(n)
                    
        self._candidates = self._candidates.difference(self._X)
        return self._candidates

    def __repr__(self):
        return str(self)

    def isClique(self, times, node):
        """ returns True if X(c) union node is a clique over tb;te, False otherwise"""

        # sys.stderr.write("Begin isClique: nodes : %s b : %f e : %f, node %s \n"%(self._X.__str__(),self._tb, self._te, node))
        for i in self._X:
            # sys.stderr.write("testing link between nodes %s and %s \n"%(i, node))
            # Clem 20171031
            # if frozenset([i, node]) not in times.keys():
            if frozenset([i, node]) not in times:
                # Check that (i, node) exists in stream.
                return False
            else:
                link = frozenset([i, node])
                # Check there is a link (b, e, i, node) s.t. b <= tb and e >= te, otherwise not a clique.
                
                #tlist is a list of non-overlapping couples (b,e)
                tlist = times[link]
                # start binary search for b in tlist
                first = 0
                last = len(tlist)-1
                middle = (first+last)//2
                # sys.stderr.write("  Debug binary search: %f %f\n"%(self._tb, self._te))
                # sys.stderr.write("  tlist : %s\n"%tlist.__str__())
                while first <= last:
                    # sys.stderr.write("  First %g last %g\n"%(first, last))
                    if tlist[middle][0] > self._tb:
                        last = middle - 1
                    elif tlist[middle][1] < self._tb:
                        first = middle + 1
                    else:
                        # found a link that contains b
                        # sys.stderr.write("  Found link %f %f\n"%(tlist[middle][0], tlist[middle][1]))
                        assert tlist[middle][0] <= self._tb and tlist[middle][1] >= self._tb
                        if tlist[middle][1] < self._te:
                            # sys.stderr.write("  Found link not long enough, return False\n")
                            return False
                        break
                    middle = (first + last ) // 2
                # if we are here without having found a link that contains self._tb
                if first > last:
                    # sys.stderr.write("  No satisfying link found, return False\n")
                    return False
                
        return True

    def getTd(self, times, omega):
        # Pour chaque lien dans X, Récupérer dans T les temps x tq te < x
        # . Si len(T) = 1, regarder si x est plus petit que le tmin déjà
        # connu.
        td = 0
        min_t = None
        for u in self._X:
            for v in self._X:
                link = frozenset([u, v])
                if link in times:
                    # Find min time x > te s.t. (b,x,u,v) exists in stream
                    tlist = times[link]

                    first = 0
                    last = len(tlist)-1
                    middle = (first+last)//2
                    # sys.stderr.write("  Debug binary search: %f %f\n"%(self._tb, self._te))
                    # sys.stderr.write("  tlist : %s\n"%tlist.__str__())
                    while first <= last:
                        # sys.stderr.write("  First %g last %g\n"%(first, last))
                        if tlist[middle][0] > self._tb:
                            last = middle - 1
                        elif tlist[middle][1] < self._tb:
                            first = middle + 1
                        else:
                            # found a link that contains b
                            # sys.stderr.write("  Found link %f %f\n"%(tlist[middle][0], tlist[middle][1]))
                            assert tlist[middle][0] <= self._tb and tlist[middle][1] >= self._tb
                            assert tlist[middle][1] >= self._te
                            if min_t != None:
                                min_t = min(min_t, tlist[middle][1])
                            else:
                                min_t = tlist[middle][1]
                            break
                        middle = (first + last ) // 2

                    # We should not be here except for a break in the while loop above
                    assert first <= last
        return min_t

