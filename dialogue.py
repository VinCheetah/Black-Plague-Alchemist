class DialogueNode:

    def __init__(self, config):
        self.priority: int = config.priority
        self.children: list[DialogueNode] = config.childrens
        self.dialogue = config.dialogue
        self.conditions = config.conditions

    def next_dialogue(self, game):
        max_prior, next_dialogue = 0, None
        for child in self.children:
            if game.verify(child.conditions) and child.priority > max_prior:
                max_prior, next_dialogue = child.priority, child
        return next_dialogue
