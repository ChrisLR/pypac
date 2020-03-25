from pypac import utils


def a_star(origin, target, origin_array):
    # TODO Getting a pixel coordinate and giving grid based coordinate is no good. Fix this
    go_x = int(origin.x / 16)
    go_y = int(origin.y / 16)
    gt_x = int(target.x / 16)
    gt_y = int(target.y / 16)
    origin_node = Node(go_x, go_y, 0, 0, None)
    open_nodes = [origin_node]
    target_node = Node(gt_x, gt_y, 0, 0, None)
    if retrieve_tile_node(gt_x, gt_y, origin_array, target_node, target_node) is None:
        raise ValueError("Invalid Target")

    closed_nodes = {}
    while open_nodes:
        probable_node = min(open_nodes, key=lambda n: n.cost)
        open_nodes.remove(probable_node)
        x = probable_node.x
        y = probable_node.y
        successors = (
            retrieve_tile_node(x, y - 1, origin_array, probable_node, target),
            retrieve_tile_node(x + 1, y, origin_array, probable_node, target),
            retrieve_tile_node(x, y + 1, origin_array, probable_node, target),
            retrieve_tile_node(x - 1, y, origin_array, probable_node, target)
        )
        for successor in successors:
            if successor is None:
                continue

            if successor.x == gt_x and successor.y == gt_y:
                # SUCCESS
                return gather_result(successor)
            if any((on for on in open_nodes if same_pos_and_lower(successor, on))):
                continue

            closed_node_list = closed_nodes.get((successor.x, successor.y), [])
            if any((on for on in closed_node_list if same_pos_and_lower(successor, on))):
                continue
            open_nodes.append(successor)
        closed_node_list = closed_nodes.setdefault((probable_node.x, probable_node.y), [])
        closed_node_list.append(probable_node)


def gather_result(successor):
    path = []
    while successor.parent:
        path.append((successor.x, successor.y))
        successor = successor.parent

    return reversed(path)


def same_pos_and_lower(successor, node):
    return node.x == successor.x and node.y == successor.y  # and node.cost < successor.cost


def retrieve_tile_node(x, y, array, parent_node, target):
    if y <= -1 or x <= -1:
        return None
    try:
        tile_type = array[y][x]
        if not tile_type:
            dist = utils.get_distance_from_tuples((x, y), (target.x, target.y))
            return Node(x, y, parent_node.total_movement_g, dist, parent_node)
        return None
    except IndexError:
        return None


class Node(object):
    __slots__ = ('x', 'y', 'total_movement_g', 'estimated_left_h', 'parent', 'cost')

    def __init__(self, x, y, total_movement_g, estimated_left_h, parent):
        self.x = x
        self.y = y
        self.total_movement_g = total_movement_g
        self.estimated_left_h = estimated_left_h
        self.parent = parent
        self.cost = self.total_movement_g + self.estimated_left_h
