# -*-coding:utf8*-
from collections import deque
from Clique import Clique


class CliqueMaster:

    def __init__(self):
        self._S = deque()
        self._S_set = set()
        self._R = set()
        self._times = dict()
        self._nodes = dict()

    def addClique(self, c):
        """ Adds a clique to S,
        checking beforehand that this clique is not already present in S. """
        if c not in self._S_set:
            self._S.appendleft(c)
            #self._S.append(c)
            self._S_set.add(c)

    def getClique(self):
        c = self._S.pop()
        return c

    def getMaximalCliques(self, omega):
        """ Returns a set of maximal cliques. """

        while len(self._S) != 0:
            c = self.getClique()
            is_max = True

            # Grow time on the right side
            td = c.getTd(self._times, omega)
            if td != c._te:
                c_add = Clique((c._X, (c._tb, td)), c._candidates)
                
                self.addClique(c_add)

                is_max = False

            # Grow node set
            candidates = c.getAdjacentNodes(self._times, self._nodes)

            for node in candidates:
                if c.isClique(self._times, node):
                    Xnew = set(c._X).union([node])
                    c_add = Clique(
                        (frozenset(Xnew), (c._tb, c._te)), c._candidates)

                    self.addClique(c_add)
                    
                    is_max = False


            if is_max:
                self._R.add(c)
        return self._R

    def printCliques(self):
        return None

    def __str__(self):
        msg = ""
        for c in self._R:
            msg += str(c) + "\n"
        return msg
