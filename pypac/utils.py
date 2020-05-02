import math


def get_distance(origin_object, destination_object):
    ox = origin_object.x
    oy = origin_object.y
    dx = destination_object.x
    dy = destination_object.y
    return round(math.sqrt((ox - dx) ** 2 + (oy - dy) ** 2))


def get_distance_from_tuples(origin, destination):
    ox, oy = origin
    dx, dy = destination
    return round(math.sqrt((ox - dx) ** 2 + (oy - dy) ** 2))
