from typing import Dict
from langgraph.graph import StateGraph, END
from models.game_state import GameState
from agents.game_selector import GameSelectorAgent
from agents.number_game import NumberGameAgent
from agents.word_game import WordGameAgent
from agents.base_agent import BaseAgent
from utils.interface import CommandLineInterface

class GameSystem:
    def __init__(self):
        self.interface = CommandLineInterface()
        self.agents: Dict[str, BaseAgent] = {
            "game_selector": GameSelectorAgent(),
            "number_game": NumberGameAgent(),
            "word_game": WordGameAgent()
        }
        self.app = self._build_graph()

    
    def _route_game_choice(self, state: GameState) -> str:
        """Directly route based on current_game state"""
        if state.current_game == "number_game":
            return "number_game"
        elif state.current_game == "word_game":
            return "word_game"
        elif not state.should_continue:
            return END
        return "game_selector"  # Default to menu

    
    def _build_graph(self):
        workflow = StateGraph(GameState)

        # Add nodes
        workflow.add_node("game_selector", self.agents["game_selector"].run)
        workflow.add_node("number_game", self.agents["number_game"].run)
        workflow.add_node("word_game", self.agents["word_game"].run)
        
        # Set up routing
        workflow.add_conditional_edges(
            "game_selector",
            self._route_game_choice,
            {
                "number_game": "number_game",
                "word_game": "word_game",
                "game_selector": "game_selector",
                END: END
            }
        )

        # Game completion handling
        workflow.add_conditional_edges(
            "number_game",
            lambda state: "game_selector" if state.current_game != "number_game" else "number_game",
            {"game_selector": "game_selector", "number_game": "number_game"}
        )
        
        workflow.add_conditional_edges(
            "word_game",
            lambda state: "game_selector" if state.current_game != "word_game" else "word_game",
            {"game_selector": "game_selector", "word_game": "word_game"}
        )

        workflow.set_entry_point("game_selector")
        return workflow.compile()

    
    def run(self):
        state = GameState()
        state.current_game = None  # Start with selector
        
        while state.should_continue:
            stream = self.app.stream(state)
            for event in stream:
                node_name, current_state_dict = list(event.items())[0]
                state = GameState(**current_state_dict)
                
                # print(state)
                
                # Display messages
                if state.system_message:
                    self.interface.display(state.system_message)
                    state.system_message = None
                
                # Get input if needed
                if state.needs_input:
                    state.user_input = self.interface.get_input()
                    state.needs_input = False
                    break  # Pause further processing until input is provided
            

if __name__ == "__main__":
    game_system = GameSystem()
    game_system.run()