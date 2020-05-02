from pypac.gameobjects import listing


class LameFactory(object):
    def __init__(self, game):
        self.game = game

    def get_or_create(self, type_id, properties, x, y):
        _type_class = listing.get(type_id)
        return _type_class(self.game, x, y)

    def create_from_type(self, type_class, properties, x, y):
        return type_class(self.game, x, y)
