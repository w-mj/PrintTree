import tkinter as tk
import queue
import math
import json
import sys


def _td_g(c, n):
    if isinstance(c, dict):
        return c.get(n, [])
    return c.__dict__.get(n, [])


class PrintTree(object):
    class Node:
        def __init__(self, name, id, parent, layer):
            self.name = name
            self.id = id
            self.relative_x_offset = 0
            self.x_offset = 0
            self.layer = layer
            self.parent = parent
            self.children = []
            self.x = 0
            self.y = 0
            self.dis_brother = 0

    def get_id(self):
        i = 0
        while True:
            yield i
            i += 1



    def _build(self, cls):
        qn = queue.Queue()
        qo = queue.Queue()
        nodes = []
        qo.put(cls)
        iid = self.get_id()
        qn.put(self.Node(_td_g(cls, 'name'), next(iid), None, 0))
        while not qo.empty():
            cn = qo.get()
            nn = qn.get()
            nodes.append(nn)

            for i, child in enumerate(_td_g(cn, 'children')):
                new_n = self.Node(_td_g(child, 'name'), next(iid), nn, nn.layer + 1)
                new_n.relative_x_offset = + (2 * i - len(_td_g(cn, 'children')) + 1)
                new_n.x_offset = nn.x_offset + new_n.relative_x_offset
                nn.children.append(new_n)
                qn.put(new_n)
                qo.put(child)

        key_node = {}

        def get_dis(i, j):
            d = key_node.get((i, j), 0)
            return d


        num_nodes = len(nodes)
        for i in range(num_nodes - 1):
            if nodes[i].layer == nodes[i + 1].layer:
                pl = nodes[i]
                pr = nodes[i + 1]
                while pl.parent != pr.parent:
                    pl = pl.parent
                    pr = pr.parent

                d = (nodes[i].relative_x_offset - nodes[i + 1].relative_x_offset)
                if get_dis(pl.id, pr.id) < d:
                    key_node[(pl.id, pr.id)] = d + (pr.id - pl.id - 1)



        for node in nodes:
            length = 0
            for i in range(1, len(node.children)):
                fni = node.children[0].id
                cni = node.children[i].id
                d = i
                for k in range(i):
                    mni = node.children[k].id
                    d = max(d, get_dis(fni, mni) + get_dis(mni, cni))
                node.children[i].dis_brother = d
            for i, child in enumerate(node.children):
                if len(node.children) <= 1:
                    child.relative_x_offset = 0
                else:
                    length = node.children[-1].dis_brother
                    child.relative_x_offset = child.dis_brother - length // 2
                child.x_offset = node.x_offset + child.relative_x_offset

        lwidth = 0
        rwidth = 0
        height = 0
        for node in nodes:
            lwidth = min(lwidth, node.x_offset)
            rwidth = max(rwidth, node.x_offset)
            height = max(height, node.layer)

        return nodes, key_node, -lwidth, round(rwidth - lwidth + 1), height + 1



    def _draw(self, nodes, x0, y0):
        n_size = self.node_size
        r_size = self.radius
        l_height = self.layer_height
        nodes[0].x = x0 * n_size + n_size / 2
        nodes[0].y = y0 + n_size / 2
        for i in range(1, len(nodes)):
            n = nodes[i]
            n.x = n.parent.x + (n.dis_brother - len(n.parent.children) / 2) * n_size + n_size / 2
            n.y = n.layer * l_height + n_size / 2 + y0
        top = tk.Tk()
        top.geometry("{}x{}".format(self.width * self.node_size, self.height * self.layer_height))

        can = tk.Canvas(top, width=self.width * self.node_size, height=self.height * self.layer_height)
        can.pack()
        for n in nodes:
            can.create_oval(n.x - r_size, n.y - r_size, n.x + r_size, n.y + r_size)
            can.create_text(n.x, n.y, text=n.name)
            for c in n.children:
                x0 = n.x
                y0 = n.y
                x1 = c.x
                y1 = c.y
                theta = math.atan2(y1 - y0, x0 - x1)
                x1 = x1 + r_size * math.cos(theta)
                y1 = y1 - r_size * math.sin(theta)
                x0 = x0 - r_size * math.cos(theta)
                y0 = y0 + r_size * math.sin(theta)
                can.create_line(x0, y0, x1, y1)

        top.mainloop()

    def __init__(self, cls):
        if isinstance(cls, str):
            cls = json.loads(cls)
        self.layer_height = 50
        self.node_size = 40
        self.radius = 15
        self.nodes, self.key_nodes, x0, self.width, self.height = self._build(cls)
        # self.nodes = self._cal(self.nodes, x0, 10)
        self._draw(self.nodes, x0, 10)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        exit(-1)
    else:
        if sys.argv[1] == '-f':
            if len(sys.argv) < 3:
                exit(-1)
            else:
                with open(sys.argv[2]) as f:
                    s = f.read()
        else:
            s = sys.argv[1]
        PrintTree(s)

