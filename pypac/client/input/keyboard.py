import pyglet

from pypac.client.keymap import Keymap


class Keyboard(object):
    """
    This object receives keypresses and turn them into Game Actions
    """
    def __init__(self, mapping):
        self.pressed_keys = set()
        self.mapping = mapping

    def get_keymaps(self):
        return {self.mapping.get(key) for key in self.pressed_keys}

    def on_key_press(self, symbol, modifiers):
        if self.mapping.handles_keypress(symbol):
            self.pressed_keys.add(symbol)

    def on_key_release(self, symbol, modifiers):
        if symbol in self.pressed_keys:
            self.pressed_keys.remove(symbol)


class KeyboardMapping(object):
    def __init__(self, up, down, left, right, a, b, start):
        self._mapping = {
            up: Keymap.Up,
            down: Keymap.Down,
            left: Keymap.Left,
            right: Keymap.Right,
            a: Keymap.A,
            b: Keymap.B,
            start: Keymap.Start,
        }

    def get(self, symbol):
        return self._mapping.get(symbol)

    def handles_keypress(self, symbol):
        if symbol in self._mapping:
            return True
        return False

    @classmethod
    def default(cls):
        return cls(
            up=pyglet.window.key.W,
            down=pyglet.window.key.S,
            left=pyglet.window.key.A,
            right=pyglet.window.key.D,
            a=pyglet.window.key.F,
            b=pyglet.window.key.G,
            start=pyglet.window.key.T,
        )

    @classmethod
    def alternate(cls):
        return cls(
            up=pyglet.window.key.UP,
            down=pyglet.window.key.DOWN,
            left=pyglet.window.key.LEFT,
            right=pyglet.window.key.RIGHT,
            a=pyglet.window.key.NUM_0,
            b=pyglet.window.key.NUM_DECIMAL,
            start=pyglet.window.key.NUM_ENTER
        )
