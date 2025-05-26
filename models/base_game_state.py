from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class BaseGameState:
    """Shared fields across all game states"""
    system_message: Optional[str] = None
    user_input: Optional[str] = None
    needs_input: bool = False
    game_result: Optional[str] = None
    error_message: Optional[str] = None