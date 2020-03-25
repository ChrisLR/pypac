import math
from pypac.geom import Rectangle


class Level(object):
    """
    A container of objects and statics representing a game level.
    """
    def __init__(self, name, width, height, origin_array):
        self.name = name
        self.width = width
        self.height = height
        self.game_objects = []
        self.statics = []
        self.static_collision_map = CollisionMap(width, height)
        self.background_image = None
        self.background_image_offset = None
        self.background_color = None
        self.origin_array = origin_array

    def add_game_object(self, game_object):
        self.game_objects.append(game_object)

    def add_static(self, static_object):
        rectangle = Rectangle(static_object.x, static_object.y, 16, 16)
        self.statics.append(static_object)
        self.static_collision_map.add_collider(static_object, rectangle)

    def set_background_image(self, image, offset):
        self.background_image = image
        self.background_image_offset = offset

    def remove_static(self, static_object):
        rectangle = Rectangle(static_object.x, static_object.y, 16, 16)
        self.statics.remove(static_object)
        self.static_collision_map.remove_collider(rectangle)

    def remove_game_object(self, game_object):
        self.game_objects.remove(game_object)


class CollisionMap(object):
    """
    An object containing rectangles of static game objects for collisions
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.width_tiles = int(math.ceil(width / 16)) + 1
        self.height_tiles = int(math.ceil(height / 16)) + 1
        self._collision_map = [[None for _ in range(self.height_tiles)] for _ in range(self.width_tiles)]

    def add_collider(self, collider, rectangle):
        width_tiles = int(rectangle.width / 16)
        height_tiles = int(rectangle.height / 16)
        ox = int(rectangle.left / 16)
        oy = int(rectangle.top / 16)
        for x in range(ox, ox + width_tiles):
            for y in range(oy, oy + height_tiles):
                self._collision_map[x][y] = collider

    def check_collision(self, x, y):
        if x <= 0 or y <= 0 or x >= self.width or y >= self.height:
            return True
        return self._collision_map[x][y]

    def check_collision_point(self, point):
        return self._collision_map[point.x][point.y]

    def check_collision_rect(self, rectangle):
        collisions = set()
        for x in range(int(rectangle.left), int(math.ceil(rectangle.right))):
            for y in range(int(rectangle.top), int(math.ceil(rectangle.bottom))):
                if x < 0 or x >= self.width:
                    continue
                if y < 0 or y >= self.height:
                    continue
                collision = self._collision_map[x][y]
                if collision is not None:
                    collisions.add(collision)

        return collisions

    def remove_collider(self, rectangle):
        width_tiles = int(rectangle.width / 16)
        height_tiles = int(rectangle.height / 16)
        ox = int(rectangle.left / 16)
        oy = int(rectangle.top / 16)
        for x in range(ox, ox + width_tiles):
            for y in range(oy, oy + height_tiles):
                self._collision_map[x][y] = None

    def get_array(self):
        return self._collision_map
