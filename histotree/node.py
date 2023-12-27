import pygame

from math import sqrt
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

        self.pos = self.x, self.y = x, y
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
        return str(self.id)

    def dist(self, x, y):
        return sqrt(pow(self.x - x, 2) + pow(self.y - y, 2))

    def move(self, rel_x, rel_y):
        self.x += rel_x
        self.y += rel_y

    def set_pos(self, pos):
        self.pos = self.x, self.y = pos



class FightNode(Node):

    def add_init(self):
        self.size = 50
        self.color = 40, 120, 110


class TalkNode(Node):

    def add_init(self):
        self.size = 30
        self.color = 170, 30, 130




class HistoTree:
    def __init__(self):
        self._root: Node | None = None
        self.graph: dict[Node, list[Node]] = {}
        self.nodes: set[Node] = set()
        self.links: set[tuple[Node, Node]] = set()

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
            self.links.add((n1, n2))
            self.graph[n1].append(n2)
            return True
        return False

    def delete_node(self, node):
        self.nodes.discard(node)
        link_bin = set()
        for link in self.links:
            if node in link:
                if node == link[1]:
                    self.graph[link[0]].remove(node)
                link_bin.add(link)
        self.links = self.links.symmetric_difference(link_bin)
        del self.graph[node]

    def __repr__(self):
        return f"Nodes : {self.nodes}\nLinks : {self.links}"

    def __str__(self):
        return self.__repr__()

