from models.game_state import GameState
from .base_agent import BaseAgent

class WordGameAgent(BaseAgent):
    WORD_LIST = ["apple", "chair", "elephant", "guitar", "rocket", "pencil", "pizza", "tiger"]
    
    # Define question strategies with associated predicates
    QUESTIONS = [
        ("Is your word a living thing? (yes/no/maybe): ", lambda w: w in ["elephant", "tiger"]),
        ("Is your word something you can eat? (yes/no/maybe): ", lambda w: w in ["apple", "pizza"]),
        ("Is your word man-made? (yes/no/maybe): ", lambda w: w in ["chair", "guitar", "rocket", "pencil"]),
        ("Is your word longer than 5 letters? (yes/no/maybe): ", lambda w: len(w) > 5),
        ("Does your word start with a vowel? (yes/no/maybe): ", lambda w: w[0].lower() in "aeiou")
    ]

    def __init__(self):
        self.max_questions = 5

    def run(self, state: GameState) -> GameState:
        if not state.word_game_state:
            # Initialize game
            state.word_game_state = {
                "possible_words": self.WORD_LIST.copy(),
                "questions_asked": 0,
                "guesses_made": 0,
                "responses": []
            }
            # Display word list and first question
            word_list_str = ", ".join(self.WORD_LIST)
            state.system_message = (
                f"Choose a word from this list: [{word_list_str}]\n"
                f"{self._generate_question(state.word_game_state)}"
            )
            state.needs_input = True
            return state

        # Input validation
        if not state.user_input or not isinstance(state.user_input, str):
            state.system_message = "Please answer with yes/no/maybe (or yes/no for guesses): "
            state.needs_input = True
            return state

        response = state.user_input.strip().lower()
        word_state = state.word_game_state

        # If we're still asking questions
        if word_state["questions_asked"] < self.max_questions:
            if response not in ["yes", "no", "maybe"]:
                state.system_message = "Invalid input. Please answer with yes/no/maybe: "
                state.needs_input = True
                return state

            # Store the response
            word_state["responses"].append(response)

            # Narrow down words based on response
            self._narrow_words(word_state, response)

            word_state["questions_asked"] += 1

            if word_state["questions_asked"] < self.max_questions and word_state["possible_words"]:
                state.system_message = self._generate_question(word_state)
                state.needs_input = True
            else:
                # Time to guess
                guessed_word = word_state["possible_words"][0] if word_state["possible_words"] else "apple"
                word_state["guesses_made"] += 1
                state.system_message = (
                    f"I think your word is: {guessed_word}\n"
                    "Was I correct? (yes/no): "
                )
                state.needs_input = True
        else:
            # Processing guess response
            if response not in ["yes", "no"]:
                state.system_message = "Please answer with yes or no: "
                state.needs_input = True
                return state

            if response == "yes":
                state.word_game_count += 1
                state.game_result = (
                    "Great! I guessed your word correctly.\n"
                    "Returning to main menu..."
                )
                state.current_game = None
                state.word_game_state = {}
            else:
                if word_state["guesses_made"] < 1:  # Allow one retry
                    word_state["guesses_made"] += 1
                    # Reset for retry: go back to asking questions
                    word_state["possible_words"] = self.WORD_LIST.copy()
                    word_state["questions_asked"] = 0
                    word_state["responses"] = []
                    word_list_str = ", ".join(self.WORD_LIST)
                    state.system_message = (
                        f"Let's try again! Choose a word from this list: [{word_list_str}]\n"
                        f"{self._generate_question(word_state)}"
                    )
                    state.needs_input = True
                else:
                    state.word_game_count += 1
                    state.game_result = (
                        "I couldn't guess your word this time.\n"
                        "Returning to main menu..."
                    )
                    state.current_game = None
                    state.word_game_state = {}

        state.user_input = None  # Reset input for the next step
        return state

    def _generate_question(self, word_state: dict) -> str:
        # Use the next question from the predefined list
        question_idx = word_state["questions_asked"]
        if question_idx >= len(self.QUESTIONS):
            question_idx = 0  # Fallback if we run out of questions
        return self.QUESTIONS[question_idx][0]

    def _narrow_words(self, word_state: dict, response: str):
        question_idx = word_state["questions_asked"]
        if question_idx >= len(self.QUESTIONS):
            question_idx = 0
        predicate = self.QUESTIONS[question_idx][1]

        new_possible_words = []
        for word in word_state["possible_words"]:
            matches_predicate = predicate(word)
            if response == "yes" and matches_predicate:
                new_possible_words.append(word)
            elif response == "no" and not matches_predicate:
                new_possible_words.append(word)
            elif response == "maybe":
                new_possible_words.append(word)  # Keep all words on "maybe"

        word_state["possible_words"] = new_possible_words if new_possible_words else word_state["possible_words"]