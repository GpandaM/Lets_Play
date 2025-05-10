from models.game_state import GameState
from .base_agent import BaseAgent

class NumberGameAgent(BaseAgent):
    def __init__(self):
        self.min = 1
        self.max = 50
        self.max_attempts = 10  # Added to prevent infinite loops

    def run(self, state: GameState) -> GameState:
        if not state.number_game_state:
            initial_guess = (self.min + self.max) // 2
            state.number_game_state = {
                "min": self.min,
                "max": self.max,
                "guess": initial_guess,
                "attempts": 0
            }
            state.system_message = (
                "Think of a number between 1 and 50. I'll try to guess it!\n"
                f"Is your number {initial_guess}? (yes/higher/lower): "
            )
            state.needs_input = True
            return state

        if not state.user_input or not isinstance(state.user_input, str):
            state.system_message = "Please answer with: yes/higher/lower: "
            state.needs_input = True
            return state

        response = state.user_input.strip().lower()
        if response not in ["yes", "higher", "lower"]:
            state.system_message = "Invalid input. Please answer with: yes/higher/lower: "
            state.needs_input = True
            return state

        # Process response
        current_min = state.number_game_state["min"]
        current_max = state.number_game_state["max"]
        current_guess = state.number_game_state["guess"]
        attempts = state.number_game_state["attempts"]

        if response == "yes":
            state.number_game_count += 1
            state.game_result = (
                f"Got it! Your number was {current_guess}.\n"
                f"It took me {attempts + 1} attempts.\n"
                "Returning to main menu..."
            )
            state.current_game = None
            state.number_game_state = {}
        else:
            if response == "higher":
                new_min = max(current_min, current_guess + 1)
                state.number_game_state["min"] = new_min
            elif response == "lower":
                new_max = min(current_max, current_guess - 1)
                state.number_game_state["max"] = new_max

            # Check for convergence or max attempts
            if state.number_game_state["min"] == state.number_game_state["max"]:
                state.number_game_state["guess"] = state.number_game_state["min"]
                state.number_game_state["attempts"] += 1
                state.number_game_count += 1
                state.game_result = (
                    f"Got it! Your number was {state.number_game_state['guess']}.\n"
                    f"It took me {state.number_game_state['attempts']} attempts.\n"
                    "Returning to main menu..."
                )
                state.current_game = None
                state.number_game_state = {}
            elif state.number_game_state["attempts"] >= self.max_attempts:
                state.game_result = (
                    "I've run out of attempts! I couldn't guess your number.\n"
                    "Returning to main menu..."
                )
                state.current_game = None
                state.number_game_state = {}
            else:
                # Make new guess
                new_guess = (state.number_game_state["min"] + state.number_game_state["max"]) // 2
                state.number_game_state["guess"] = new_guess
                state.number_game_state["attempts"] += 1
                state.system_message = (
                    f"Is your number {new_guess}? (yes/higher/lower): "
                )
                state.needs_input = True

        state.user_input = None
        return state