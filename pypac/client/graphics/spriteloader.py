import os

import pyglet


class SpriteLoader(object):
    def __init__(self):
        base_dir = str(os.path.dirname(__file__).split('pypac')[0]) + "pypac/pypac/client/graphics/"
        res_dir = base_dir
        pyglet.resource.path = [res_dir]
        pyglet.resource.reindex()
        self._sprite_sheets = {}

    def get_by_name(self, name):
        return self._sprite_sheets.get(name)

    def load_sprite_sheets(self, file_names, cell_width=16, cell_height=16, padding=0):
        """
        Loads and initialize spritesheets
        :param file_names: File names including extension of spritesheets to load
        """
        images = [(file_name.split(".")[0], file_name) for file_name in file_names]
        self._sprite_sheets.update({
            name: SpriteSheet(name, path, cell_width, cell_height, padding) for name, path in images
        })


class SpriteSheet(object):
    def __init__(self, name, path, cell_width, cell_height, padding):
        self.name = name
        self.path = path
        self.image = pyglet.resource.image(path)
        self.image_grid = self._load_image_grid(self.image, cell_width, cell_height, padding)
        self.region_names = {}

    @staticmethod
    def _load_image_grid(image, cell_width, cell_height, padding):
        rows = int(image.height / cell_height)
        cols = int(image.width / cell_width)

        return pyglet.image.ImageGrid(image, rows, cols, cell_width, cell_height,
                                      row_padding=padding, column_padding=padding)

    def get_region_by_name(self, name):
        region_tuple = self.region_names.get(name)
        if region_tuple is not None:
            image = self.image_grid[region_tuple]
            image.anchor_x = image.width / 2
            image.anchor_y = image.height / 2
            return image

        return None

    def get_region(self, row, col):
        return self.image_grid[row, col]

    def set_region_name(self, name, row, col):
        self.region_names[name] = (row, col)
