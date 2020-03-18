from PIL import Image

from pypac.factory import LameFactory
from pypac.gameobjects import listing
from pypac.level import Level


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


def get_array():
    array = [[False for _ in range(32)] for _ in range(32)]
    im = Image.open("client\\graphics\\emptylevel.png")
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

    # Lets try to reverse
    inverse_array = [row for row in array[::-1]]

    return inverse_array


def make_level(game):
    array = get_array()
    adapted_array = adapt_walls(array)
    rows = len(array)
    columns = len(array[0])
    level = Level("generated", columns * 16, rows * 16)
    factory = LameFactory(game)
    for y, row in enumerate(adapted_array):
        for x, tile_type in enumerate(row):
            if tile_type is not False:
                wall = factory.create_from_type(tile_type, None, x * 16, y * 16)
                level.add_static(wall)

    return level


def adapt_walls(array):
    for y, row in enumerate(array):
        for x, tile_val in enumerate(row):
            if not tile_val:
                continue

            try:
                top = array[y - 1][x]
            except IndexError:
                top = None

            try:
                right = array[y][x + 1]
            except IndexError:
                right = None

            try:
                bottom = array[y + 1][x]
            except IndexError:
                bottom = None

            try:
                left = array[y][x - 1]
            except IndexError:
                left = None

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


if __name__ == '__main__':
    t = get_array()
    a = adapt_walls(t)
    that_str = ""
    for y in t:
        for x in y:
            that_str += str(x) if x else " "
        that_str += "\n"
    print(that_str)
