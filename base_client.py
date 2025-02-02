import random

from game.client.user_client import UserClient
from game.commander_clash.character.character import Character, Leader
from game.common.enums import *
from game.utils.vector import *
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
        return 'Jade Orbiters', (SelectGeneric.GEN_TANK, SelectLeader.FULTRA, SelectGeneric.GEN_HEALER)

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

        return self.take_action_based_on_character(active_character, turn, world)

    def get_my_active_char(self, team_manager: TeamManager, world: GameBoard) -> Character | None:
        """
        Returns your active character based on which characters have already acted. If None is returned, that means
        none of your characters can act again until the turn order refreshes. This also means your team has fewer
        characters than the opponent.
        """

        active_character = team_manager.get_active_character(world.ordered_teams, world.active_pair_index)

        return active_character

    def take_action_based_on_character(self, character: Character, turn: int, world: GameBoard) -> list[ActionType] | None:
        if character is not None:
            opponent = self.get_opponent(character, world)
            healthy: bool = character.max_health - character.current_health <= (230 if character.name == 'Fultra' else 100)
            if turn >= 2:
                if character.rank_type is RankType.LEADER:
                    if turn == 2:
                        pass
                    else:
                        action = self.swap_to_char(character, ClassType.HEALER, world)
                        if action:
                            return action

                        opp = self.get_opp_dead(character, world)
                        if opp is not int:
                            action = self.swap_to_char(character, opp, world)
                            if action:
                                return action

                        # If SP < 2
                        if character.special_points < 2:
                            # Normal Attack
                            return [ActionType.USE_NM]


                        # - If opponent Dead
                        # if opponent is None:
                        #     # if SP > 2 & 200 below max health
                        #     if character.special_points > 2 and not healthy:
                        #         # Heal
                        #         return [ActionType.USE_S1]
                        #     else:
                        #         # else swap
                        #         return [ActionType.SWAP_UP] # CHANGE ME

                        # If 200 below max health
                        if not healthy:
                            # Heal
                            return [ActionType.USE_S1]

                        # If SP >= 5
                        if character.special_points >= 5:
                            # Special 2
                            return [ActionType.USE_S2]
                        return [ActionType.USE_NM]

                elif character.class_type == ClassType.TANK:

                    # opp = self.get_opp_dead(character, world)
                    # if opp is not int:
                    #     action = self.swap_to_char(character, opp, world)
                    #     if action:
                    #         return action

                    if character.special_points < 3:
                        return [ActionType.USE_NM]
                    elif character.special_points == 3:
                        return [ActionType.USE_S2]
                    if not healthy:
                        return self.swap_empty(character, world)

                elif character.class_type == ClassType.HEALER:
                    # opp = self.get_opp_dead(character, world)
                    # if opp > 1:
                    #     action = self.swap_to_char(character, opp, world)
                    #     if action:
                    #         return action
                    if character.special_points < 3:
                        return [ActionType.USE_NM]
                    elif character.special_points == 3:
                        return [ActionType.USE_S2]
                    if not healthy:
                        return [ActionType.USE_S1]

            elif turn == 1:
                return [ActionType.USE_NM]

            else:
                return [ActionType.USE_NM]

    def get_opponent(self, character: Character, world: GameBoard) -> Character | None:
        if character.position is not None:
            if character.position.x == 0:
                target_spot = character.position.add_x(1)
            else:
                target_spot = character.position.add_x(-1)

            char = world.get_character_from(target_spot)

            if char is Character:
                return char
        return None

    # Swap to empty
    def swap_empty(self, current: Character, world: GameBoard):
        if current.position is not None:
            target_spot = current.position

            if current.position.x == 0:
                target_spot = current.position.add_x(1)
            else:
                target_spot = current.position.add_x(-1)

            # Is slot empty
            target_spot.y = 0
            if world.get_character_from(target_spot) == None:
                diff: Vector = self.sub_vectors(target_spot, current.position)
                if(diff.y > 0):
                    return [ActionType.SWAP_UP]
                elif(diff.y < 0):
                    return [ActionType.SWAP_DOWN]

            # Find empty Slot
            # If slot > 1 from current, Ignore
            # If slot +
                # Swap Up
            # Else
                # Swap Down

    # Swap to character
    def swap_to_char(self, current: Character, target: ClassType, world: GameBoard):
        if current.position is not None:
            target_pos = None
            target_pos0 = Vector(0 if current.position.x == 1 else 1, 0)
            target_pos1 = Vector(0 if current.position.x == 1 else 1, 1)
            target_pos2 = Vector(0 if current.position.x == 1 else 1, 2)

            target_pos_opp = Vector(0 if current.position.x == 1 else 1, current.position.y)

            char_at_0: Character | None = world.get_character_from(target_pos0)
            char_at_1: Character | None = world.get_character_from(target_pos1)
            char_at_2: Character | None = world.get_character_from(target_pos2)
            char_at_opp: Character | None = world.get_character_from(target_pos_opp)

            if char_at_0 is not None:
                if char_at_0.class_type == target:
                    target_pos = target_pos0

            if char_at_1 is not None:
                if char_at_1.class_type == target:
                    target_pos = target_pos1

            if char_at_2 is not None:
                if char_at_2.class_type == target:
                    target_pos = target_pos2

            if target_pos:
                diff: Vector = self.sub_vectors(target_pos, current.position)
                print(str(target_pos) + " " + str(current.position))

                if(diff.y > 0):
                    return [ActionType.SWAP_UP]
                elif(diff.y < 0):
                    return [ActionType.SWAP_DOWN]
                else:
                    return None


    def sub_vectors(self, vect1: Vector, vect2: Vector) -> Vector:
        return Vector(vect2.x - vect1.x, vect2.y - vect1.y)

    def get_opp_dead(self, current: Character, world: GameBoard) -> int | ClassType:
        num_dead: int = 0
        if current.position is not None:
            target_pos0 = Vector(0 if current.position.x == 1 else 1, 0)
            target_pos1 = Vector(0 if current.position.x == 1 else 1, 1)
            target_pos2 = Vector(0 if current.position.x == 1 else 1, 2)

            char_at_0: Character | None = world.get_character_from(target_pos0)
            char_at_1: Character | None = world.get_character_from(target_pos1)
            char_at_2: Character | None = world.get_character_from(target_pos2)

            if char_at_0:
                num_dead += 1

            if char_at_1:
                num_dead += 1

            if char_at_2:
                num_dead += 1

            if num_dead == 1:
                if char_at_0:
                    return char_at_0.class_type
                if char_at_1:
                    return char_at_1.class_type
                if char_at_2:
                    return char_at_2.class_type

        return num_dead
