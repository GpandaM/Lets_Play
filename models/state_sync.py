from .game_state import GameState
from .base_game_state import BaseGameState
from .word_game_state import WordGameState


# class StateSynchronizer:
#     """Handles state synchronization between master and subgraphs"""
    
#     @staticmethod
#     def sync_to_subgraph(master_state: GameState, sub_state: BaseGameState) -> BaseGameState:
#         """Sync shared fields from master to subgraph"""
#         sub_state.system_message = master_state.system_message
#         sub_state.user_input = master_state.user_input
#         sub_state.needs_input = master_state.needs_input
#         sub_state.game_result = master_state.game_result
#         sub_state.error_message = master_state.error_message
#         return sub_state
    
#     @staticmethod
#     def sync_from_subgraph(master_state: GameState, sub_state: BaseGameState) -> GameState:
#         """Sync shared fields from subgraph back to master"""
#         master_state.system_message = sub_state.system_message
#         master_state.user_input = sub_state.user_input
#         master_state.needs_input = sub_state.needs_input
#         master_state.game_result = sub_state.game_result
#         master_state.error_message = sub_state.error_message

#         # Force synchronization of nested state
#         if not master_state.word_game_state:
#             master_state.word_game_state = sub_state
#         else:
#             master_state.word_game_state.__dict__.update(sub_state.__dict__)
    
#         return master_state


class StateSynchronizer:
    """Enhanced state synchronization with proper input handling"""
    @staticmethod
    def sync_to_subgraph(master_state: GameState, sub_state: BaseGameState) -> BaseGameState:
        # only forward a completed user_input into the subgraph
        if master_state.user_input is not None and not master_state.needs_input:
            sub_state.user_input   = master_state.user_input
            sub_state.needs_input  = False
            master_state.user_input = None  # consume it
        # forward errors if any
        if master_state.error_message:
            sub_state.error_message = master_state.error_message
        return sub_state

    @staticmethod
    def sync_from_subgraph(master_state: GameState, sub_state: BaseGameState) -> GameState:
        # pull back game_result/errors
        master_state.game_result   = sub_state.game_result
        master_state.error_message = sub_state.error_message

        # always update the nested word_game_state
        if isinstance(sub_state, WordGameState):
            master_state.word_game_state = sub_state

        return master_state