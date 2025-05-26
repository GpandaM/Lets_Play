from models.word_game_state import WordGameState
from agents.base_agent import BaseAgent

# class ClueAsker(BaseAgent):
#     QUESTIONS = [
#         ("Is your word a living thing? (yes/no/maybe): ", lambda w: w in ["elephant", "tiger"]),
#         ("Is your word something you can eat? (yes/no/maybe): ", lambda w: w in ["apple", "pizza"]),
#         ("Is your word man-made? (yes/no/maybe): ", lambda w: w in ["chair", "guitar", "rocket", "pencil"]),
#         ("Is your word longer than 5 letters? (yes/no/maybe): ", lambda w: len(w) > 5),
#         ("Does your word start with a vowel? (yes/no/maybe): ", lambda w: w[0].lower() in "aeiou")
#     ]

#     def run(self, state: WordGameState) -> WordGameState:
#         print(f"\n\n ClueAsker: entering with state {state}")
#         if state.clue_index >= state.max_questions or state.game_result:
#             state.game_result = state.game_result or "out_of_questions"
#             return state
        
#         # Set prompt for InputAgent to display
#         prompt, _ = self.QUESTIONS[state.clue_index]
#         state.system_message = prompt
#         state.needs_input = True
#         print(f"\nClueAsker: Prompting user with: {prompt} and state at the end of run is {state}")
#         return state


class ClueAsker(BaseAgent):
    """Enhanced ClueAsker that properly handles input requests"""

    QUESTIONS = [
        ("Is your word a living thing? (yes/no/maybe): ", lambda w: w in ["elephant", "tiger"]),
        ("Is your word something you can eat? (yes/no/maybe): ", lambda w: w in ["apple", "pizza"]),
        ("Is your word man-made? (yes/no/maybe): ", lambda w: w in ["chair", "guitar", "rocket", "pencil"]),
        ("Is your word longer than 5 letters? (yes/no/maybe): ", lambda w: len(w) > 5),
        ("Does your word start with a vowel? (yes/no/maybe): ", lambda w: w[0].lower() in "aeiou")
    ]

    def run(self, state: WordGameState) -> WordGameState:
        # end‐of‐game check unchanged
        if state.clue_index >= state.max_questions or state.game_result:
            state.game_result = state.game_result or "out_of_questions"
            return state

        # Only ask if we're not currently waiting for an answer
        if state.waiting_for_input:
            return state


        # Request input if we don't have it
        if not state.needs_input and not state.waiting_for_input:
                prompt, _ = self.QUESTIONS[state.clue_index]
                state.current_question  = prompt
                state.system_message    = prompt
                state.needs_input       = True
                state.waiting_for_input = True

        return state


            
        
        