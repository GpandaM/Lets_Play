from models.game_state import GameState
from .base_agent import BaseAgent

class GameSelectorAgent(BaseAgent):
    def run(self, state: GameState) -> GameState:
        # Handle game completion or initial state
        if state.game_result or state.current_game is None:
            state.current_game = "selecting"
            state.system_message = (
                "Welcome to the Game Zone!\n"
                "Choose a game to play:\n"
                "1. Number Guessing Game\n"
                "2. Word Guessing Game\n"
                "3. Exit\n"
                "Enter your choice (1-3): "
            )
            state.needs_input = True
            state.game_result = None
            return state

        # Process user input only if in selection mode
        if state.current_game == "selecting" and state.user_input:
            try:
                choice = state.user_input.strip()
                if choice == "1":
                    state.current_game = "number_game"
                    state.number_game_state = {}
                elif choice == "2":
                    state.current_game = "word_game"
                    state.word_game_state = {}
                elif choice == "3":
                    state.should_continue = False
                    state.system_message = "Thanks for playing!"
                else:
                    raise ValueError("Invalid choice")
                
                state.user_input = None  # Clear input after processing
            except:
                state.system_message = "Invalid input. Please enter 1, 2, or 3: "
                state.needs_input = True  # Request input again
        
        return state