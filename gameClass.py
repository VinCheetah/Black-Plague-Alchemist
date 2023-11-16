import place

class Game:

    def __init__(self):
        self.main_character = []
        self.place =
        self.group_inventory = []
        self.characters = []

    def start(self):
        self.init_starting()

    def init_starting(self):
        self.place = place.Home()
