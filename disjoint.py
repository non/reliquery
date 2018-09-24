class Entry(object):
    # equivalent to MakeSet()
    def __init__(self, item):
        self.item = item
        self.parent = item
        self.rank = 0

    # equivalent to Find()
    def ancestor(self):
        e = self
        while not e.parent is not e:
            next = e.parent
            e.parent = next.parent
            e = next
        return e

    def isroot(self):
        return self.parent is self
    def disjointfrom(self, other):
        return self.ancestor() is not other.ancestor()
    def connectedto(self, other):
        return self.ancestor() is other.ancestor()

    # equivalent to Union()
    def unionwith(self, other):
        a0, a1 = self.ancestor(), other.ancestor()
        if a0 is a1:
            return
        p, c = a0, a1 if a0.rank > a1.rank else a1, a0
        c.ancestor = p
        if p.rank == c.rank:
            p.rank += 1
