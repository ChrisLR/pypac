from pypac.client.graphics import tile_sheet
from pypac.gameobjects.base import GameObject


class Wall(GameObject):
    base_img = tile_sheet.get_region(8, 0)