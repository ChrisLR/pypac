from pypac import utils
from pypac.ai import pathfinding


class GhostAI(object):
    MAX_STEPS = 5

    def __init__(self, controller):
        self.controller = controller
        self._current_path = None
        self._steps = 0

    def update(self):
        actor = self.controller.game_object
        if actor.actions.move_target is not None:
            return

        if not self._current_path:
            self._steps = 0
            game = actor.game
            pacmen = game.locator.get_pacmen()
            if not pacmen:
                return

            closest_target = min(pacmen, key=lambda p: utils.get_distance(actor, p))
            path_iterator = pathfinding.a_star(actor, closest_target, game.level.origin_array)
            if path_iterator is not None:
                self._current_path = list(path_iterator)
        else:
            self._steps += 1
            next_step = self._current_path.pop(0)
            actor.actions.move_target = next_step
            if self._steps >= self.MAX_STEPS:
                self._current_path = None
