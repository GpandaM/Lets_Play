# Game Zone: Command-Line Guessing Games

Welcome to **Game Zone**, a fun and interactive command-line game built in Python! This game offers two exciting guessing games: **Number Guessing Game** and **Word Guessing Game**. Test your wits as the computer tries to guess your number or word through a series of questions, or challenge it to guess correctly in as few attempts as possible!

## Overview

Game Zone is a Python-based command-line application that provides two games:
1. **Number Guessing Game**: Think of a number between 1 and 50, and the computer will try to guess it by asking if its guess is correct, higher, or lower.
2. **Word Guessing Game**: Choose a word from a predefined list, and the computer will attempt to guess it by asking yes/no/maybe questions about its properties (e.g., "Is it a living thing?").

The game tracks how many times you’ve played each game and displays a summary when you exit. It’s simple to run, easy to play, and a great way to explore interactive Python applications!

## Prerequisites

To play Game Zone, you need:
- **Python 3.11 or higher** installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- A terminal or command-line interface (e.g., Command Prompt on Windows, Terminal on macOS/Linux).
- The required Python packages (listed below).

## Installation

1. **Clone or Download the Repository**:
   - If using Git, clone the repository:
     ```bash
     git clone <repository-url>
     cd game-zone
     ```
   - Alternatively, download the project as a ZIP file and extract it.

## Architecture

### System Layers

The system is organized into five layers. Each layer has a single responsibility and communicates only with its immediate neighbors.

```
┌──────────────────────────────────────────────────────┐
│  Layer 5: Execution Loop (main.py)                   │
│  Drives the while-loop, converts state ↔ dict,       │
│  handles display and user input via CLI               │
├──────────────────────────────────────────────────────┤
│  Layer 4: Interface (CommandLineInterface)            │
│  display() and get_input() — the only code that       │
│  touches stdin/stdout                                 │
├──────────────────────────────────────────────────────┤
│  Layer 3: Orchestration (master_workflow)             │
│  LangGraph StateGraph with conditional edges.         │
│  Decides which agent runs next by inspecting state.   │
├──────────────────────────────────────────────────────┤
│  Layer 2: Agents                                      │
│  Pure functions: State → State                        │
│  Menu, Input, Validator, ErrorHandler, Retry,         │
│  WordGameWrapper, and the Word Game subgraph agents   │
├──────────────────────────────────────────────────────┤
│  Layer 1: State                                       │
│  BaseGameState → GameState → WordGameState            │
│  Single source of truth. Agents never talk directly   │
│  to each other — they communicate through state.      │
└──────────────────────────────────────────────────────┘
```

### State Hierarchy

State is layered into three tiers. Each tier is visible only to the agents that need it.

```
BaseGameState (Shared Protocol)
│   Fields every agent can read/write:
│   system_message, user_input, needs_input,
│   game_result, error_message
│
├── GameState (Orchestration State)
│   │   Fields only the orchestrator and wrappers use:
│   │   current_game, should_continue, input_context,
│   │   number_game_count, word_game_count
│   │
│   └── word_game_state: WordGameState (Domain State)
│           Fields only the word game agents use:
│           possible_words, clue_index, clue_answers,
│           tried_words, guesses_made, max_questions,
│           max_guesses, current_question, waiting_for_input
```



### State Synchronization Between Master and Subgraph

`WordGameWrapper` bridges the two graphs using `StateSynchronizer`. This is the
consume-once pattern: user input flows down, gets cleared from master, and
results flow back up.

```
    MASTER (GameState)                    SUBGRAPH (WordGameState)
    ┌──────────────────┐                  ┌──────────────────┐
    │                  │  sync_to_subgraph │                  │
    │  user_input ─────┼────────────────►  │  user_input      │
    │  (then cleared)  │                  │  needs_input=F   │
    │  error_message ──┼────────────────►  │  error_message   │
    │                  │                  │                  │
    │                  │ sync_from_subgraph│                  │
    │  game_result  ◄──┼──────────────────┼─ game_result     │
    │  error_message◄──┼──────────────────┼─ error_message   │
    │  word_game_state◄┼──────────────────┼─ (full object)   │
    │                  │                  │                  │
    │                  │  handoff (if      │                  │
    │  needs_input=T ◄─┼─ subgraph needs  │  needs_input=T   │
    │  system_message◄─┼─ user input)     │  system_message  │
    │  input_context  ◄┼─────────────────  │                  │
    │   = "word"       │                  │                  │
    └──────────────────┘                  └──────────────────┘
```

### Execution Loop (main.py)

The outer loop in `GameSystem.run()` drives everything. It is the only code that
interacts with the user and the only code that invokes the LangGraph graph.

```
┌─► Convert GameState to dict
│         │
│         ▼
│   app.stream(state_dict)
│         │
│         ▼
│   For each event in stream:
│     - Extract node name + state data
│     - Display system_message if present
│         │
│         ▼
│   Rebuild GameState from last event dict
│         │
│         ▼
│   If needs_input or word_game waiting:
│     - CLI get_input()
│     - Store in state.user_input
│     - Clear needs_input flag
│         │
│         ▼
│   Check should_continue
│         │
└───── (loop back if True)
```

### Agent Roles

| Agent | Layer | Reads | Writes | Purpose |
|-------|-------|-------|--------|---------|
| `MenuAgent` | Master | `current_game` | `system_message`, `needs_input`, `input_context` | Shows menu when no game is active |
| `InputAgent` | Master | `system_message` | `user_input`, `needs_input` | Prompts and reads user input inside the graph |
| `InputValidator` | Master | `user_input` | `current_game`, `word_game_state`, `error_message` | Parses menu choice, initializes game state |
| `ErrorHandler` | Master | `error_message` | clears `error_message`, `current_game`, `needs_input` | Displays error and resets to menu |
| `RetryDecisionAgent` | Master | `game_result`, `user_input` | `should_continue`, clears `word_game_state` | End-of-game flow: play again or quit |
| `WordGameWrapper` | Bridge | `GameState` | `GameState` (after sync) | Runs subgraph, syncs state up and down |
| `ClueAsker` | Subgraph | `clue_index` | `current_question`, `waiting_for_input`, `system_message` | Poses the next yes/no/maybe question |
| `ClueCollector` | Subgraph | `user_input` | `clue_answers`, `clue_index` | Validates and records the user's clue answer |
| `FilterAgent` | Subgraph | `clue_answers` | `possible_words` | Narrows the candidate word list |
| `GuessAgent` | Subgraph | `possible_words` | `game_result`, `guesses_made`, `tried_words` | Makes a guess and checks with the user |


## Usage

1. **Run the Game**:
   - Navigate to the project directory in your terminal:
     ```bash
     cd game-zone
     ```
   - Start the game by running:
     ```bash
     python main.py
     ```

2. **Follow the Instructions**:
   - The game will display a menu:
     ```
     Welcome to the Game Zone!
     Choose a game to play:
     1. Number Guessing Game
     2. Word Guessing Game
     3. Exit
     Enter your choice (1-3):
     ```
   - Enter `1`, `2`, or `3` to select an option.


## Dependencies

- `langgraph`: Used for state graph management to handle game flow and transitions.
  Install with:
  ```bash
  pip install langgraph
  ```

You can create a `requirements.txt` file with:
```
langgraph
```
Then install dependencies using:
```bash
pip install -r requirements.txt
```


## ------------------ Phase 2 --------------  ##
make internal nodes private in subgraph 
