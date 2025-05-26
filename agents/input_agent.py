from models.game_state import GameState
from agents.base_agent import BaseAgent

# class InputAgent(BaseAgent):
#     def run(self, state: GameState) -> GameState:
#         if state.needs_input:
#             print(state.system_message)  # Display current prompt
#             state.user_input = str(input(">> "))
#             state.needs_input = False
#         return state


class InputAgent(BaseAgent):
    """Enhanced input agent with context awareness"""
    
    def run(self, state: GameState) -> GameState:
        if state.needs_input and state.system_message:
            print(f"\n{state.system_message}", end="")
            user_input = input(">> ").strip()
            
            # Store input and clear input request
            state.user_input = user_input
            state.needs_input = False
            state.system_message = None
            
            print(f"DEBUG - InputAgent: Received '{user_input}' for context '{state.input_context}'")
            
        return state
