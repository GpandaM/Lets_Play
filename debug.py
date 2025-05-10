"""
Debug script to help diagnose issues with the game system.
Place this in the same directory as your main script.
"""

from models.game_state import GameState
from utils.interface import CommandLineInterface

class MockInterface(CommandLineInterface):
    """Mock interface that prints debug information"""
    def __init__(self):
        super().__init__()
        
    def display(self, message):
        print("\nDISPLAY:", message)
        
    def get_input(self):
        print("\nGETTING INPUT...")
        user_input = input("> ")
        print(f"INPUT RECEIVED: '{user_input}'")
        return user_input

def inspect_game_state(state, title="GAME STATE"):
    """Helper to print the current state"""
    print(f"\n=== {title} ===")
    for key, value in vars(state).items():
        print(f"{key}: {value}")
    print("="*20)

# Patch your GameSystem.run() method to insert debugging:

def debug_run(self):
    """Debug version of run() with extra logging"""
    # Initialize state
    state = GameState()
    state.current_game = None
    
    step_count = 0
    
    # Main game loop
    while True:
        step_count += 1
        print(f"\n\n--- STEP {step_count} ---")
        
        inspect_game_state(state, "BEFORE PROCESSING")
        
        # Process current state through the workflow
        print("\nPROCESSING STATE THROUGH WORKFLOW...")
        stream = self.app.stream(state)
        step = next(stream, None)
        
        # Exit if the workflow ends
        if step is None:
            print("\nWORKFLOW ENDED (step is None)")
            break
            
        if not state.should_continue:
            print("\nGAME ENDING (should_continue is False)")
            break
            
        # Extract updated state
        node_name, current_state_dict = list(step.items())[0]
        print(f"\nACTIVE NODE: {node_name}")
        
        state = GameState(**current_state_dict)
        inspect_game_state(state, "AFTER PROCESSING")
        
        # Display system message if present
        if state.system_message:
            self.interface.display(state.system_message)
            state.system_message = None
        else:
            print("\nNO SYSTEM MESSAGE TO DISPLAY")
        
        # Get user input if needed
        if state.should_continue:
            print("\nGETTING USER INPUT...")
            state.user_input = self.interface.get_input()
        else:
            print("\nSKIPPING INPUT (should_continue is False)")
            
    # Display final message if applicable
    if state.system_message:
        self.interface.display(state.system_message)
    
    print("\n--- GAME ENDED ---")

