import json
import os

from pypac.levelanalyser import LevelArrayAdapter

# TODO These paths should be moved somewhere it makes sense
LEVEL_FOLDER_PATH = str(os.path.dirname(__file__).split('pypac')[0]) + "pypac\\pypac\\levels\\"


class LevelLoader(object):
    """
    This loads and prepares a level for use
    """
    def __init__(self, game):
        self.game = game
        level_file_names = (
            file_name for file_name in os.listdir(LEVEL_FOLDER_PATH)
            if file_name.endswith(".json")
        )
        self.level_infos = {
            level_file_name.split(".json")[0]: self._load_level_info(level_file_name)
            for level_file_name in level_file_names
        }
        self.adapter = LevelArrayAdapter(game)

    def load_level(self, level_name):
        level_info = self.level_infos.get(level_name)
        if level_info is None:
            raise ValueError(f"Invalid level name {level_name}.")

        level = self.adapter.make_level(level_info)

        return level

    def _load_level_info(self, level_file_name):
        file_path = os.path.join(LEVEL_FOLDER_PATH, level_file_name)
        with open(file_path, 'r') as level_file:
            level_info = json.load(level_file)

        return LevelInfo.from_dict(level_info)


class LevelInfo(object):
    def __init__(self, width, height, str_array):
        self.width = width
        self.height = height
        self.str_array = str_array

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            width=data_dict["width"],
            height=data_dict["height"],
            str_array=data_dict["str_array"]
        )
