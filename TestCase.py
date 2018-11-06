from SheepTree import *

class Cls(object):
    def __init__(self, n=1):
        self.v = n
        self._children = []

    def __str__(self):
        return str(self.v)

    def addChild(self, cls):
        self._children.append(cls)

    def get_children(self):
        return self._children


if __name__ == '__main__':
    clss = [Cls(i) for i in range(7)]
    for i in range(3):
        clss[i].addChild(clss[2 * i + 1])
        clss[i].addChild(clss[2 * i + 2])

    SheepTree(clss[0])
