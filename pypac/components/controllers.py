from pypac.client.keymap import Keymap


class Player(object):
    def __init__(self, game_object, input):
        self.game_object = game_object
        self.input = input

    def update(self):
        game_object = self.game_object
        if game_object.dead is True:
            # TODO Do something like respawn
            return

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


class NPC(object):
    def __init__(self, game_object, ai):
        self.game_object = game_object
        self.ai = ai(self)

    def update(self):
        self.ai.update()
        self.game_object.update()
