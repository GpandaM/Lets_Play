from typing import List, Optional
from dataclasses import dataclass, field
from .base_game_state import BaseGameState

@dataclass
class WordGameState(BaseGameState):
    """Word game subgraph state"""
    possible_words: List[str] = field(default_factory=lambda: [
        "apple", "chair", "elephant", "guitar", "rocket", 
        "pencil", "pizza", "tiger"
    ])
    clue_index: int = 0
    clue_answers: List[str] = field(default_factory=list)
    tried_words: List[str] = field(default_factory=list)
    guesses_made: int = 0
    max_questions: int = 5
    max_guesses: int = 2

    current_question: Optional[str] = None  # NEW: Track current question
    waiting_for_input: bool = False  # NEW: Explicit input waiting flag