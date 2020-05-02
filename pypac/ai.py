from pypac import pathfinding, utils


class GhostAI(object):
    def __init__(self, controller):
        self.controller = controller
        self._current_path = None

    def update(self):
        actor = self.controller.game_object
        if actor.actions.move_target is not None:
            return

        if not self._current_path:
            # TODO This indirect way of getting pacman must be improved
            game = actor.game
            players = game.players
            pacmen = [
                p.game_object for p in players
                if p.game_object.type_id == "pacman" and not p.game_object.dead
            ]
            if not pacmen:
                return

            closest_target = min(pacmen, key=lambda p: utils.get_distance(actor, p))
            path = pathfinding.a_star(actor, closest_target, game.level.origin_array)
            if path is not None:
                # TODO Wtf?
                self._current_path = list(path)
        else:
            next_step = self._current_path.pop(0)
            actor.actions.move_target = next_step
