import pygame

from math import sqrt, atan2

import color


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
        self.properties = set()

        self.x, self.y = x, y
        self.size = 40
        self.color = 170, 130, 40

        self._name = None
        self.type = None
        self.outs: list[tuple[id, list[Condition], int]] = []
        self.add_init()
        self.set_name()

    def add_init(self):
        pass

    def set_id(self, new_id):
        self.id = new_id

    def set_name(self, new_name=None):
        self._name = new_name or self._name
        size = 30
        while 1.7 * self.size < pygame.font.SysFont("Courier New", size).render(self.name, True, color.WHITE).get_width():
            size -= 1
        self.size_text = size

    @property
    def name(self):
        return self._name or f"Node {self.id}"

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

    def add_property(self, prop, value):
        self.properties.add(prop)
        setattr(self, prop, value)


class FightNode(Node):

    def add_init(self):
        self.size = 50
        self.color = 40, 120, 110
        self.type = "Fight"


class TalkNode(Node):

    def add_init(self):
        self.size = 30
        self.color = 170, 30, 130
        self.type = "Talk"
        self.add_property("speaker", "")
        self.add_property("messages", [])


class PlaceNode(Node):

    def add_init(self):
        self.color = 30, 170, 140
        self.type = "Place"
        self.add_property("place", "")
        self.add_property("subplace", "")

class ChoiceNode(Node):

    def add_init(self):
        self.color = 230, 160, 100
        self.type = "Choice"

class Link:
    _id = 0

    def __init__(self, n1, n2):
        self.id: int = self._id
        Link._id += 1

        self.n1: Node = n1
        self.n2: Node = n2
        self.size = 8
        self.nodes = self.n1, self.n2
        self.color = 100, 120, 170

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

    def add_node(self, x, y, t=None):
        node = (t or Node)(x, y)
        self.nodes.add(node)
        self.graph[node] = []
        return node

    def replace_node(self, new_node, old_node):
        self.nodes.discard(old_node)
        self.nodes.add(new_node)
        self.graph[new_node] = self.graph[old_node][:]
        del self.graph[old_node]
        for adj in self.graph.values():
            if old_node in adj:
                adj.remove(old_node)
                adj.append(new_node)
        link_bin = {link for link in self.links if old_node in link.nodes}
        for link in link_bin:
            if link.n1 == old_node:
                self.links.add(Link(new_node, link.n2))
            else:
                self.links.add(Link(link.n1, new_node))
        self.links = self.links.difference(link_bin)

    def change_type_node(self, node, new_type):
        new_node = (new_type or Node)(*node.pos)
        self.transfer_info(new_node, node)
        self.replace_node(new_node, node)
        return new_node

    def transfer_info(self, new_node: Node, old_node: Node):
        new_node.set_name(old_node._name)
        for prop in old_node.properties:
            new_node.add_property(prop, getattr(old_node, prop))


    def add_link(self, n1, n2):
        if (n1, n2) not in self.links:
            self.links.add(Link(n1, n2))
            self.graph[n1].append(n2)
            return True
        return False

    def delete_node(self, node):
        self.nodes.discard(node)
        if self.rooted() and node == self.root:
            self._root = None
        link_bin = set()
        for link in self.links:
            if node in link.nodes:
                if node == link.n2:
                    self.graph[link.n1].remove(node)
                link_bin.add(link)
        self.links = self.links.symmetric_difference(link_bin)
        del self.graph[node]

    def delete_link(self, link):
        self.links.discard(link)
        self.graph[link.n1].remove(link.n2)

    def __repr__(self):
        return f"Nodes : {self.nodes}\nLinks : {self.links}"

    def __str__(self):
        return self.__repr__()

