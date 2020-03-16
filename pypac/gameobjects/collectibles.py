from pypac.client.graphics import tile_sheet
from pypac.gameobjects.base import GameObject


class SmallWhiteDot(GameObject):
    base_img = tile_sheet.get_region(6, 13)


class MediumWhiteDot(GameObject):
    base_img = tile_sheet.get_region(6, 14)


class LargeWhiteDot(GameObject):
    base_img = tile_sheet.get_region(6, 15)