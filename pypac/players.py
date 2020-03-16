from pypac.keymap import Keymap


class Player(object):
    def __init__(self, game_object, input):
        self.game_object = game_object
        self.input = input

    def update(self):
        game_object = self.game_object
        actions = game_object.actions
        keymaps = self.input.get_keymaps()
        if Keymap.Left in keymaps:
            actions.move_left()
        elif Keymap.Right in keymaps:
            actions.move_right()
        elif Keymap.Up in keymaps:
            actions.move_up()
        elif Keymap.Down in keymaps:
            actions.move_down()
        self.game_object.update()
