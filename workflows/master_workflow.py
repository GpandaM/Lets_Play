from langgraph.graph import StateGraph, END
from agents.menu_agent import MenuAgent
from agents.input_agent import InputAgent
from agents.retry_agent import RetryDecisionAgent
from agents.input_validator import InputValidator
from agents.error_handler import ErrorHandler
from models.game_state import GameState
from workflows.word_workflow import word_workflow
from workflows.word_game_wrapper import WordGameWrapper


def master_workflow():
    workflow = StateGraph(GameState)
    
    # Add nodes
    workflow.add_node("menu", MenuAgent().run)
    workflow.add_node("input", InputAgent().run)
    workflow.add_node("input_validator", InputValidator().run)
    workflow.add_node("error_handler", ErrorHandler().run)
    workflow.add_node("retry_decision", RetryDecisionAgent().run)
    workflow.add_node("word_game", WordGameWrapper().run)
    # workflow.add_node("number_game", NumberGameWrapper().run)  # Added number game node

    # Define edges
    workflow.set_entry_point("menu")
    
    # Menu to input/error
    workflow.add_conditional_edges(
        "menu",
        lambda state: (
            "error_handler" if state.error_message 
            else "input" if state.needs_input
            else "input_validator"
        ),
        {
            "error_handler": "error_handler",
            "input": "input",
            "input_validator": "input_validator"
        }
    )

    # Input to validator or game based on current_game
    workflow.add_conditional_edges(
        "input",
        lambda state: (
            "input_validator" if state.current_game is None else
            "word_game" if state.current_game == "word" else
            # "number_game" if state.current_game == "number" else
            "retry_decision" if state.input_context == "retry" and state.user_input else
            "menu"  # Fallback, though unlikely
        ),
        {
            "input_validator": "input_validator",
            "word_game": "word_game",
            # "number_game": "number_game",
            "retry_decision" : "retry_decision",
            "menu": "menu"
        }
    )


    workflow.add_conditional_edges(
    "input_validator",
    lambda state: (
        "word_game" if state.current_game == "word"
        else "error_handler" if state.error_message
        else END if not state.should_continue
        else "menu"
    ),
    {
        "word_game": "word_game",
        "error_handler": "error_handler",
        END: END,
        "menu": "menu"
    }
)


    workflow.add_conditional_edges(
        "word_game",
        lambda state: (
            "input"               if state.needs_input      # new: hand off when subgraph wants user input
            else "retry_decision" if state.game_result  # same as before
            else "word_game"                         # otherwise keep driving the subgraph
        ),
        {
            "input": "input", 
            "retry_decision": "retry_decision",
            "word_game": "word_game"
        }
    )
    

    workflow.add_conditional_edges(
        "retry_decision",
        lambda state: (
            END if not state.should_continue
            else "menu"
        ),
        {
            END: END,
            "menu": "menu"
        }
    )
    
    # Error handler to menu
    workflow.add_edge("error_handler", "menu")
    # workflow.add_edge("retry_decision", "menu")
    
    return workflow

# def master_workflow():
#     workflow = StateGraph(GameState)
    
#     # Add nodes
#     workflow.add_node("menu", MenuAgent().run)
#     workflow.add_node("input", InputAgent().run)
#     workflow.add_node("input_validator", InputValidator().run)
#     workflow.add_node("error_handler", ErrorHandler().run)
#     workflow.add_node("retry_decision", RetryDecisionAgent().run)
#     # workflow.add_node("word_game", word_workflow().compile())  # Subgraph
#     workflow.add_node("word_game", WordGameWrapper().run)

#     # Define edges
#     workflow.set_entry_point("menu")
    

#     # Menu to input/error
#     workflow.add_conditional_edges(
#         "menu",
#         lambda state: (
#             "error_handler" if state.error_message else
#             "input"
#         ),
#         {
#             "error_handler": "error_handler",
#             "input": "input"
#         }
#     )

#     workflow.add_edge("input", "input_validator")

#     # Validator to game or error
#     workflow.add_conditional_edges(
#         "input_validator",
#         lambda state: (
#             "word_game" if state.current_game == "word" else
#             "error_handler" if state.error_message else
#             "menu"
#         ),
#         {"word_game": "word_game", "error_handler": "error_handler", "menu": "menu"}
#     )
    
#     # Word game to retry or menu
#     workflow.add_conditional_edges(
#         "word_game",
#         lambda state: (
#             "retry_decision" if state.game_result and not state.should_continue else
#             "menu" if not state.current_game else
#             "input_validator" if state.needs_input else
#             "word_game"
#         ),
#         {
#             "retry_decision": "retry_decision",
#             "menu": "menu",
#             "input_validator": "input_validator",
#             "word_game": "word_game"
#         }
#     )
    
#     # Retry to game or menu
#     workflow.add_conditional_edges(
#         "retry_decision",
#         lambda state: (
#             "word_game" if state.current_game == "word" else
#             "menu"
#         ),
#         {"word_game": "word_game", "menu": "menu"}
#     )
    
#     # Error handler to menu
#     workflow.add_edge("error_handler", "menu")
    
#     return workflow



### **--------- mermaid ----------** 

#     A[menu] -->|needs_input=True| B[input_validator]
#     A -->|!needs_input| E[error_handler]
#     B -->|current_game='word'| C[word_game]
#     B -->|error_message| E
#     B -->|else| A
#     C -->|needs_input=True| B
#     C -->|game_result && !should_continue| D[retry_decision]
#     C -->|!current_game| A
#     C -->|else| C
#     D -->|current_game='word'| C
#     D -->|else| A
#     E --> A


###   Key Transitions:


# 1. menu → input_validator (if needs_input)
#    menu → error_handler (else)

# 2. input_validator → word_game (if current_game=word)
#    input_validator → error_handler (if error_message)
#    input_validator → menu (else)

# 3. word_game → retry_decision (if game_result & !should_continue)
#    word_game → menu (if !current_game)
#    word_game → input_validator (if needs_input)
#    word_game → word_game (else)

# 4. retry_decision → word_game (if current_game=word)
#    retry_decision → menu (else)

# 5. error_handler → menu (always)