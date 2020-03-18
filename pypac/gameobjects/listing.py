_type_listing_by_type_id = {}


def register(type_class):
    _type_listing_by_type_id[type_class.type_id] = type_class
    return type_class


def get(type_id):
    try:
        return _type_listing_by_type_id[type_id]
    except KeyError:
        raise ValueError(f"Gameobject Type id '{type_id}' is invalid or unregistered.")
