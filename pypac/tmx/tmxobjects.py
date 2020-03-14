from lxml import etree


class TmxMap(object):
    FLIPPED_HORIZONTALLY_FLAG = 1 << 31
    FLIPPED_VERTICALLY_FLAG = 1 << 30
    FLIPPED_DIAGONALLY_FLAG = 1 << 29

    def __init__(self, width, height, tilesets, layers, object_layers, image_layers, render_order, tile_height, tile_width, background_color=None):
        self.width = width
        self.height = height
        self.tilesets = tilesets
        self.layers = layers
        self.object_layers = object_layers
        self.image_layers = image_layers
        self.render_order = render_order
        self.tile_height = tile_height
        self.tile_width = tile_width
        self.background_color = background_color

    @property
    def pixel_width(self):
        return self.width * self.tile_width

    @property
    def pixel_height(self):
        return self.height * self.tile_height

    @classmethod
    def from_xml(cls, xml_file_name):
        with open(xml_file_name, 'rb') as xml_file:
            tree = etree.parse(xml_file)
        root = tree.getroot()
        render_order = root.attrib.get('renderorder')
        tile_width = int(root.attrib.get('tilewidth'))
        tile_height = int(root.attrib.get('tileheight'))
        map_width = int(root.attrib.get('width'))
        map_height = int(root.attrib.get('height'))
        bg_hex_color = root.attrib.get('backgroundcolor')
        background_color = None if not bg_hex_color else _hex_to_rgb(bg_hex_color)
        tilesets = []
        layers = []
        object_layers = []
        image_layers = []
        for child in root:
            if child.tag == 'tileset':
                cls._handle_xml_tileset(child, tilesets)
            elif child.tag == 'layer':
                cls._handle_tile_layer(child, tilesets, layers)
            elif child.tag == 'objectgroup':
                cls._handle_object_layer(child, tilesets, object_layers)
            elif child.tag == 'imagelayer':
                cls._handle_image_layer(child, image_layers)

        return TmxMap(map_width, map_height, tilesets, layers, object_layers, image_layers, render_order, tile_height, tile_width, background_color=background_color)

    @classmethod
    def get_tileset_used_by_gid(cls, tilesets, gid):
        return max((tileset for tileset in tilesets if tileset.first_gid <= gid),
                   key=lambda t: t.first_gid)

    @classmethod
    def _handle_xml_tileset(cls, child, tilesets):
        first_gid = int(child.attrib.get('firstgid'))
        tileset_source = "tmx\\" + child.attrib.get('source')
        tmx_tileset = TmxTileset.from_xml(tileset_source)
        tmx_tileset.first_gid = first_gid
        tilesets.append(tmx_tileset)

    @classmethod
    def _handle_tile_layer(cls, child, tilesets, layers):
        layer_id = child.attrib.get('id')
        layer_name = child.attrib.get('name')
        layer_width = int(child.attrib.get('width'))
        layer_height = int(child.attrib.get('height'))
        layer_data = child[0]
        layer_tile_data = []
        for tile_data in layer_data:
            tile_id = tile_data.get('gid')
            if tile_id:
                tile_id = int(tile_id)
                # Tile Instances do not have properties
                properties = {}
                current_tileset = cls.get_tileset_used_by_gid(tilesets, tile_id)
                tileset_tile = current_tileset.id_mapping.get(tile_id - current_tileset.first_gid)
                if not tileset_tile:
                    _, tileset_tile = cls._handle_flipped(tile_id, properties, current_tileset)
                properties.update(tileset_tile.properties)
                layer_tile_data.append((tileset_tile.tile_type, properties))
            else:
                layer_tile_data.append(None)

        layers.append(TmxLayer(layer_id, layer_name, layer_width, layer_height, layer_tile_data))

    @classmethod
    def _handle_object_layer(cls, child, tilesets, object_layers):
        layer_id = child.attrib.get('id')
        layer_name = child.attrib.get('name')
        tmx_objects = []
        for tmx_object in child:
            attribs = tmx_object.attrib
            object_gid = int(attribs['gid'])
            tileset = cls.get_tileset_used_by_gid(tilesets, object_gid)
            object_type = tileset.id_mapping.get(object_gid - tileset.first_gid)
            properties = _extract_properties(tmx_object)
            if not object_type:
                object_gid, object_type = cls._handle_flipped(object_gid, properties, tileset)

            tmx_objects.append(
                TmxObject(
                    attribs['id'], object_gid,
                    float(attribs['x']), float(attribs['y']) - 8,
                    int(attribs['width']), int(attribs['height']),
                    object_type.tile_type, properties=properties)
            )
        object_layers.append(TmxObjectLayer(layer_id, layer_name, tmx_objects))

    @classmethod
    def _handle_flipped(cls, gid, properties, tileset):
        is_flipped_horizontal = bool(gid & cls.FLIPPED_HORIZONTALLY_FLAG)
        is_flipped_vertical = bool(gid & cls.FLIPPED_VERTICALLY_FLAG)
        object_gid = gid & ~(
                cls.FLIPPED_HORIZONTALLY_FLAG
                | cls.FLIPPED_VERTICALLY_FLAG
                | cls.FLIPPED_DIAGONALLY_FLAG
        )
        object_type = tileset.id_mapping.get(object_gid - tileset.first_gid)
        if is_flipped_horizontal:
            properties['flipped_horizontal'] = True

        if is_flipped_vertical:
            properties['flipped_vertical'] = is_flipped_vertical

        return object_gid, object_type

    @classmethod
    def _handle_image_layer(cls, child, image_layers):
        attrib = child.attrib
        image_element = child[0]
        image_name = image_element.attrib.get('source').rsplit('/', 1)[1].split('.')[0]
        transparent_hex_color = image_element.attrib.get('trans')
        transparent_color = _hex_to_rgb(transparent_hex_color)
        new_image_layer = TmxImageLayer(
            attrib['id'],
            attrib['name'],
            int(attrib['offsetx']),
            int(attrib['offsety']),
            image_name,
            transparent_color
        )
        image_layers.append(new_image_layer)


_property_type_map = {
        "string": str,
        "int": int,
        "float": float,
        "bool": bool,
    }


def _extract_properties(tmx_object):
    properties = {}
    for child in tmx_object:
        if child.tag == "properties":
            for property_ in child:
                attribs = property_.attrib
                name = attribs['name']
                type_ = _property_type_map.get(attribs.get('type'))
                value = attribs['value']
                if type_ is not None:
                    value = type_(value)
                properties[name] = value

    return properties


class TmxTileset(object):
    def __init__(self, tiles, id_mapping):
        self.tiles = tiles
        self.id_mapping = id_mapping
        self.first_gid = None

    @classmethod
    def from_xml(cls, xml_file_name):
        tiles = []
        id_mapping = {}
        with open(xml_file_name, 'rb') as xml_file:
            tree = etree.parse(xml_file)
        root = tree.getroot()
        for child in root:
            if not child.tag == 'tile':
                continue

            tile_id = int(child.attrib.get('id'))
            tile_type = child.attrib.get('type')
            properties = _extract_properties(child)
            tile = TmxTile(tile_id, tile_type, properties)
            id_mapping[tile_id] = tile
            tiles.append(tile)

        return TmxTileset(tiles, id_mapping)


class TmxLayer(object):
    def __init__(self, layer_id, name, width, height, tiles):
        self.layer_id = layer_id
        self.name = name
        self.width = width
        self.height = height
        self.tiles = tiles


class TmxTile(object):
    __slots__ = ('tile_id', 'tile_type', 'properties')

    def __init__(self, tile_id, tile_type, properties=None):
        self.tile_id = tile_id
        self.tile_type = tile_type
        self.properties = properties or {}


class TmxObjectLayer(object):
    def __init__(self, layer_id, name, objects):
        self.layer_id = layer_id
        self.name = name
        self.objects = objects


class TmxImageLayer(object):
    def __init__(self, layer_id, name, offset_x, offset_y, image_name, transparent_color):
        self.layer_id = layer_id
        self.name = name
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.image_name = image_name
        self.transparent_color = transparent_color


class TmxObject(object):
    __slots__ = ('object_id', 'object_gid', 'x', 'y', 'width', 'height', 'object_type', 'properties')

    def __init__(self, object_id, object_gid, x, y, width, height, object_type, properties=None):
        self.object_id = object_id
        self.object_gid = object_gid
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.object_type = object_type
        self.properties = properties or {}


def _hex_to_rgb(hex):
    r = int(hex[1:3], 16)
    g = int(hex[3:5], 16)
    b = int(hex[5::], 16)

    return r, g, b
