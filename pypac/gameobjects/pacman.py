import pyglet

from pypac.client.graphics import sprite_sheet
from pypac.gameobjects.base import Actor


class Pacman(Actor):
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
        self.move_speed = 2
