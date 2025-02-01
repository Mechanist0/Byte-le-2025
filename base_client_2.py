import random

from game.client.user_client import UserClient
from game.commander_clash.character.character import Character
from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.team_manager import TeamManager


class State(Enum):
    HEALTHY = auto()
    UNHEALTHY = auto()


class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()

    def team_data(self) -> tuple[str, tuple[SelectGeneric, SelectLeader, SelectGeneric]]:
        """
        Returns your team name (to be shown on visualizer) and a tuple of enums representing the characters you
        want for your team. The tuple of the team must be ordered as (Generic, Leader, Generic). If an enum is not
        placed in the correct order (e.g., (Generic, Leader, Leader)), whichever selection is incorrect will be
        swapped with a default value of Generic Attacker.
        """
        return 'DEFENSE', (SelectGeneric.GEN_HEALER, SelectLeader.IRWIN, SelectGeneric.GEN_ATTACKER)

    def first_turn_init(self, team_manager: TeamManager):
        """
        This is where you can put setup for things that should happen at the beginning of the first turn. This can be
        edited as needed.
        """
        self.country = team_manager.country_type
        self.my_team = team_manager.team
        self.current_state = State.HEALTHY

    def get_health_percentage(self, character: Character):
        """
        Returns a float representing the health of the given character.
        :param character: The character to get the health percentage for.
        """
        return float(character.current_health / character.max_health)

    # This is where your AI will decide what to do
    def take_turn(self, turn: int, actions: list[ActionType], world: GameBoard, team_manager: TeamManager):
        """
        This is where your AI will decide what to do.
        :param turn:         The current turn of the game.
        :param actions:      This is the actions object that you will add effort allocations or decrees to.
        :param world:        Generic world information
        :param team_manager: A class that wraps the list of Characters to control
        """
        if turn == 1:
            self.first_turn_init(team_manager)

        # get your active character for the turn; may be None
        active_character: Character = self.get_my_active_char(team_manager, world)

        # if there is no active character for my team on this current turn, return an empty list
        if active_character is None:
            return []

        # determine if the active character is healthy
        current_state: State = State.HEALTHY if self.get_health_percentage(
            active_character) >= 0.50 else State.UNHEALTHY

        actions: list[ActionType]

        if current_state == State.HEALTHY:
            # if the active character from my team is healthy, use its Normal Move
            actions = [ActionType.USE_NM]
        else:
            # if unhealthy, randomly decide to swap in a direction or use special 1
            action: ActionType = random.choice([ActionType.SWAP_UP, ActionType.SWAP_DOWN, ActionType.USE_NM])

            actions = [action]

        return actions

    def get_my_active_char(self, team_manager: TeamManager, world: GameBoard) -> Character | None:
        """
        Returns your active character based on which characters have already acted. If None is returned, that means
        none of your characters can act again until the turn order refreshes. This also means your team has fewer
        characters than the opponent.
        """

        active_character = team_manager.get_active_character(world.ordered_teams, world.active_pair_index)

        return active_character
