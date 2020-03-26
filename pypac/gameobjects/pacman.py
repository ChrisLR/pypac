import pyglet

from pypac.client.graphics import sprite_sheet
from pypac.gameobjects.base import Actor
from pypac.gameobjects import listing


@listing.register
class Pacman(Actor):
    right_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(7, 0), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(7, 1), 0.15),
    ])
    left_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(6, 0), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(6, 1), 0.15),
    ])
    up_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(5, 0), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(5, 1), 0.15),
    ])
    down_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(4, 0), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(4, 1), 0.15),
    ])

    base_img = left_animation
    type_id = "pacman"

    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.move_speed = 2

    def collide_with(self, other_object):
        if other_object.type_id in {"small_white_dot", "medium_white_dot", "large_white_dot"}:
            # TODO ADD SCORE
            self.game.level.remove_static(other_object)