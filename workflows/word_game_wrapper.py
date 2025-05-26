from models.state_sync import StateSynchronizer
from models.game_state import GameState
from models.base_game_state import BaseGameState
from models.word_game_state import WordGameState
from .word_workflow import word_workflow
from agents.base_agent import BaseAgent

import traceback

class WordGameWrapper(BaseAgent):
    """Enhanced wrapper with proper state handling"""
    def __init__(self):
        self.subgraph = word_workflow().compile()
        self.sync     = StateSynchronizer()

    def run(self, master_state: GameState) -> GameState:
        print("\n\nWordGameWrapper: inside run")
        print("Master at start:", master_state)

        # 1) Init
        if master_state.word_game_state is None:
            master_state.word_game_state = WordGameState()
            print("🎯 Starting Word Game!")

        # 2) Sync down input
        wg_state = self.sync.sync_to_subgraph(
            master_state,
            master_state.word_game_state
        )
        print("✅ sync_to_subgraph done")

        # 3) Run subgraph _once_ and grab ALL outputs
        outputs = list(self.subgraph.stream(wg_state))
        print("🎯 [DEBUG] raw stream outputs:")
        for i, out in enumerate(outputs):
            print(f"  [{i}]: {out!r}")

        # 4) Pick the LAST emitted state as the “final” one
        final_wg_state = None
        for out in outputs:
            s = self._extract_state(out)
            if s:
                final_wg_state = s
        if final_wg_state is None:
            raise RuntimeError("No WordGameState in subgraph outputs!")

        # 5) Sync back
        master_state = self.sync.sync_from_subgraph(
            master_state,
            final_wg_state
        )
        print("✅ sync_from_subgraph done")

        # 6) Hand-off prompt if subgraph is asking for input
        if final_wg_state.needs_input and final_wg_state.system_message:
            print("🚀 Handing off prompt:", final_wg_state.system_message)
            master_state.needs_input    = True
            master_state.system_message = final_wg_state.system_message
            master_state.input_context  = "word"

        print("✅ master at end:", master_state)
        return master_state


    def _extract_state(self, output) -> WordGameState:
        if isinstance(output, WordGameState):
            return output
        if isinstance(output, dict):
            for v in output.values():
                if isinstance(v, WordGameState):
                    return v
            # Try constructing WordGameState directly from dict if it looks like one
            if 'possible_words' in output and 'clue_index' in output:
                try:
                    return WordGameState(**output)
                except Exception as e:
                    print(f"⚠️ Failed to cast to WordGameState: {e}")
        return None
    



# class WordGameWrapper(BaseAgent):
#     def __init__(self):
#         self.subgraph = word_workflow().compile()
#         self.sync     = StateSynchronizer()

#     def run(self, master_state: GameState) -> GameState:
        
#         # 1) initialize sub-state
#         if master_state.word_game_state is None:
#             master_state.word_game_state = WordGameState()

#         print(f"\nWordGameWrapper: before sync_to_subgraph master state is {master_state}")
#         # 2) sync master -> subgraph
#         wg = self.sync.sync_to_subgraph(master_state, master_state.word_game_state)
#         print(f"\nWordGameWrapper: after sync_to_subgraph wg state is {wg}")

#         full_output = []
#         for node_output in self.subgraph.stream(wg):
#             full_output.append(node_output)
            
#         # Get final state from last output
#         next_wg = self._get_final_state(full_output)
        
#         # Enhanced sync with debug logging
#         print(f"DEBUG - Subgraph Final State: {next_wg}")
#         master_state = self.sync.sync_from_subgraph(master_state, next_wg)
#         print(f"DEBUG - Master After Sync: {master_state}")
        
#         return master_state

#     def _get_final_state(self, outputs):
#         for output in reversed(outputs):
#             if isinstance(output, WordGameState):
#                 return output
#             if isinstance(output, dict):
#                 for v in output.values():
#                     if isinstance(v, WordGameState):
#                         return v
#         return WordGameState()  # Fallback
    

        