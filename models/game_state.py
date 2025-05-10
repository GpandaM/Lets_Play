from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class GameState:
    current_game: Optional[str] = None

    ## count
    number_game_count: int = 0
    word_game_count: int = 0

    ## state
    number_game_state: Dict[str, Any] = field(default_factory=dict)
    word_game_state: Dict[str, Any] = field(default_factory=dict)

    ## user input
    user_input: Optional[str] = None

    ## system message
    system_message: Optional[str] = None

    ## game results
    game_result: Optional[str] = None
    
    user_input: Optional[str] = None
    needs_input: bool = False

    ## wanna continue ?
    should_continue: bool = True