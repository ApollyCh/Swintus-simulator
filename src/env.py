# @see https://github.com/datamllab/rlcard/blob/master/rlcard/envs/uno.py

from collections import OrderedDict

import numpy as np
from rlcard.envs import Env

from .game import Game
from .utils import ACTION_LIST, ACTION_SPACE, cards2list, encode_hand, encode_target

DEFAULT_GAME_CONFIG = {"game_num_players": 2}


class Environroment(Env):
    def __init__(self, config):
        self.name = "swintus"
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = Game()
        super().__init__(config)
        self.state_shape = [
            [4, 4, 12] for _ in range(self.num_players)
        ]  # 8 number + 4 action
        self.action_shape = [None for _ in range(self.num_players)]

    def _extract_state(self, state):
        obs = np.zeros((4, 4, 12), dtype=int)
        encode_hand(obs[:3], state["hand"])
        encode_target(obs[3], state["target"])
        legal_action_id = self._get_legal_actions()
        extracted_state = {"obs": obs, "legal_actions": legal_action_id}
        extracted_state["raw_obs"] = state
        extracted_state["raw_legal_actions"] = [a for a in state["legal_actions"]]
        extracted_state["action_record"] = self.action_recorder
        return extracted_state

    def get_payoffs(self):
        return np.array(self.game.get_payoffs())

    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        if action_id in legal_ids:
            return ACTION_LIST[action_id]
        return ACTION_LIST[np.random.choice(legal_ids)]  # type: ignore

    def _get_legal_actions(self):
        legal_actions = self.game.get_legal_actions()
        legal_ids = {ACTION_SPACE[action]: None for action in legal_actions}
        return OrderedDict(legal_ids)

    def get_perfect_information(self):
        """Get the perfect information of the current state

        Returns:
            (dict): A dictionary of all the perfect information of the current state
        """
        state = {}
        state["num_players"] = self.num_players
        state["hand_cards"] = [cards2list(player.hand) for player in self.game.players]
        state["played_cards"] = cards2list(self.game.round.played_cards)
        state["target"] = self.game.round.target.str  # type: ignore
        state["current_player"] = self.game.round.current_player
        state["legal_actions"] = self.game.round.get_legal_actions(
            self.game.players, state["current_player"]
        )
        return state
