from models.game_state import GameState
from agents.base_agent import BaseAgent

# class ErrorHandler(BaseAgent):
#     def run(self, state: GameState) -> GameState:
#         if state.error_message:
#             state.system_message = f"Error: {state.error_message}\nPlease try again: "
#             state.needs_input = True
#             state.error_message = None
#         return state


class ErrorHandler(BaseAgent):
    def run(self, state: GameState) -> GameState:
        if state.error_message:
            print(f"\n{state.error_message}")
            state.error_message = None
            state.current_game = None  # Reset to menu
            state.needs_input = False  # Reset input flag
        return state