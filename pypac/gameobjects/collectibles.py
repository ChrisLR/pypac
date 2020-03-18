from pypac.client.graphics import tile_sheet
from pypac.gameobjects.base import GameObject
from pypac.gameobjects import listing


@listing.register
class SmallWhiteDot(GameObject):
    base_img = tile_sheet.get_region(3, 4)
    type_id = "small_white_dot"


@listing.register
class MediumWhiteDot(GameObject):
    base_img = tile_sheet.get_region(3, 5)
    type_id = "medium_white_dot"


@listing.register
class LargeWhiteDot(GameObject):
    base_img = tile_sheet.get_region(3, 6)
    type_id = "large_white_dot"
