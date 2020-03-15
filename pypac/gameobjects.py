import pyglet

from pypac.client.graphics import sprite_sheet, tile_sheet

MOVE_LEFT = 0
MOVE_RIGHT = 1
MOVE_UP = 2
MOVE_DOWN = 3


class GameObject(object):
    base_img = None

    def __init__(self, game, x, y):
        self.game = game
        self.sprite = pyglet.sprite.Sprite(
            x=x,
            y=y,
            img=self.base_img,
            batch=self.game.game_objects_batch)
        self.move_speed = 1
        self.move_target = None

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

    def _move_to_target(self):
        grid_x, grid_y = self.move_target
        collider = self.game.level.static_collision_map
        if not collider.check_collision(grid_x, grid_y):
            tx = grid_x * 16
            ty = grid_y * 16
            if tx > self.x:
                self.x += self.move_speed
            elif tx < self.x:
                self.x -= self.move_speed

            if ty > self.y:
                self.y += self.move_speed
            elif ty < self.y:
                self.y -= self.move_speed
        else:
            self.move_target = None

    def _move_to(self, x_mod, y_mod, move_dir):
        new_x, new_y = self.x + x_mod, self.y + y_mod
        grid_x = int(new_x / 16)
        grid_y = int(new_y / 16)
        if move_dir == MOVE_LEFT:
            new_y = grid_y * 16
        elif move_dir == MOVE_RIGHT:
            new_y = grid_y * 16
            grid_x += 1
        elif move_dir == MOVE_UP:
            new_x = grid_x * 16
        elif move_dir == MOVE_DOWN:
            new_x = grid_x * 16
            grid_y = grid_y + 1


class Pacman(GameObject):
    right = sprite_sheet.get_region(7, 0)
    right_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(7, 0), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(7, 1), 0.15),
    ])

    left = sprite_sheet.get_region(6, 0)
    left_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(6, 0), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(6, 1), 0.15),
    ])

    up = sprite_sheet.get_region(5, 0)
    up_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(5, 0), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(5, 1), 0.15),
    ])

    down = sprite_sheet.get_region(5, 0)
    down_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(4, 0), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(4, 1), 0.15),
    ])

    base_img = left_animation

    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.game = game
        self._last_move = None
        self.move_speed = 2

    def update(self):
        if self.move_target is not None:
            if self.x == self.move_target[0] * 16 and self.y == self.move_target[1] * 16:
                self.move_target = None
            else:
                self._move_to_target()

    def move_left(self):
        if self.move_target is None:
            self.move_target = int(self.x / 16) - 1, int(self.y / 16)
            if self._last_move != MOVE_LEFT:
                self.sprite.image = self.left_animation
                self._last_move = MOVE_LEFT

    def move_right(self):
        if self.move_target is None:
            self.move_target = int(self.x / 16) + 1, int(self.y / 16)
            if self._last_move != MOVE_RIGHT:
                self.sprite.image = self.right_animation
                self._last_move = MOVE_RIGHT

    def move_down(self):
        if self.move_target is None:
            self.move_target = int(self.x / 16), int(self.y / 16) + 1
            if self._last_move != MOVE_UP:
                self.sprite.image = self.up_animation
                self._last_move = MOVE_UP

    def move_up(self):
        if self.move_target is None:
            self.move_target = int(self.x / 16), int(self.y / 16) - 1
            if self._last_move != MOVE_DOWN:
                self.sprite.image = self.down_animation
                self._last_move = MOVE_DOWN


class Wall(GameObject):
    base_img = tile_sheet.get_region(0, 0)


class SmallWhiteDot(GameObject):
    base_img = tile_sheet.get_region(6, 13)


class MediumWhiteDot(GameObject):
    base_img = tile_sheet.get_region(6, 14)


class LargeWhiteDot(GameObject):
    base_img = tile_sheet.get_region(6, 15)
