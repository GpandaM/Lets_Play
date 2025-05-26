from models.word_game_state import WordGameState
from agents.base_agent import BaseAgent


# class ClueCollector(BaseAgent):
#     def run(self, state: WordGameState) -> WordGameState:
#         if not state.user_input:
#             state.error_message = "No input provided."
#             state.needs_input = True
#             return state
        
#         input_str = state.user_input.strip().lower()
#         if input_str not in ("yes", "no", "maybe"):
#             state.error_message = "Invalid input. Please answer with yes/no/maybe."
#             state.needs_input = True
#             return state
        
#         # Valid input: store answer and advance
#         state.clue_answers.append(input_str)
#         state.clue_index += 1
#         state.user_input = None  # Clear input
#         state.needs_input = False
#         return state


class ClueCollector(BaseAgent):
    """Enhanced ClueCollector that properly processes answers"""

    def run(self, state: WordGameState) -> WordGameState:
        # Only process if we actually just got input
        if state.user_input is not None and state.waiting_for_input:
                answer = state.user_input.lower().strip()

                # Handle quit
                if answer == 'quit':
                    state.game_result = "user_quit"
                    return state

                # Validate
                if answer in ['yes','y','no','n','maybe','m']:
                    # normalize
                    if answer in ('y','yes'):
                        normalized = 'yes'
                    elif answer in ('n','no'):
                        normalized = 'no'
                    else:
                        normalized = 'maybe'

                    # record
                    state.clue_answers.append(normalized)
                    state.clue_index += 1


                    # ✅ Fully clear the “asked” flags
                    state.user_input        = None
                    state.needs_input       = False
                    state.waiting_for_input = False
                    state.system_message    = None
                    state.current_question  = None

                    print(f"✓ Answer recorded: {normalized}")
                else:

                    # Invalid answer: re‐prompt
                    state.system_message    = f"Please answer 'yes','no' or 'maybe'. {state.current_question}"

                    state.needs_input       = True
                    state.user_input        = None

        return state