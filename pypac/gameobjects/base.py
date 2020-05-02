import pyglet

from pypac.actions import Actions
from pypac import geom


class GameObject(object):
    base_img = None
    blocking = False
    type_id = "game_object"

    def __init__(self, game, x, y):
        self.game = game
        self.dead = False
        self._rectangle = geom.Rectangle(x, y, 16, 16)
        self.score = None
        self.sprite = pyglet.sprite.Sprite(
            x=x,
            y=y,
            img=self.base_img,
            batch=self.game.game_objects_batch)

    @property
    def x(self):
        return self.sprite.x

    @x.setter
    def x(self, value):
        self.sprite.x = value

    @property
    def y(self):
        return self.sprite.y

    @y.setter
    def y(self, value):
        self.sprite.y = value

    @property
    def rectangle(self):
        self._rectangle.x = self.sprite.x
        self._rectangle.y = self.sprite.y
        return self._rectangle

    def collide_with(self, other_object):
        pass

    def die(self):
        pass


class Actor(GameObject):
    type_id = "actor"

    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.move_speed = 1
        self.actions = Actions(self)

    def update(self):
        self.actions.update()
