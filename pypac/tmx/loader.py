from pypac.level import Level
from pypac.tmx.tmxobjects import TmxMap


class TmxLoader(object):
    def __init__(self, factory, game):
        self.factory = factory
        self.game = game

    def load_map(self, map_name):
        map_file_name = "tmx\\%s.tmx" % map_name
        tmx_map = TmxMap.from_xml(map_file_name)
        level = Level(self.game, tmx_map.pixel_width, tmx_map.pixel_height)
        level.background_color = tmx_map.background_color
        for layer in tmx_map.layers:
            self._handle_tile_layer(layer, level)

        for layer in tmx_map.object_layers:
            self._handle_object_layer(layer, level)

        for layer in tmx_map.image_layers:
            self._handle_image_layer(layer, level)

        return level

    def _handle_tile_layer(self, layer, level):
        layer_data = (tile for tile in layer.tiles)
        for y in range(layer.height):
            for x in range(layer.width):
                tile_tuple = next(layer_data)
                if tile_tuple:
                    tile_type, properties = tile_tuple
                    tile = self.factory.get_or_create(tile_type, properties, x * 16, y * 16)
                    level.add_static(tile)

    def _handle_object_layer(self, layer, level):
        for tmx_object in layer.objects:
            game_object = self.factory.get_or_create(
                tmx_object.object_type, tmx_object.properties, tmx_object.x, tmx_object.y)
            level.add_game_object(game_object)

    def _handle_image_layer(self, layer, level):
        # TODO This means the Loader needs access to the sprite_loader
        pyglet_image = self.factory.sprite_loader.get_background(layer.image_name)
        image_offset = (layer.offset_x, layer.offset_y)
        level.set_background_image(pyglet_image, image_offset)
