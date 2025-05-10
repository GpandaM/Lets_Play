from models.game_state import GameState
from .base_agent import BaseAgent
import random

class WordGameAgent(BaseAgent):
    WORD_LIST = ["apple", "chair", "elephant", "guitar", "rocket", "pencil", "pizza", "tiger"]
    
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
            # Initialize game and increment counter
            state.word_game_count += 1
            state.word_game_state = {
                "possible_words": self.WORD_LIST.copy(),
                "questions_asked": 0,
                "guesses_made": 0,
                "responses": [],
                "tried_words": []  # Track guessed words
            }
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
                guessed_word = self._select_guess(word_state)
                word_state["guesses_made"] += 1
                word_state["tried_words"].append(guessed_word)
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
                state.game_result = (
                    "Great! I guessed your word correctly.\n"
                    "Returning to main menu..."
                )
                state.current_game = None
                state.word_game_state = {}
            else:
                # Try another word if available
                remaining_words = [w for w in word_state["possible_words"] if w not in word_state["tried_words"]]
                if remaining_words and word_state["guesses_made"] < 2:  # Allow up to 2 guesses
                    guessed_word = self._select_guess(word_state)
                    word_state["guesses_made"] += 1
                    word_state["tried_words"].append(guessed_word)
                    state.system_message = (
                        f"I think your word is: {guessed_word}\n"
                        "Was I correct? (yes/no): "
                    )
                    state.needs_input = True
                else:
                    # Reset for retry or end game
                    if word_state["guesses_made"] < 2:  # Allow one retry
                        word_state["guesses_made"] = 0
                        word_state["tried_words"] = []
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
                        state.game_result = (
                            "I couldn't guess your word this time.\n"
                            "Returning to main menu..."
                        )
                        state.current_game = None
                        state.word_game_state = {}

        state.user_input = None
        return state

    def _generate_question(self, word_state: dict) -> str:
        question_idx = word_state["questions_asked"]
        if question_idx >= len(self.QUESTIONS):
            question_idx = 0
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

    def _select_guess(self, word_state: dict) -> str:
        # Select a random word from remaining possible words, excluding tried words
        remaining_words = [w for w in word_state["possible_words"] if w not in word_state.get("tried_words", [])]
        return random.choice(remaining_words) if remaining_words else "apple"