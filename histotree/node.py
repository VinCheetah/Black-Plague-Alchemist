import pygame

from math import sqrt, atan2
class Condition:
    pass

    def __init__(self, condition="True"):
        self.condition: str = condition

    def eval(self, *args) -> bool:
        if type(self.condition) is str:
            return eval(self.condition)
        elif callable(self.condition):
            return self.condition(*args)


class Node:
    _id = 0

    def __init__(self, x, y):
        self.id: int = self._id
        Node._id += 1

        self.x, self.y = x, y
        self.size = 40
        self.color = 170, 130, 40

        self.name: str = f"Node {self.id}"
        self.outs: list[tuple[id, list[Condition], int]] = []
        self.add_init()

    def add_init(self):
        pass

    def set_id(self, new_id):
        self.id = new_id
        self.name = f"Node {self.id}"

    def add_dialogue(self, dialogue: str):
        self.dialogues.append(dialogue)

    def remove_dialogue(self, i):
        assert 0 <= i < len(self.dialogues)
        self.dialogues.pop(i)

    def reset_dialogues(self):
        self.dialogues = []

    def add_out(self, out=None, cond=None, priority=-1):
        self.outs.append((out, cond, priority))

    def reset_outs(self):
        self.outs = []

    def __repr__(self):
        return "Node n°" + str(self.id)

    def dist(self, x, y):
        return sqrt(pow(self.x - x, 2) + pow(self.y - y, 2))

    def move(self, rel_x, rel_y):
        self.x += rel_x
        self.y += rel_y

    def set_pos(self, p):
        self.x, self.y = p

    @property
    def pos(self):
        return self.x, self.y


class FightNode(Node):

    def add_init(self):
        self.size = 50
        self.color = 40, 120, 110


class TalkNode(Node):

    def add_init(self):
        self.size = 30
        self.color = 170, 30, 130


class Link:
    _id = 0

    def __init__(self, n1, n2):
        self.id: int = self._id
        Link._id += 1

        self.n1: Node = n1
        self.n2: Node = n2
        self.size = 8
        self.color = 100, 120, 40

        self.conditions: list = []

        self.name: str = f"Link n°{self.id}"
        self.add_init()

    def add_init(self):
        pass

    def set_id(self, new_id):
        self.id = new_id
        self.name = f"Node {self.id}"

    def __repr__(self):
        return "Link n°" + str(self.id)

    @property
    def angle(self):
        return atan2(self.n2.y - self.n1.y, self.n2.x - self.n1.x)

    @property
    def middle(self):
        return (self.n1.x + self.n2.x) / 2, (self.n1.y + self.n2.y) / 2

    @staticmethod
    def dist_pts(p1, p2):
        return pow(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2), 0.5)

    def dist(self, x, y):
        if (x - self.n1.x) * (self.n2.x - self.n1.x) + (y - self.n1.y) * (self.n2.y - self.n1.y) <= 0:
            return self.dist_pts(self.n1.pos, (x, y))
        if (x - self.n2.x) * (self.n1.x - self.n2.x) + (y - self.n2.y) * (self.n1.y - self.n2.y) <= 0:
            return self.dist_pts(self.n2.pos, (x, y))
        return abs((self.n2.x - self.n1.x) * (self.n1.y - y) - (self.n1.x - x) * (self.n2.y - self.n1.y)) / self.dist_pts(self.n1.pos, self.n2.pos)

    def move_pos(self, x, y):
        self.n1.move(x, y)
        self.n2.move(x, y)

class HistoTree:
    def __init__(self):
        self._root: Node | None = None
        self.graph: dict[Node, list[Node]] = {}
        self.nodes: set[Node] = set()
        self.links: set[Link] = set()

    def rooted(self) -> bool:
        try: return (self.root or True)
        except: return False

    @property
    def root(self) -> Node:
        if self._root is None:
            raise AttributeError("Root Not initialized")
        return self._root

    def set_root(self, new_root: Node):
        self._root = new_root

    def add_node(self, x, y):
        node = Node(x, y)
        self.nodes.add(node)
        self.graph[node] = []
        return node

    def add_link(self, n1, n2):
        if (n1, n2) not in self.links:
            self.links.add(Link(n1, n2))
            self.graph[n1].append(n2)
            return True
        return False

    def delete_node(self, node):
        self.nodes.discard(node)
        if node == self.root:
            self._root = None
        link_bin = set()
        for link in self.links:
            if node in link:
                if node == link.n2:
                    self.graph[link.n1].remove(node)
                link_bin.add(link)
        self.links = self.links.symmetric_difference(link_bin)
        del self.graph[node]

    def __repr__(self):
        return f"Nodes : {self.nodes}\nLinks : {self.links}"

    def __str__(self):
        return self.__repr__()

