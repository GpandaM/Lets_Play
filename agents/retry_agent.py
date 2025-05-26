from models.game_state import GameState
from agents.base_agent import BaseAgent

# class RetryDecisionAgent(BaseAgent):
#     def run(self, state: GameState) -> GameState:
#         state.system_message = "Would you like to retry the same game? (yes/no): "
#         state.needs_input = True
#         if state.user_input and state.user_input.strip().lower() == "no":
#             state.current_game = None
#             state.word_game_state = {}
#         state.user_input = None
#         return state

class RetryDecisionAgent(BaseAgent):
    def run(self, state: GameState) -> GameState:
        if state.game_result:
            # Display game result
            result_messages = {
                "won": "🎉 Congratulations! I guessed your word!",
                "out_of_questions": "🤔 I ran out of questions.",
                "max_guesses_reached": "😅 I couldn't guess your word.",
                "no_words_left": "🤷 I have no more words to guess.",
                "user_quit": "👋 Thanks for playing!"
            }
            
            message = result_messages.get(state.game_result, f"Game ended: {state.game_result}")
            print(f"\n{message}")
            
            if state.game_result != "user_quit":
                state.system_message = "\nWould you like to play another game? (yes/no): "
                state.needs_input = True
                state.input_context = "retry"
            else:
                state.should_continue = False
            
            # Reset game state
            state.game_result = None
            state.current_game = None
            state.word_game_state = None
            
        elif state.user_input and state.input_context == "retry":
            answer = state.user_input.lower().strip()
            if answer in ['yes', 'y']:
                state.should_continue = True
            else:
                state.should_continue = False
            
            state.user_input = None
            
        return state