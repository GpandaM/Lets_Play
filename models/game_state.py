from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from .base_game_state import BaseGameState
from .word_game_state import WordGameState
# from .number_game_state import NumberGameState

@dataclass
class GameState(BaseGameState):
    """Master workflow state"""
    current_game: Optional[str] = None
    number_game_count: int = 0
    word_game_count: int = 0
    should_continue: bool = True

    # Nested state objects (typed, not dicts)
    word_game_state: Optional[WordGameState] = None
    # number_game_state: Optional['NumberGameState'] = None

    input_context: Optional[str] = None  # NEW: Track which context needs input

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for LangGraph compatibility"""
        return {
            'system_message': self.system_message,
            'user_input': self.user_input,
            'needs_input': self.needs_input,
            'game_result': self.game_result,
            'error_message': self.error_message,
            'current_game': self.current_game,
            'number_game_count': self.number_game_count,
            'word_game_count': self.word_game_count,
            'should_continue': self.should_continue,
            'word_game_state': self.word_game_state,
            'input_context': self.input_context
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameState':
        """Create GameState from dictionary"""
        # Handle nested word_game_state
        if 'word_game_state' in data and data['word_game_state'] is not None:
            if isinstance(data['word_game_state'], dict):
                data['word_game_state'] = WordGameState(**data['word_game_state'])
        
        return cls(**data)