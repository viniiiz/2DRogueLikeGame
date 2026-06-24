from code import Entity


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []  # List to hold all entities in the level


    def run_level(self, ):
        print(f"Running {self.name} with game mode: {self.game_mode}")
        pass