MOVE_LEFT = 0
MOVE_RIGHT = 1
MOVE_UP = 2
MOVE_DOWN = 3


class Actions(object):
    def __init__(self, host):
        self.host = host
        self.move_target = None
        self._last_move = None

    def update(self):
        host = self.host
        if self.move_target is not None:
            if host.x == self.move_target[0] * 16 and host.y == self.move_target[1] * 16:
                self.move_target = None
            else:
                self._move_to_target()

    def move_left(self):
        host = self.host
        if self.move_target is None:
            self.move_target = int(host.x / 16) - 1, int(host.y / 16)
            if self._last_move != MOVE_LEFT:
                host.sprite.image = host.left_animation
                self._last_move = MOVE_LEFT

    def move_right(self):
        host = self.host
        if self.move_target is None:
            self.move_target = int(host.x / 16) + 1, int(host.y / 16)
            if self._last_move != MOVE_RIGHT:
                host.sprite.image = host.right_animation
                self._last_move = MOVE_RIGHT

    def move_up(self):
        host = self.host
        if self.move_target is None:
            self.move_target = int(host.x / 16), int(host.y / 16) + 1
            if self._last_move != MOVE_UP:
                host.sprite.image = host.up_animation
                self._last_move = MOVE_UP

    def move_down(self):
        host = self.host
        if self.move_target is None:
            self.move_target = int(host.x / 16), int(host.y / 16) - 1
            if self._last_move != MOVE_DOWN:
                host.sprite.image = host.down_animation
                self._last_move = MOVE_DOWN

    def _move_to_target(self):
        host = self.host
        grid_x, grid_y = self.move_target
        tx = grid_x * 16
        ty = grid_y * 16
        collider = host.game.level.static_collision_map
        collision = collider.check_collision(grid_x, grid_y)
        if collision is True or (collision and collision.blocking):
            self.move_target = None
        elif tx == host.x and ty == host.y:
            self.move_target = None
        else:
            tx = grid_x * 16
            ty = grid_y * 16
            if tx > host.x:
                host.x += host.move_speed
            elif tx < host.x:
                host.x -= host.move_speed

            if ty > host.y:
                host.y += host.move_speed
            elif ty < host.y:
                host.y -= host.move_speed
