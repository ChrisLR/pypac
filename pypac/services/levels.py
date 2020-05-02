import json
import os


LEVEL_FOLDER_PATH = "pypac/pypac/levels/"


class LevelLoader(object):
    """
    This loads and prepares a level for use
    """
    def __init__(self):
        level_file_names = (
            file_name for file_name in os.listdir(LEVEL_FOLDER_PATH)
            if file_name.endswith(".json")
        )
        self.level_infos = [self._load_level_info(level_file_name) for level_file_name in level_file_names]

    def _load_level_info(self, level_file_name):
        file_path = os.path.join(LEVEL_FOLDER_PATH, level_file_name)
        with open(file_path, 'r') as level_file:
            level_info = json.load(level_file)

        return LevelInfo.from_dict(level_info)


class LevelInfo(object):
    def __init__(self, width, height, tile_array):
        self.width = width
        self.height = height
        self.tile_array = tile_array

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            width=data_dict["width"],
            height=data_dict["height"],
            tile_array=data_dict["tile_array"]
        )
