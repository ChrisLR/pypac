from pypac.client.keymap import Keymap


class Joystick(object):
    """
    This object turns Joystick Motions/Buttons into Game Actions
    """
    THRESHOLD = 0.2
    MAX_SPEED_PER_TICK = 20

    def __init__(self, joystick, mapping):
        self.joystick = joystick
        self.mapping = mapping

    def get_keymaps(self):
        motions = self.joystick.x, self.joystick.y, self.joystick.rx, self.joystick.ry
        buttons_pressed = [i for i, pressed in enumerate(self.joystick.buttons) if pressed]
        keymaps = self.mapping.get(motions, buttons_pressed)

        return keymaps

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass


class JoystickMapping(object):
    def __init__(self, a, b, start):
        self._mapping = {
            a: Keymap.A,
            b: Keymap.B,
            start: Keymap.Start,
        }

    def get(self, motions, buttons_pressed):
        joy_x, joy_y, joy_rx, joy_ry = motions
        maps = {self._mapping.get(button) for button in buttons_pressed}
        if joy_x >= 0.5:
            maps.add(Keymap.Right)
        elif joy_x < -0.5:
            maps.add(Keymap.Left)

        if joy_y >= 0.5:
            maps.add(Keymap.Down)
        elif joy_y <= -0.5:
            maps.add(Keymap.Up)

        return maps

    @classmethod
    def default(cls):
        return cls(
            a=2,
            b=0,
            start=8
        )
