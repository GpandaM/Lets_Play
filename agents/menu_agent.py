from models.game_state import GameState
from agents.base_agent import BaseAgent

# class MenuAgent(BaseAgent):
#     def run(self, state: GameState) -> GameState:
#         if state.game_result:
#             state.system_message = (
#                 f"Game over! {state.game_result}\n"
#                 f"Word games played: {state.word_game_count}\n"
#                 f"Number games played: {state.number_game_count}\n"
#                 "Choose a game: (1) Word Game, (2) Number Game, (3) Exit: "
#             )
#             state.game_result = None
#             state.current_game = None  # Reset current game
#         else:
#             state.system_message = (
#                 f"Welcome! \n"
#                 f"Word games played: {state.word_game_count}\n"
#                 f"Number games played: {state.number_game_count}\n"
#                 "Choose a game: (1) Word Game, (2) Number Game, (3) Exit: "
#             )
        
#         state.needs_input = True
#         return state

class MenuAgent(BaseAgent):
    def run(self, state: GameState) -> GameState:
        if state.current_game is None and not state.needs_input:
            state.system_message = "\n🎮 GameZone Menu\n" + "="*20 + "\n1. Word Game\n2. Number Game\n\nChoose your game (1 or 2): "
            state.needs_input = True
            state.input_context = "menu"
        return state