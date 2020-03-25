import pyglet
from pyglet import gl

from pypac import gameobjects, levelanalyser
from pypac.client import input
from pypac.controllers import Player, NPC
from pypac.ai import GhostAI


class Game(object):
    def __init__(self):
        self.inputs = []
        self.window = None
        self.players = []
        self.npcs = []
        self.grid_size = 16
        self.game_objects_batch = pyglet.graphics.Batch()
        self.level_batch = pyglet.graphics.Batch()
        self.level = None

    def on_draw(self):
        self.window.clear()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glPushMatrix()
        gl.glScalef(1.5, -1.5, 0)
        gl.glOrtho(-300, 724, 650, -150, -1, 1)
        self.level_batch.draw()
        self.game_objects_batch.draw()
        gl.glPopMatrix()

    def on_key_press(self, symbol, modifiers):
        for input_ in self.inputs:
            input_.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        for input_ in self.inputs:
            input_.on_key_release(symbol, modifiers)

    def update(self, dt):
        for player in self.players:
            player.update()
        for npc in self.npcs:
            npc.update()

    def set_clear_color(self, rgb_color):
        r, g, b = rgb_color
        r = r / 255.0
        g = g / 255.0
        b = b / 255.0
        pyglet.gl.glClearColor(r, g, b, 1)

    def start(self):
        self._initialize_opengl()
        self.initialize_keyboard_players()
        self.initialize_joystick_players()
        self.initialize_ui()
        self._start_level()
        pyglet.clock.schedule_interval(self.update, 1 / 1000)
        pyglet.app.run()

    def initialize_keyboard_players(self):
        keyboard_1 = input.Keyboard(input.KeyboardMapping.default())
        keyboard_2 = input.Keyboard(input.KeyboardMapping.alternate())
        self.inputs.append(keyboard_1)
        self.inputs.append(keyboard_2)

    def initialize_ui(self):
        self.window = pyglet.window.Window(1024, 800)
        self.window.event(self.on_draw)
        self.window.event(self.on_key_press)
        self.window.event(self.on_key_release)

    def initialize_joystick_players(self):
        joysticks = pyglet.input.get_joysticks()
        for joystick in joysticks:
            joystick.open()
            joystick_mapping = input.JoystickMapping.default()
            joystick_input = input.Joystick(joystick, joystick_mapping)
            self.inputs.append(joystick_input)

    def _initialize_opengl(self):
        # Initialize Modelview matrix
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        # Set antialiasing
        gl.glEnable(gl.GL_LINE_SMOOTH)
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)

        # Set alpha blending
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glViewport(0, 0, 1024, 800)

    def _start_level(self):
        self.level = levelanalyser.make_level(self)
        ghost = gameobjects.GhostTeal(self, 32, 464)
        self.npcs.append(NPC(ghost, GhostAI))
        for _input in self.inputs:
            pacman = gameobjects.Pacman(self, 16, 16)
            self.players.append(Player(pacman, _input))


if __name__ == '__main__':
    new_game = Game()
    new_game.start()
