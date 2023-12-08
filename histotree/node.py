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

    def __init__(self):
        self.id: int = self._id
        Node._id += 1

        self.name: str = f"Node {self.id}"
        self.dialogues: list[str] = []
        self.outs: list[tuple[id, list[Condition], int]] = []

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


class HistoTree:
    def __init__(self):
        self.root: Node
        self.graph: dict[Node, Node] = {}
