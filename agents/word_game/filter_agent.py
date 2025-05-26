from models.word_game_state import WordGameState
from agents.base_agent import BaseAgent
from agents.word_game.clue_asker import ClueAsker

# class FilterAgent(BaseAgent):
#     def run(self, state: WordGameState) -> WordGameState:
#         if state.clue_index >= state.max_questions:
#             for idx, response in enumerate(state.clue_answers):
#                 predicate = ClueAsker.QUESTIONS[idx][1]
#                 print(predicate)
#                 new_possible_words = []
#                 for word in state.possible_words:
#                     matches_predicate = predicate(word)
#                     if response == "yes" and matches_predicate:
#                         new_possible_words.append(word)
#                     elif response == "no" and not matches_predicate:
#                         new_possible_words.append(word)
#                     elif response == "maybe":
#                         new_possible_words.append(word)
#                 print(f"\n\n FilterAgent : {new_possible_words}")
#                 state.possible_words = new_possible_words if new_possible_words else state.possible_words
#         return state


class FilterAgent(BaseAgent):
    """Filter possible words based on clue answers"""
    
    def run(self, state: WordGameState) -> WordGameState:
        # Simple filtering logic based on answers
        print(f"\n FilterAgent: starting run method")
        filtered_words = []
        for word in state.possible_words:
            matches = True
            
            # Apply each question's logic
            for i, answer in enumerate(state.clue_answers):
                if i < len(ClueAsker.QUESTIONS):
                    _, condition = ClueAsker.QUESTIONS[i]
                    expected = condition(word)
                    
                    if answer == 'yes' and not expected:
                        matches = False
                        break
                    elif answer == 'no' and expected:
                        matches = False
                        break
                    # 'maybe' always matches
            
            if matches:
                filtered_words.append(word)
        
        # Keep at least one word for guessing
        if not filtered_words:
            filtered_words = state.possible_words[:1]
            
        state.possible_words = filtered_words
        print(f"🔍 Narrowed down to: {', '.join(filtered_words)}")
    
        return state