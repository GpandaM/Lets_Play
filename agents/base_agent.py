from abc import ABC, abstractmethod
from typing import Dict, Any
from models.game_state import GameState

class BaseAgent(ABC):
    @abstractmethod
    def run(self, state: GameState) -> GameState:
        pass