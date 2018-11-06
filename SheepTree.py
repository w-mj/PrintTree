import tkinter as tk
import queue

class _SheepTreeNode(object):
    def __init__(self, obj, parent, depth=0):
        self.text = str(obj)
        self.max_width = 0
        self.depth = depth
        self.parent = parent
        self.children = []
        for x in obj.get_children():
            self.children.append(_SheepTreeNode(x, self, depth + 1))
        if len(self.children) == 0:
            self.max_width = 1
            self.max_depth = 0
        else:
            self.max_width = max([x.max_width for x in self.children])
            self.max_width = max(self.max_width, len(self.children))
            self.max_depth = max([x.max_depth for x in self.children])
        self.line_text = []
        self.obj = obj
        self.is_leave = len(self.children) == 0

class SheepTree(object):
    def __init__(self, cls):
        self._window = tk.Tk()
        self._tree = _SheepTreeNode(cls, None)
        self._level = []
        self._width = self._get_tree_width(cls)
        self._height = self._get_tree_height(cls)
        self._window.geometry("800x600")
        print("tree height {}".format(self._height))
        print("tree width {}".format(self._width))
        self._canvas = tk.Canvas(self._window, width=800, height=600)
        self._canvas.pack()

        self.draw(0, self._width * 100, self._tree)
        self._window.mainloop()


    def draw(self, x, max_width, tree):
        self._draw_node((x + max_width) // 2, tree.depth, tree)
        if not tree.is_leave:
            p = [x.max_width for x in tree.children]
            sum_p = sum(p)
            p = [x / sum_p for x in p]
            dw = max_width - x
            width = [dw * x for x in p]
            last_all = x
            for i, x in enumerate(tree.children):
                w = width[i]
                self.draw(last_all, last_all + w, x)
                last_all += w


    def _draw_node(self, x, y, cls):
        y = y * 100
        self._canvas.create_oval(x + 20, y + 20, x + 80, y + 80)
        self._canvas.create_text(x + 50, y + 50, text=cls.text)


    def _get_tree_height(self, tree, n=1):
        maxh = [self._get_tree_height(x, n + 1) for x in tree.get_children()]
        return max(maxh) if len(maxh) > 0 else n

    def _get_tree_width(self, tree):
        q = queue.Queue()
        q.put(tree)
        current_w = 1
        max_w = 0
        self._level.append([tree])
        while not q.empty():
            self._level.append([])
            while current_w:
                ele = q.get()
                for x in ele.get_children():
                    q.put(x)
                    self._level[-1].append(x)
                current_w -= 1
            max_w = max(max_w, q.qsize())
            current_w = q.qsize()
        return max_w

