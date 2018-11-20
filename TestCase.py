from Tree import *

class Cls(object):
    def __init__(self, n=1):
        self.v = n
        self.name = str(n)
        self.children = []

    def __str__(self):
        return str(self.v)

    def addChild(self, cls):
        self.children.append(cls)
        return self

    def get_children(self):
        return self.children


if __name__ == '__main__':
    n = [Cls(i) for i in range(20)]
    n[0].addChild(n[1]).addChild(n[11])
    n[0].addChild(n[2]).addChild(n[12])
    n[2].addChild(n[3])
    n[2].addChild(n[4])
    n[4].addChild(n[5])
    n[4].addChild(n[6])
    n[5].addChild(n[7])
    n[5].addChild(n[8])
    n[6].addChild(n[9]).addChild(n[10])

    PrintTree(n[0])
