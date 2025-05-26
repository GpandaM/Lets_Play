from models.game_state import GameState
from agents.base_agent import BaseAgent
from models.word_game_state import WordGameState

class InputValidator(BaseAgent):
    def run(self, state: GameState) -> GameState:
        
        print(f"InputValidator : user_input : {state.user_input}")
        print(f"InputValidator : type of user_input : {type(state.user_input)}")
        
        if not state.user_input:
            state.error_message = "No input provided."
            state.needs_input = True
            print(f"InputValidator : not state.user_input: {state}")
            return state
        
        input_str = state.user_input.strip().lower()
        
        print(f"InputValidator : current_game : {state.current_game}")

        if state.current_game is None:
            
            print(f"InputValidator : input_str : {input_str}")
            
            if input_str in ["1", "word"]:
                print(f"InputValidator : inside the word game")
                state.current_game = "word"
                state.word_game_count += 1
                state.word_game_state = WordGameState()  # Initialize word game state
                state.needs_input = False
                print(f"and the state is {state.current_game}")
            
            elif input_str in ["2", "number"]:
                state.current_game = "number"
                state.number_game_count += 1
                # state.number_game_state = {}  # Initialize number game state
                state.needs_input = False
            
            elif input_str in ["3", "exit"]:
                state.should_continue = False
                state.needs_input = False
            
            else:
                state.error_message = "Invalid choice. Enter 1, 2, word, number, or 3."
                state.needs_input = True
        
        

        state.user_input = None
        print(f"InputValidator : user_input at the end of run function : {state.user_input}")
        print(f"InputValidator : current game at the end of run function : {state.current_game}")
        print(f"InputValidator : complete state at the end of run function : {state}")
        return state