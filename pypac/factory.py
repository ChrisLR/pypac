from pypac import gameobjects


class LameFactory(object):
    def __init__(self, game):
        self.game = game
        self._mapping = {
            "pacman": self.make_pacman,
            "wall_ne_curve": self.make_wall,
            "wall_nw_curve": self.make_wall,
            "wall_e": self.make_wall,
            "wall_w": self.make_wall,
            "wall_se_curve": self.make_wall,
            "wall_sw_curve": self.make_wall,
            "wall_se": self.make_wall,
            "wall_sw": self.make_wall,
            "wall_ne": self.make_wall,
            "wall_nw": self.make_wall,
            "wall_n": self.make_wall,
            "wall_s": self.make_wall,
            "small_white_dot": self.make_dot,
            "medium_white_dot": self.make_dot,
            "large_white_dot": self.make_dot,
        }

    def get_or_create(self, type_id, properties, x, y):
        create_func = self._mapping.get(type_id)
        if create_func is None:
            raise ValueError(f"Unknown type id {type_id}")

        return create_func(x, y, properties)

    def make_pacman(self, x, y, properties):
        return gameobjects.Pacman(self.game, x, y)

    def make_wall(self, x, y, properties):
        return gameobjects.Wall(self.game, x, y)

    def make_dot(self, x, y, properties):
        return gameobjects.SmallWhiteDot(self.game, x, y)
