"""
This is the legacy code used to analyse the image and create an array from it.
It will eventually be superceded by something better.
"""


import copy

from PIL import Image

from pypac import services
from pypac.gameobjects import listing
from pypac.levels.level import Level

m_single = listing.get("wall_single")
m_row_left = listing.get("wall_row_left")
m_row_middle = listing.get("wall_row_middle")
m_row_right = listing.get("wall_row_right")
m_col_top = listing.get("wall_col_top")
m_col_middle = listing.get("wall_col_middle")
m_col_bottom = listing.get("wall_col_bottom")
m_top_left = listing.get("wall_top_left")
m_top_middle = listing.get("wall_top_middle")
m_top_right = listing.get("wall_top_right")
m_center_left = listing.get("wall_center_left")
m_center_middle = listing.get("wall_center_middle")
m_center_right = listing.get("wall_center_right")
m_bottom_left = listing.get("wall_bottom_left")
m_bottom_middle = listing.get("wall_bottom_middle")
m_bottom_right = listing.get("wall_bottom_right")
c_small_dot = listing.get("small_white_dot")
d_ghost_door = listing.get("ghost_door")

w_space = 0
w_wall = 1
w_door = 2


def get_array_from_image():
    array = [[False for _ in range(28)] for _ in range(31)]
    im = Image.open("../client/graphics/emptylevel.png")
    im = im.convert('RGB')
    img_width, img_height = im.size
    for y, i in enumerate(range(0, img_height,  8)):
        for x, j in enumerate(range(0, img_width, 8)):
            box = (j, i, j+8, i+8)
            a = im.crop(box)
            data = a.getdata()
            for pixel in data:
                if pixel != (0, 0, 0):
                    array[y][x] = True
                    break
            else:
                array[y][x] = False

    inverse_array = [row for row in array[::-1]]

    return inverse_array


def make_level(game):
    with open('levels\\level.txt', 'r') as level_file:
        str_array = level_file.readlines()

    # Strip away the newlines from each row, since they are kept by readlines()
    for i, line in enumerate(str_array):
        str_array[i] = line[:-1]

    array = read_level(str_array)
    origin_array = copy.deepcopy(array)
    new_array = adapt_walls(array)
    new_array = add_coins(new_array)
    rows = len(array)
    columns = len(array[0])
    level = Level("generated", columns * 16, rows * 16, origin_array)
    factory = services.LameFactory(game)
    for y, row in enumerate(new_array):
        for x, tile_type in enumerate(row):
            if tile_type:
                wall = factory.create_from_type(tile_type, None, x * 16, y * 16)
                level.add_static(wall)

    return level


# TODO Do we still need this?
def retrieve(x, y, array):
    if y <= -1 or x <= -1:
        return None

    try:
        return array[y][x]
    except IndexError:
        return None


def retrieve_tile_node(x, y, array):
    if y <= -1 or x <= -1:
        return TileNode(x, y, None)

    try:
        return TileNode(x, y, array[y][x])
    except IndexError:
        return TileNode(x, y, None)


def add_coins(array):
    x = 1
    y = 2
    closed_tiles = set()
    open_tiles = [TileNode(x, y, False)]
    while open_tiles:
        tile = open_tiles.pop()
        x = tile.x
        y = tile.y
        top = retrieve_tile_node(x, y - 1, array)
        right = retrieve_tile_node(x + 1, y, array)
        bottom = retrieve_tile_node(x, y + 1, array)
        left = retrieve_tile_node(x - 1, y, array)
        array[y][x] = c_small_dot
        closed_tiles.add((tile.x, tile.y))
        open_tiles.extend(
            (t for t in (top, right, bottom, left)
             if t.value is w_space and (t.x, t.y) not in closed_tiles))

    return array


def adapt_walls(array):
    for y, row in enumerate(array):
        for x, tile_val in enumerate(row):
            if tile_val == w_door:
                array[y][x] = d_ghost_door
            if tile_val != w_wall:
                continue

            top = retrieve(x, y - 1, array)
            right = retrieve(x + 1, y, array)
            bottom = retrieve(x, y + 1, array)
            left = retrieve(x - 1, y, array)

            designation = m_single
            if not bottom and not top:
                # single row
                if left and right:
                    designation = m_row_middle
                if not left and right:
                    designation = m_row_left
                elif left and not right:
                    designation = m_row_right
            elif bottom and top:
                # center row
                if left and right:
                    designation = m_center_middle
                if not left and right:
                    designation = m_center_left
                elif left and not right:
                    designation = m_center_right
                elif not left and not right:
                    designation = m_col_middle
            elif bottom:
                # top row
                if left and right:
                    designation = m_top_middle
                if not left and right:
                    designation = m_top_left
                elif left and not right:
                    designation = m_top_right
                elif not left and not right:
                    designation = m_col_top
            elif top:
                # bottom row
                if left and right:
                    designation = m_bottom_middle
                if not left and right:
                    designation = m_bottom_left
                elif left and not right:
                    designation = m_bottom_right
                elif not left and not right:
                    designation = m_col_bottom

            array[y][x] = designation

    return array


class TileNode(object):
    __slots__ = ('x', 'y', 'value')

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value


def dump_level(array):
    def to_ascii(value):
        if value == w_wall:
            return "#"
        elif value == w_door:
            return "-"
        return " "

    str_array = "\n".join(("".join((to_ascii(value) for value in row)) for row in array))
    with open('level.txt', 'w') as level_file:
        level_file.writelines(str_array)


def read_level(str_array):
    def from_ascii(char):
        if char == "#":
            return w_wall
        elif char == " ":
            return w_space
        elif char == "-":
            return w_door
        return None

    array = [[from_ascii(char) for char in line] for line in str_array]

    return array


if __name__ == '__main__':
    array = get_array_from_image()
    dump_level(array)
