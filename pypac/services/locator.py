class LocatorService(object):
    """
    This object returns the requested live game_objects
    """
    def __init__(self, game):
        self.game = game
        self._pacmen = None
        self._ghosts = None

    def update(self):
        """
        We update our cache only once every update
        """
        self._pacmen = None
        self._ghosts = None

    def get_pacmen(self):
        if self._pacmen:
            return self._pacmen

        game_objects = self.game.game_objects
        self._pacmen = [
            game_object for game_object in game_objects
            if game_object.type_id == "pacman"
        ]

        return self._pacmen

    def get_ghosts(self):
        if self._ghosts:
            return self._ghosts

        game_objects = self.game.game_objects
        self._ghosts = [
            game_object for game_object in game_objects
            if game_object.type_id.startswith("ghost_")
        ]

        return self._ghosts
