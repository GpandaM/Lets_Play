import random
from models.word_game_state import WordGameState
from agents.base_agent import BaseAgent

# class GuessAgent(BaseAgent):
#     def run(self, state: WordGameState) -> WordGameState:
#         remaining_words = [w for w in state.possible_words if w not in state.tried_words]
#         if not remaining_words:
#             state.game_result = "I couldn't guess your word."
#             return state
        
#         guess = random.choice(remaining_words)
#         state.tried_words.append(guess)
#         state.guesses_made += 1
#         state.system_message = f"I think your word is: {guess}\nWas I correct? (yes/no): "
#         state.needs_input = True
        
#         if state.user_input and state.user_input.strip().lower() == "yes":
#             state.game_result = "Great! I guessed your word correctly."
#         elif state.user_input and state.user_input.strip().lower() == "no" and state.guesses_made >= state.max_guesses:
#             state.game_result = "I couldn't guess your word."
#         state.user_input = None

#         print(f"\n\n GuessAgent: state at the end is {state}")
#         return state


class GuessAgent(BaseAgent):
    """Make guesses based on filtered words"""
    
    def run(self, state: WordGameState) -> WordGameState:
        if state.guesses_made >= state.max_guesses:
            state.game_result = "max_guesses_reached"
            return state
        
        # Check if we're waiting for a guess confirmation
        if state.user_input and state.guesses_made > 0:
            answer = state.user_input.lower().strip()
            if answer in ['yes', 'y']:
                state.game_result = "won"
                return state
            elif answer in ['no', 'n']:
                # Remove the wrong guess and continue
                if state.tried_words:
                    wrong_word = state.tried_words[-1]
                    state.possible_words = [w for w in state.possible_words if w != wrong_word]
                state.user_input = None
            else:
                state.system_message = "Please answer 'yes' or 'no'. Is your word correct? "
                state.needs_input = True
                return state
        
        # Make a new guess
        if not state.user_input:  # Only make guess if we're not waiting for input
            if state.possible_words:
                guess = state.possible_words[0]  # Take first filtered word
                state.tried_words.append(guess)
                state.guesses_made += 1
                
                # Request confirmation
                state.system_message = f"🤔 I think your word is '{guess}'. Is that correct? (yes/no): "
                state.needs_input = True
                state.current_question = state.system_message
            else:
                state.game_result = "no_words_left"
                
        return state
