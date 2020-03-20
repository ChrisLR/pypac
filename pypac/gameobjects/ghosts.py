import pyglet

from pypac.client.graphics import sprite_sheet
from pypac.gameobjects import listing
from pypac.gameobjects.base import Actor


class Ghost(Actor):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.move_speed = 2


@listing.register
class GhostRed(Ghost):
    right_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(3, 3), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(3, 4), 0.15),
    ])
    left_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(3, 5), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(3, 6), 0.15),
    ])
    up_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(3, 7), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(3, 8), 0.15),
    ])
    down_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(3, 9), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(3, 10), 0.15),
    ])

    base_img = left_animation
    type_id = "ghost_red"


@listing.register
class GhostPink(Ghost):
    right_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 3), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 4), 0.15),
    ])
    left_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 5), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 6), 0.15),
    ])
    up_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 7), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 8), 0.15),
    ])
    down_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 9), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 10), 0.15),
    ])

    base_img = left_animation
    type_id = "ghost_pink"


@listing.register
class GhostPink(Ghost):
    right_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 3), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 4), 0.15),
    ])
    left_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 5), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 6), 0.15),
    ])
    up_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 7), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 8), 0.15),
    ])
    down_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 9), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(2, 10), 0.15),
    ])

    base_img = left_animation
    type_id = "ghost_pink"


@listing.register
class GhostTeal(Ghost):
    right_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(1, 3), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(1, 4), 0.15),
    ])
    left_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(1, 5), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(1, 6), 0.15),
    ])
    up_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(1, 7), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(1, 8), 0.15),
    ])
    down_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(1, 9), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(1, 10), 0.15),
    ])

    base_img = left_animation
    type_id = "ghost_teal"


@listing.register
class GhostPeach(Ghost):
    right_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(0, 3), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(0, 4), 0.15),
    ])
    left_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(0, 5), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(0, 6), 0.15),
    ])
    up_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(0, 7), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(0, 8), 0.15),
    ])
    down_animation = pyglet.image.animation.Animation(frames=[
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(0, 9), 0.15),
        pyglet.image.animation.AnimationFrame(sprite_sheet.get_region(0, 10), 0.15),
    ])

    base_img = left_animation
    type_id = "ghost_peach"
