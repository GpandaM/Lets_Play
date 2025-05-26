from langgraph.graph import StateGraph, END
from models.word_game_state import WordGameState
from agents.word_game.clue_asker import ClueAsker
from agents.word_game.clue_collector import ClueCollector
from agents.word_game.filter_agent import FilterAgent
from agents.word_game.guess_agent import GuessAgent

# def word_workflow():
#     workflow = StateGraph(WordGameState)
    
#     # Add nodes
#     workflow.add_node("clue_asker", ClueAsker().run)
#     workflow.add_node("clue_collector", ClueCollector().run)
#     workflow.add_node("filter_agent", FilterAgent().run)
#     workflow.add_node("guess_agent", GuessAgent().run)
    
#     # Define edges
#     workflow.set_entry_point("clue_asker")
    
#     # Clue asker routing
#     workflow.add_conditional_edges(
#         "clue_asker",
#         lambda state: (
#             "exit" if state.needs_input  # Changed condition check
#             else "clue_collector" if state.user_input 
#             else "clue_asker"
#         ),
#         {
#             "exit": END,
#             "clue_collector": "clue_collector",
#             "clue_asker": "clue_asker"
#         }
#     )
    
#     # Collector routing
#     workflow.add_conditional_edges(
#         "clue_collector",
#         lambda state: (
#             "filter_agent" if not state.needs_input and state.clue_index >= state.max_questions else
#             "clue_asker" if not state.needs_input else
#             "clue_collector"
#         ),
#         {
#             "filter_agent": "filter_agent",
#             "clue_asker": "clue_asker",
#             "clue_collector": "clue_collector"
#         }
#     )
    
#     # Filter agent routing
#     workflow.add_edge("filter_agent", "guess_agent")
    
#     # Guess agent routing
#     workflow.add_conditional_edges(
#         "guess_agent",
#         lambda state: (
#             "clue_asker" if not state.game_result and state.guesses_made < state.max_guesses else
#             "exit"
#         ),
#         {
#             "clue_asker": "clue_asker",
#             "exit": END
#         }
#     )

#     return workflow


def word_workflow():
    """Create the word game subgraph"""
    workflow = StateGraph(WordGameState)
    
    # Add nodes
    workflow.add_node("clue_asker",    ClueAsker().run)
    workflow.add_node("clue_collector",ClueCollector().run)
    workflow.add_node("filter_agent",  FilterAgent().run)
    workflow.add_node("guess_agent",   GuessAgent().run)
    
    # ←— CHANGE HERE: start with the collector, not the asker
    workflow.set_entry_point("clue_collector")
    
    # edges out of the collector
    workflow.add_conditional_edges(
        "clue_collector",
        lambda state: (
            END if state.needs_input or state.game_result
            else "filter_agent"   if state.clue_index >= state.max_questions
            else "clue_asker"
        ),
        {
            END: END,
            "filter_agent": "filter_agent",
            "clue_asker":   "clue_asker"
        }
    )
    
    # now the asker
    workflow.add_conditional_edges(
        "clue_asker",
        lambda state: (
            END if state.waiting_for_input or state.game_result
            else "clue_collector" if state.user_input
            else "clue_asker"
        ),
        {
            END: END,
            "clue_collector": "clue_collector",
            "clue_asker":     "clue_asker"
        }
    )
    
    # filter → guess
    workflow.add_edge("filter_agent", "guess_agent")
    
    # guess logic
    workflow.add_conditional_edges(
        "guess_agent",
        lambda state: (
            END if state.needs_input or state.game_result
            else "clue_asker" if state.guesses_made < state.max_guesses
            else END
        ),
        {
            END: END,
            "clue_asker": "clue_asker"
        }
    )
    
    return workflow
