from typing import Dict
from langgraph.graph import StateGraph, END
from models.game_state import GameState
from workflows.master_workflow import master_workflow
from utils.interface import CommandLineInterface



# class GameSystem:
#     def __init__(self):
#         self.interface = CommandLineInterface()
#         self.app = master_workflow().compile()
    
#     def run(self):
#         state = GameState()
        
#         while state.should_continue:
#             # Get user input BEFORE running workflow if needed
#             if state.needs_input:
#                 state.user_input = self.interface.get_input()
#                 state.needs_input = False
            
#             # Stream through the workflow
#             stream = self.app.stream(state)
            
#             for event in stream:
#                 node_name, current_state_dict = list(event.items())[0]
#                 state = GameState(**current_state_dict)
                
#                 # Display system messages
#                 if state.system_message:
#                     self.interface.display(state.system_message)
#                     state.system_message = None

# # =============================================================================
# # USAGE
# # =============================================================================

# if __name__ == "__main__":
#     game_system = GameSystem()
#     game_system.run()



class GameSystem:
    """Fixed GameSystem with proper state management"""
    
    def __init__(self):
        self.interface = CommandLineInterface()
        self.app = master_workflow().compile()
        self.current_state = GameState()
    
    def run(self):
        """Main game loop with proper state management"""
        print("🎮 Welcome to GameZone!")
        print("=" * 50)
        
        try:
            while self.current_state.should_continue:
                # Convert state to dict for LangGraph
                state_dict = self.current_state.to_dict()
                
                # Run one step of the workflow
                stream = self.app.stream(state_dict)
                
                # Process the stream
                latest_state_dict = None
                for event in stream:
                    if event:  # Make sure event is not empty
                        # Get the latest state from the event
                        node_name, state_data = list(event.items())[0]
                        latest_state_dict = state_data
                        
                        # Handle immediate display needs
                        if isinstance(state_data, dict):
                            temp_state = GameState.from_dict(state_data)
                            if temp_state.system_message:
                                self.interface.display(temp_state.system_message)
                
                # Update current state
                if latest_state_dict:
                    self.current_state = GameState.from_dict(latest_state_dict)
                
                # Handle input requests AFTER workflow processing
                if (self.current_state.needs_input and self.current_state.system_message) or \
                    (self.current_state.word_game_state and self.current_state.word_game_state.waiting_for_input):
                    # Get user input
                    user_input = self.interface.get_input()
                    
                    # Handle quit command
                    if user_input.lower() == 'quit':
                        self.current_state.should_continue = False
                        break
                    
                    # Store input and clear flags
                    self.current_state.user_input = user_input
                    self.current_state.needs_input = False
                    self.current_state.system_message = None  # Clear after displaying
                
                if (self.current_state.needs_input or 
                    (self.current_state.word_game_state and self.current_state.word_game_state.needs_input)):
                    break # Exit loop to prompt user
                
                # Small delay to prevent rapid looping
                import time
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n👋 Game interrupted. Thanks for playing!")
        except Exception as e:
            print(f"\n❌ Error occurred: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n🎮 Thanks for playing GameZone!")

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    game_system = GameSystem()
    game_system.run()