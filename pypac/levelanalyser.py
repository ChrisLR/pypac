"""
This is the legacy code used to analyse the image and create an array from it.
It will eventually be superceded by something better.
"""


import copy
from enum import Enum, IntEnum

from PIL import Image

from pypac.gameobjects import listing
from pypac.levels.level import Level


class AdaptedTileTypes(Enum):
    """
    An Enum holding the types required to add to a level
    """
    single = listing.get("wall_single")
    row_left = listing.get("wall_row_left")
    row_middle = listing.get("wall_row_middle")
    row_right = listing.get("wall_row_right")
    col_top = listing.get("wall_col_top")
    col_middle = listing.get("wall_col_middle")
    col_bottom = listing.get("wall_col_bottom")
    top_left = listing.get("wall_top_left")
    top_middle = listing.get("wall_top_middle")
    top_right = listing.get("wall_top_right")
    center_left = listing.get("wall_center_left")
    center_middle = listing.get("wall_center_middle")
    center_right = listing.get("wall_center_right")
    bottom_left = listing.get("wall_bottom_left")
    bottom_middle = listing.get("wall_bottom_middle")
    bottom_right = listing.get("wall_bottom_right")
    small_dot = listing.get("small_white_dot")
    ghost_door = listing.get("ghost_door")


class TileRep(IntEnum):
    """
    An enum for comparing raw array values
    """
    space = 0
    wall = 1
    door = 2


class TileNode(object):
    __slots__ = ('x', 'y', 'value')

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value


class LevelArrayAdapter(object):
    ascii_tile_map = {
        "#": TileRep.wall,
        " ": TileRep.space,
        "-": TileRep.door,
    }
    
    def __init__(self, game):
        self.game = game
        
    def make_level(self, level_info):
        tile_array = self._read_str_array(level_info.str_array)
        origin_array = copy.deepcopy(tile_array)
        new_array = self._adapt_walls(tile_array)
        new_array = self._add_coins(new_array)
        level = self._create_level_from_adapted_array(new_array, origin_array, level_info)

        return level

    def _adapt_walls(self, tile_array):
        for y, row in enumerate(tile_array):
            for x, tile_val in enumerate(row):
                if tile_val == TileRep.door:
                    tile_array[y][x] = AdaptedTileTypes.ghost_door
                if tile_val != TileRep.wall:
                    continue

                top = self._retrieve_tile_node(x, y - 1, tile_array).value
                right = self._retrieve_tile_node(x + 1, y, tile_array).value
                bottom = self._retrieve_tile_node(x, y + 1, tile_array).value
                left = self._retrieve_tile_node(x - 1, y, tile_array).value

                designation = AdaptedTileTypes.single
                if not bottom and not top:
                    # single row
                    if left and right:
                        designation = AdaptedTileTypes.row_middle
                    if not left and right:
                        designation = AdaptedTileTypes.row_left
                    elif left and not right:
                        designation = AdaptedTileTypes.row_right
                elif bottom and top:
                    # center row
                    if left and right:
                        designation = AdaptedTileTypes.center_middle
                    if not left and right:
                        designation = AdaptedTileTypes.center_left
                    elif left and not right:
                        designation = AdaptedTileTypes.center_right
                    elif not left and not right:
                        designation = AdaptedTileTypes.col_middle
                elif bottom:
                    # top row
                    if left and right:
                        designation = AdaptedTileTypes.top_middle
                    if not left and right:
                        designation = AdaptedTileTypes.top_left
                    elif left and not right:
                        designation = AdaptedTileTypes.top_right
                    elif not left and not right:
                        designation = AdaptedTileTypes.col_top
                elif top:
                    # bottom row
                    if left and right:
                        designation = AdaptedTileTypes.bottom_middle
                    if not left and right:
                        designation = AdaptedTileTypes.bottom_left
                    elif left and not right:
                        designation = AdaptedTileTypes.bottom_right
                    elif not left and not right:
                        designation = AdaptedTileTypes.col_bottom

                tile_array[y][x] = designation

        return tile_array

    def _add_coins(self, new_array):
        """
        This walks through all reachable spaces to add Coins
        """
        x = 1
        y = 2
        closed_tiles = set()
        open_tiles = [TileNode(x, y, False)]
        while open_tiles:
            tile = open_tiles.pop()
            x = tile.x
            y = tile.y
            top = self._retrieve_tile_node(x, y - 1, new_array)
            right = self._retrieve_tile_node(x + 1, y, new_array)
            bottom = self._retrieve_tile_node(x, y + 1, new_array)
            left = self._retrieve_tile_node(x - 1, y, new_array)
            new_array[y][x] = AdaptedTileTypes.small_dot
            closed_tiles.add((tile.x, tile.y))
            open_tiles.extend(
                (t for t in (top, right, bottom, left)
                 if t.value is TileRep.space and (t.x, t.y) not in closed_tiles))

        return new_array

    def _read_str_array(self, str_array):
        tile_array = [
            [self.ascii_tile_map.get(char) for char in line] 
            for line in str_array
        ]

        return tile_array
    
    def _create_level_from_adapted_array(self, new_array, origin_array, level_info):
        rows = level_info.height
        columns = level_info.width
        level = Level("generated", columns * 16, rows * 16, origin_array)
        factory = self.game.factory
        for y, row in enumerate(new_array):
            for x, tile_type in enumerate(row):
                if tile_type:
                    wall = factory.create_from_type(tile_type, None, x * 16, y * 16)
                    level.add_static(wall)
        
        return level

    def _retrieve_tile_node(self, x, y, array):
        if y <= -1 or x <= -1:
            return TileNode(x, y, None)

        try:
            return TileNode(x, y, array[y][x])
        except IndexError:
            return TileNode(x, y, None)


class ImageLevelAdapter():
    """
    Legacy code that was used to get the starting array.
    Left as an example for future endeavors
    """
    tile_ascii_map = {
        TileRep.wall: "#",
        TileRep.space: " ",
        TileRep.door: "-",
    }

    def get_array_from_image(self):
        array = [[False for _ in range(28)] for _ in range(31)]
        im = Image.open("client/graphics/emptylevel.png")
        im = im.convert('RGB')
        img_width, img_height = im.size
        for y, i in enumerate(range(0, img_height, 8)):
            for x, j in enumerate(range(0, img_width, 8)):
                box = (j, i, j + 8, i + 8)
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

    def dump_level(self, tile_array):
        str_array = "\n".join(
            ("".join((self.tile_ascii_map.get(value) for value in row)) for row in tile_array)
        )
        with open('levels/level.txt', 'w') as level_file:
            level_file.writelines(str_array)
