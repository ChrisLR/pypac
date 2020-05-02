from pypac import geom
from pypac.ai import pathfinding
from pypac.levels import levelanalyser


def test_easy_pathfind():
    level_array = levelanalyser.read_level(simple_level)
    origin = geom.Point(1 * 16, 1 * 16)
    target = geom.Point(1 * 16, 5 * 16)
    result_coordinates = list(pathfinding.a_star(origin, target, level_array))

    assert result_coordinates[0] == (1, 2)
    assert result_coordinates[1] == (1, 3)
    assert result_coordinates[2] == (1, 4)
    assert result_coordinates[3] == (1, 5)


def test_harder_pathfind():
    level_array = levelanalyser.read_level(simple_level)
    origin = geom.Point(1, 1)
    target = geom.Point(16, 5)
    result_coordinates = list(pathfinding.a_star(origin, target, level_array))
    expected_path = [
        (2, 1), (3, 1), (4, 1),
        (5, 1), (6, 1), (7, 1),
        (8, 1), (9, 1), (10, 1),
        (11, 1), (12, 1), (13, 1),
        (14, 1), (15, 1), (15, 2),
        (15, 3), (15, 4), (15, 5), (16, 5)
    ]
    assert result_coordinates == expected_path


def test_complete_pathfind():
    level_array = levelanalyser.read_level(complete_level)
    origin = geom.Point(1, 1)
    target = geom.Point(1, 29)
    result_coordinates = list(pathfinding.a_star(origin, target, level_array))
    expected_path = [
    ]
    assert result_coordinates == expected_path


simple_level = (
    "############################",
    "#                          #",
    "# #### ##### ## ##### #### #",
    "# #  # #   # ## #   # #  # #",
    "# #### ##### ## ##### #### #",
    "#            ##            #",
    "############################"
)

complete_level = (
    "############################",
    "#                          #",
    "# ########## ## ########## #",
    "# ########## ## ########## #",
    "#      ##    ##    ##      #",
    "### ## ## ######## ## ## ###",
    "### ## ## ######## ## ## ###",
    "#   ##                ##   #",
    "# #### ##### ## ##### #### #",
    "# #### ##### ## ##### #### #",
    "#            ##            #",
    "###### ## ######## ## ######",
    "###### ## ######## ## ######",
    "     # ##          ## #     ",
    "     # ## ######## ## #     ",
    "###### ## #      # ## ######",
    "          #      #          ",
    "###### ## #      # ## ######",
    "###### ## ######## ## ######",
    "     # ##          ## #     ",
    "     # ##### ## ##### #     ",
    "###### ##### ## ##### ######",
    "#      ##    ##    ##      #",
    "# #### ## ######## ## #### #",
    "# #### ## ######## ## #### #",
    "#                          #",
    "# #### ##### ## ##### #### #",
    "# #  # #   # ## #   # #  # #",
    "# #### ##### ## ##### #### #",
    "#            ##            #",
    "############################"
)
