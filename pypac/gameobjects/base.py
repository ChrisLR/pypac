import pyglet

from pypac.actions import Actions


class GameObject(object):
    base_img = None

    def __init__(self, game, x, y):
        self.game = game
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


class Actor(GameObject):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.move_speed = 1
        self.actions = Actions(self)

    def update(self):
        self.actions.update()
