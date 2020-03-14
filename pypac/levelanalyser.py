from PIL import Image
from pypac.level import Level
from pypac.factory import LameFactory


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
    rows = len(array)
    columns = len(array[0])
    level = Level("generated", columns * 16, rows * 16)
    factory = LameFactory(game)
    for y, row in enumerate(array):
        for x, tile_val in enumerate(row):
            if tile_val:
                wall = factory.make_wall(x * 16, y * 16, None)
                level.add_static(wall)

    return level


if __name__ == '__main__':
    t = get_array()
    that_str = ""
    for y in t:
        for x in y:
            that_str += "#" if x else " "
        that_str += "\n"
    print(that_str)